from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
from enum import Enum
import logging

log = logging.getLogger(__name__)


class ReminderTimeslot(Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"


def getUserName(update):
    return f"{update.message.from_user.username} ({update.message.from_user.id})"


def getReminders(db, update):
    return db['reminders'].find({ "user_id": update.message.from_user.id })


class Bot:
    def __init__(self, args, db):
        log.info("Creating Bot...")
        self.db = db
        self.updater = Updater(args.botToken, use_context=True)

        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("help", self.start))
        dispatcher.add_handler(CommandHandler("create", self.create))
        dispatcher.add_handler(CommandHandler("delete", self.delete))
        dispatcher.add_handler(CommandHandler("list", self.list))

        self.updater.start_polling()
        log.info("Bot listening")
        self.updater.idle()

    def start(self, update, context):
        update.message.reply_text("Hi!")

    def create(self, update, context):
        message = update.message.text.replace("/create", "")
        when = message.split()[0]
        text = message.split(" ", 2)[2]

        whenOk = when in set(item.value for item in ReminderTimeslot)
        textOk = len(text) > 0

        if whenOk and textOk:
            reminder = { "when": when, "text": text, "user_id": update.message.from_user.id }
            id = self.db.reminders.insert_one(reminder).inserted_id
            log.info(f"Saved reminder ({id}): {when} {text} from {getUserName(update)}")
            update.message.reply_text(f'Will remind you "{text}" every {when}')
        else:
            log.info(f"Received malformed message: {message}")
            update.message.reply_text(
                "Correct format: /create [morning|afternoon|evening] [reminder]"
            )

    def delete(self, update, context):
        reminders = getReminders(self.db, update)
        id = update.message.text.replace("/delete", "")
        update.message.reply_text("Not found")

    def list(self, update, context):
        reminderCount = self.db.reminders.count_documents({ "user_id": update.message.from_user.id })

        if reminderCount > 0:
            log.info(
                f"Sending list of {reminderCount} reminders to {getUserName(update)}"
            )
            message = ""
            for reminder in getReminders(self.db, update):
                message += f'Every {reminder["when"]}: "{reminder["text"]}".\n'
            update.message.reply_text(message)
        else:
            log.info(f"{getUserName(update)} has no remidners yet")
            update.message.reply_text("You don't have any reminders yet")

