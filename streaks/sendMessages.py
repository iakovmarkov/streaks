from datetime import datetime
from telegram.bot import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from models.Streak import Streak
from models.User import User
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

log = logging.getLogger(__name__)


def sendMessages(args, session: Session):
    log.info("Sending messages...")
    bot = Bot(args.botToken)
    now = datetime.now()

    streaks = session.query(Streak)  # .filter(Streak.next_date < datetime.now())

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
                [InlineKeyboardButton("✔️ Complete", callback_data=streak.id)],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id=streak.user_id, text=streak.title, reply_markup=reply_markup
            )
        log.info(f"Updated & sent {streaks.count()} streaks.")
    else:
        log.info(f"No messages to send")
