from commands.Command import Command
from commands.delete import Delete
from models.User import User
from models.Streak import Streak
from utils.getUserName import getUserName
from utils.callbacks import CallbackKeys
from utils.callbacks import CallbackKeys
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import logging
import json

log = logging.getLogger(__name__)


def get_markup(streak: Streak):
    keyboard = [
        [
            InlineKeyboardButton(
                "Delete",
                callback_data=json.dumps(
                    {
                        CallbackKeys.COMMAND.value: Delete.command,
                        CallbackKeys.PAYLOAD.value: streak.id,
                    }
                ),
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


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
                f"Sending list of {streaks.count()} streaks to {getUserName(update)}"
            )
            for streak in streaks.all():
                message = f'Every {streak.when}: "{streak.title}".'
                update.message.reply_text(
                    text=message,
                    reply_markup=get_markup(streak),
                )
        else:
            log.info(f"{getUserName(update)} has no remidners yet")
            update.message.reply_text("You don't have any reminders yet")
