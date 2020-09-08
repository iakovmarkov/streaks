from datetime import datetime, timezone, timedelta, time
from telegram.bot import Bot
from models.Streak import Streak
from models.User import User
from sqlalchemy.orm import Session
from sqlalchemy import func
from commands.complete import Complete
from commands.info import Info
from utils.get_markup import get_markup
from utils.callbacks import CallbackKeys
from utils.get_streak_info import get_streak_info
import logging
import json

log = logging.getLogger(__name__)
nl = "\n"  # Python, why won't you allow this in the f-string?


def send_reminders(tz, session: Session, bot: Bot):
    users = session.query(User).filter(User.timezone == tz)
    streaks = session.query(Streak).filter(
        Streak.next_date < datetime.now(),
        Streak.user_id.in_(map(lambda user: user.id, users.all())),
    )

    ## Greet
    for streak in streaks.group_by(Streak.user_id).all():
        text = f"Hi {streak.user_id}! Those are your goals for today:"
        bot.send_message(chat_id=streak.user_id, text=text)

    ## Send streaks
    if streaks.count() > 0:
        for streak in streaks.all():
            streak.prev_date = datetime.now()
            streak.next_date = Streak.calc_next_date(streak)
            try:
                session.add(streak)
                session.commit()
            except Exception as e:
                session.rollback()
                log.error(f"Error commiting {streak.id} to DB: {e}")

            bot.send_message(
                chat_id=streak.user_id,
                text=streak.title,
                reply_markup=get_markup(streak=streak, can_complete=True),
            )
        log.info(f"Updated & sent {streaks.count()} streaks.")
    else:
        log.info(f"No reminders to send")


def send_summary(tz, session: Session, bot: Bot):
    users = session.query(User).filter(User.timezone == tz)

    for user in users.all():
        bot.send_message(chat_id=user.id, text="👋")
        streaks = session.query(Streak).filter(Streak.user_id == user.id)
        for streak in streaks:
            if streak.last_track_date < streak.prev_date:
                text = "Don't forget to mark what you've done today. And don't cheat!"
                bot.send_message(chat_id=user.id, text=text)
                return

        text = "Good job completing all your streaks today!"
        bot.send_message(chat_id=user.id, text=text)


def send_stats(tz, session: Session, bot: Bot):
    users = session.query(User).filter(User.timezone == tz)

    for user in users.all():
        streaks = session.query(Streak).filter(Streak.user_id == user.id, Streak.count_streak > 0)

        if streaks.count() == 0:
            return

        bot.send_message(chat_id=user.id, text="Good day! Those are your stats so far:")
        for streak in streaks:
            bot.send_message(chat_id=user.id, text=f"{nl}{nl}".join(get_streak_info(streak)))
        text = "You're doing a great job!"
        bot.send_message(chat_id=user.id, text=text)


def send(args, session: Session):
    log.info("Sending messages...")
    bot = Bot(args.bot_token)
    currentHour = datetime.utcnow().hour

    morning_tz = 8 - currentHour
    log.info(f"Will send morning reminders to users with TZ {morning_tz}")
    send_reminders(morning_tz, session, bot)

    evening_tz = 22 - currentHour
    log.info(f"Will send evening summary to users with TZ {evening_tz}")
    send_summary(evening_tz, session, bot)

    noon_tz = 13 - currentHour
    tz = timezone(timedelta(hours=noon_tz))
    if datetime.now(tz=tz).weekday() == 0:
        log.info(f"Will send last week summary to users with TZ {noon_tz}")
        send_stats(noon_tz, session, bot)
