from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from models.Streak import Streak
from commands.complete import Complete
from commands.delete import Delete
from commands.info import Info
from utils.callbacks import CallbackKeys
import json

def get_markup(streak: Streak, can_delete = False, can_complete=False):
    keyboard = []

    if can_delete:
        keyboard.append(
            InlineKeyboardButton(
                "🗑️ Delete",
                callback_data=json.dumps(
                    {
                        CallbackKeys.COMMAND.value: Delete.command,
                        CallbackKeys.PAYLOAD.value: streak.id,
                    }
                ),
            ),
        )

    if can_complete:
        keyboard.append(
            InlineKeyboardButton(
                "✔️ Complete",
                callback_data=json.dumps(
                    {
                        CallbackKeys.COMMAND.value: Complete.command,
                        CallbackKeys.PAYLOAD.value: streak.id,
                    }
                ),
            ),
        )

    keyboard.append(        
        InlineKeyboardButton(
            f"📈 Current streak: {streak.count_streak}",
            callback_data=json.dumps(
                {
                    CallbackKeys.COMMAND.value: Info.command,
                    CallbackKeys.PAYLOAD.value: streak.id,
                }
            ),
        )
    )
    return InlineKeyboardMarkup([keyboard])