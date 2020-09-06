from commands.Command import Command
from models.User import User
from models.Streak import Streak
from utils.getUserName import getUserName
from telegram import Update, ParseMode
import logging

log = logging.getLogger(__name__)


class Delete(Command):
    command = "_d"

    def run(bot, update: Update, payload):
        id = payload
        query = update.callback_query
        uid = query.message.chat.id

        streak = bot.session.query(Streak).filter(
            Streak.id == id, Streak.user_id == uid
        )

        if streak.count() == 0:
            query.answer(text="Something went wrong.")
            log.warn(f"Could not delete reminder {id} for {uid}")
            return

        try:
            streak = streak.first()
            when = streak.when
            title = streak.title
            bot.session.delete(streak)
            bot.session.commit()

            log.info(f"Deleted reminder {id} for {uid}")
            query.answer(text="Streak removed")
            query.edit_message_text(
                text=f"<del>{query.message.text}</del>",
                parse_mode=ParseMode.HTML,
                reply_markup=None,
            )
        except Exception as e:
            bot.session.rollback()
            log.error(f"Error deleting '{id}' for {uid}: {e}")
            query.answer(text="Something went wrong.")
