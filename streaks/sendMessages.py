from datetime import datetime, timezone, timedelta, time
from telegram.bot import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from models.Streak import Streak
from models.User import User
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging
import json

log = logging.getLogger(__name__)


def sendMessages(args, session: Session):
    log.info("Sending messages...")
    bot = Bot(args.botToken)
    now = datetime.now()
    currentHour = datetime.utcnow().hour

    morning_tz = 8 - currentHour
    users = session.query(User).filter(User.timezone == morning_tz)

    log.info(
        f"Will send morning reminders to {users.count()} users with TZ {morning_tz}"
    )

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
            streak.prev_date = now
            streak.next_date = Streak.calc_next_date(streak)
            try:
                session.add(streak)
                session.commit()
            except Exception as e:
                session.rollback()
                log.error(f"Error commiting {streak.id} to DB: {e}")

            keyboard = [
                [
                    InlineKeyboardButton(
                        "✔️ Complete",
                        callback_data=json.dumps(
                            {"action": "complete", "id": streak.id}
                        ),
                    )
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id=streak.user_id, text=streak.title, reply_markup=reply_markup
            )
        log.info(f"Updated & sent {streaks.count()} streaks.")
    else:
        log.info(f"No streaks to send")

    evening_tz = 22 - currentHour
    users = session.query(User).filter(User.timezone == evening_tz)
    log.info(f"Will send evening summary to {users.count()} users with TZ {evening_tz}")

    for user in users.all():
        bot.send_message(chat_id=user.id, text="👋")
        text = ""
        streaks = session.query(Streak).filter(Streak.user_id == user.id)
        for streak in streaks:
            if streak.last_track_date < streak.prev_date:
                text += "Don't forget to mark what you've done today. And don't cheat!"
                bot.send_message(chat_id=user.id, text=text)
                return

        text += "Good job completing all your streaks today!"
        bot.send_message(chat_id=user.id, text=text)
