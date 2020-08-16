from bson.objectid import ObjectId
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
    return db["reminders"].find({"user_id": update.message.from_user.id})


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

    ## /start
    ## Sends a welcome message listing all possible commands
    def start(self, update, context):
        nl = "\n"  # Python, why won't you allow this in the f-string?
        commands = [
            "/create [morning|afternoon|evening] [reminder] - will create a new reminder",
            "/list - will send you all your reminders",
            "/delete [id] - will delete a reminder",
            "/help - this message",
        ]
        update.message.reply_text(
            f"Hi. I am your Care Bot 👋{nl}I know the following commands:{nl.join(commands)}"
        )
        update.message.reply_text(f"Made by @iakovmarkov. {nl}Known issues: there is no way to edit the reminder. Delete it and create again 🙏")

    ## /create [morning|afternoon|evening] [reminder]
    ## Creates a new reminder for the user
    def create(self, update, context):
        message = update.message.text.replace("/create", "").strip()

        when = message.split()[0]

        textFragments = message.split()
        textFragments.remove(when)
        text = " ".join(textFragments)

        whenOk = when in set(item.value for item in ReminderTimeslot)
        textOk = len(text) > 0

        if whenOk and textOk:
            reminder = {
                "when": when,
                "text": text,
                "user_id": update.message.from_user.id,
            }
            id = self.db.reminders.insert_one(reminder).inserted_id
            log.info(f"Saved reminder ({id}): {when} {text} from {getUserName(update)}")
            update.message.reply_text(f'Will remind you "{text}" every {when}')
        else:
            log.info(f"Received malformed message: {message}")
            update.message.reply_text(
                "Correct format: /create [morning|afternoon|evening] [reminder]"
            )

    ## /delete [id]
    ## Checks if the reminder belongs to the user, and removes the reminder.
    def delete(self, update, context):
        id = update.message.text.replace("/delete", "").strip()

        if id == None:
            update.message.reply_text("Correct format: /delete [id]")
            return

        filter = {"_id": ObjectId(id), "user_id": update.message.from_user.id}

        reminder = self.db.reminders.find_one(filter)

        if reminder == None:
            update.message.reply_text("Not found")
            log.warn(f"Could not delete reminder {id} for {getUserName(update)}")
            return

        self.db.reminders.remove(filter)
        log.info(f"Deleted reminder {id} for {getUserName(update)}")
        update.message.reply_text(
            f'I will not remind you to "{reminder["text"]}" every {reminder["when"]} then.'
        )

    ## /list
    ## Lists all reminders for the user
    def list(self, update, context):
        reminderCount = self.db.reminders.count_documents(
            {"user_id": update.message.from_user.id}
        )

        if reminderCount > 0:
            log.info(
                f"Sending list of {reminderCount} reminders to {getUserName(update)}"
            )
            message = ""
            for reminder in getReminders(self.db, update):
                message += f'Every {reminder["when"]}: "{reminder["text"]}" ({reminder["_id"]}).\n'
            update.message.reply_text(message)
        else:
            log.info(f"{getUserName(update)} has no remidners yet")
            update.message.reply_text("You don't have any reminders yet")

