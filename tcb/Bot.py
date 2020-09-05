from bson.objectid import ObjectId
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
from telegram import Update
import logging
from sqlalchemy.orm import Session
from models.User import User
from models.Streak import Streak
from utils import getUserName

log = logging.getLogger(__name__)


class Bot:
    def __init__(self, args, session: Session):
        log.info("Creating Bot...")
        self.session = session
        self.updater = Updater(args.botToken, use_context=True)

        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("help", self.start))
        dispatcher.add_handler(CommandHandler("create", self.create))
        dispatcher.add_handler(CommandHandler("track", self.create))
        dispatcher.add_handler(CommandHandler("remind", self.create))
        dispatcher.add_handler(CommandHandler("delete", self.delete))
        dispatcher.add_handler(CommandHandler("list", self.list))
        dispatcher.add_handler(CommandHandler("timezone", self.timezone))

        self.updater.start_polling()
        log.info("Bot listening")
        self.updater.idle()

    ## /start
    ## Sends a welcome message listing all possible commands
    def start(self, update, context):
        nl = "\n"  # Python, why won't you allow this in the f-string?
        commands = [
            "/create [morning|afternoon|evening] [reminder] - create a new reminder",
            "/list - list all your reminders",
            "/delete [id] - delete a reminder",
            "/timezone [tz] - set your time zone (-01, +02, etc)",
            "/help - this message",
        ]
        update.message.reply_text(
            f"Hi. I am your Care Bot 👋{nl}I know the following commands:{nl}{nl.join(commands)}"
        )
        update.message.reply_text(
            f"Made by @iakovmarkov. {nl}Known issues: there is no way to edit the reminder. Delete it and create again 🙏"
        )

    ## /create [morning|afternoon|evening] [streak]
    ## Creates a new streak for the user
    def create(self, update: Update, context):
        message = update.message.text.replace("/create", "").strip()

        uid = update.message.from_user.id
        when = message.split()[0]

        textFragments = message.split()
        textFragments.remove(when)
        text = " ".join(textFragments)

        whenOk = True
        textOk = len(text) > 0

        if not (whenOk and textOk):
            log.info(f"Received malformed message: {message}")
            update.message.reply_text(
                "Correct format: /create [morning|afternoon|evening] [reminder]"
            )
            return

        # try:
        user = self.session.query(User).get(uid) or User(id=uid)
        streak = Streak(title=text, user=uid, when=when)

        self.session.add_all([user, streak])
        self.session.commit()

        log.info(
            f"Saved streak ({streak.id}): {when} {text} from {getUserName(update)}"
        )
        update.message.reply_text(f'Will remind you "{text}" every {when}')
        # except Exception as e:
        #     self.session.rollback()
        #     log.error(
        #         f"Error creating '{when}' / '{text}' for {getUserName(update)}: {e}"
        #     )
        #     update.message.reply_text(f"Sorry, something went wrong.")

    ## /delete [id]
    ## Checks if the reminder belongs to the user, and removes the reminder.
    def delete(self, update, context):
        id = update.message.text.replace("/delete", "").strip()
        uid = update.message.from_user.id

        if id == None or id == "":
            update.message.reply_text("Correct format: /delete [id]")
            return

        # filter = {"_id": ObjectId(id), "user_id": update.message.from_user.id}
        streak = self.session.query(Streak).filter(
            Streak.id == id, Streak.user_id == uid
        )

        if streak.count() == 0:
            update.message.reply_text("Not found")
            log.warn(f"Could not delete reminder {id} for {getUserName(update)}")
            return

        try:
            streak = streak.first()
            when = streak.when
            title = streak.title
            self.session.delete(streak)
            self.session.commit()

            log.info(f"Deleted reminder {id} for {getUserName(update)}")
            update.message.reply_text(
                f'I will not remind you to "{title}" every {when} then.'
            )
        except Exception as e:
            self.session.rollback()
            log.error(f"Error deleting '{id}' for {getUserName(update)}: {e}")
            update.message.reply_text(f"Sorry, something went wrong.")

    ## /list
    ## Lists all streaks for the user
    def list(self, update, context):
        uid = update.message.from_user.id
        streaks = self.session.query(Streak).filter_by(user_id=uid)

        if streaks.count() > 0:
            log.info(
                f"Sending list of {streaks.count()} streaks to {getUserName(update)}"
            )
            message = ""
            for streak in streaks.all():
                message += f'Every {streak.when}: "{streak.title}" ({streak.id}).\n'
            update.message.reply_text(message)
        else:
            log.info(f"{getUserName(update)} has no remidners yet")
            update.message.reply_text("You don't have any reminders yet")

    ## /timezonme
    ## Sets timezone for user
    def timezone(self, update: Update, context):
        tz = update.message.text.replace("/timezone", "").strip()
        uid = update.message.from_user.id

        if tz == None or tz == "":
            update.message.reply_text("Correct format: /timezone [tz]")
            return

        try:
            user = self.session.query(User).get(uid) or User(id=uid)
            user.timezone = tz
            self.session.add(user)
            self.session.commit()

            log.info(f"Set TZ to {tz} for {getUserName(update)}")
            update.message.reply_text(f"Set your timezone to {tz}")
        except Exception as e:
            self.session.rollback()
            log.error(f"Error setting TZ to '{tz}' for {getUserName(update)}: {e}")
            update.message.reply_text(f"Sorry, something went wrong.")
