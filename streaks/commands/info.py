from commands.Command import Command
from models.User import User
from models.Streak import Streak
from utils.get_streak_info import get_streak_info
from datetime import datetime, timedelta, time, timezone
from telegram import Update, ParseMode
import logging

log = logging.getLogger(__name__)
nl = "\n"  # Python, why won't you allow this in the f-string?

class Info(Command):
    command = "_i"

    def run(bot, update: Update, payload):
        query = update.callback_query
        streak_id = payload
        uid = query.message.chat.id
        streak = bot.session.query(Streak).filter(
            Streak.id == streak_id, Streak.user_id == uid
        )

        if streak.count() == 0:
            query.answer(text="Something went wrong.")
            log.warning(f"Could not get info about {streak_id} for {uid}")
            return

        streak = streak.first()

        lines = get_streak_info(streak)
                    
        query.answer()
        query.message.reply_text(text=f"{nl}{nl}".join(lines))
