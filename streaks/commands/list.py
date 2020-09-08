from commands.Command import Command
from models.User import User
from models.Streak import Streak
from utils.get_username import get_username
from utils.get_markup import get_markup
from telegram import Update
import logging

log = logging.getLogger(__name__)

class List(Command):
    command = "list"

    def describe(bot, update, context):
        return "list all your reminders"

    def help(bot, update, context):
        return List.describe(bot, update, context)

    def run(bot, update: Update, context):
        uid = update.message.from_user.id
        streaks = bot.session.query(Streak).filter_by(user_id=uid)

        if streaks.count() > 0:
            log.info(
                f"Sending list of {streaks.count()} streaks to {get_username(update)}"
            )
            for streak in streaks.all():
                message = f'Every {streak.when}: "{streak.title}".'
                update.message.reply_text(
                    text=message,
                    reply_markup=get_markup(streak=streak, can_delete=True),
                )
        else:
            log.info(f"{get_username(update)} has no remidners yet")
            update.message.reply_text("You don't have any reminders yet")
