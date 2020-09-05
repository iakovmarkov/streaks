from datetime import datetime
from telegram.bot import Bot
from models.Streak import Streak
from models.User import User
from sqlalchemy.orm import Session
import logging

log = logging.getLogger(__name__)


def sendMessages(args, session: Session):
    log.info("Sending messages...")
    bot = Bot(args.botToken)
    now = datetime.now()

    streaks = session.query(Streak).filter(Streak.next_date < datetime.now())

    if streaks.count() > 0:
        for streak in streaks.all():
            streak.prev_date = now
            streak.next_date = Streak.calc_next_date(streak)
            session.add(streak)
            bot.send_message(chat_id=streak.user_id, text=streak.title)
        log.debug(f"Sent {streaks.count()} messages.")
    else:
        log.debug(f"No messages to send")

    try:
        session.commit()
        log.info(f"Updated {streaks.count()} streaks.")
    except Exception as e:
        session.rollback()
        log.error(f"Error commiting to DB: {e}")
