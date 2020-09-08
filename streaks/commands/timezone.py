from commands.Command import Command
from models.User import User
from models.Streak import Streak
from utils.get_username import get_username
import logging

log = logging.getLogger(__name__)


class Timezone(Command):
    command = "timezone"

    def describe(bot, update, context):
        return "[tz] - set your time zone (-01, +02, etc)"

    def help(bot, update, context):
        return "[tz] - set your time zone (-01, +02, etc)"

    def run(bot, update, context):
        tz = update.message.text.replace("/timezone", "").strip()
        uid = update.message.from_user.id

        if tz == None or tz == "":
            update.message.reply_text("Correct format: /timezone [tz]")
            return

        tz = int(tz)

        try:
            user = bot.session.query(User).get(uid) or User(id=uid)
            user.timezone = tz
            bot.session.add(user)
            bot.session.commit()

            log.info(f"Set TZ to {tz} for {get_username(update)}")
            update.message.reply_text(f"Set your timezone to {tz}")
        except Exception as e:
            bot.session.rollback()
            log.error(f"Error setting TZ to '{tz}' for {get_username(update)}: {e}")
            update.message.reply_text(f"Sorry, something went wrong.")
