from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    PicklePersistence,
)

import logging

log = logging.getLogger(__name__)


class Bot:
    def __init__(self, args):
        log.info("Creating Bot...")
        self.pickle = PicklePersistence(filename="tinyCareBot")
        self.updater = Updater(args.botToken, persistence=self.pickle, use_context=True)

        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("help", self.start))

        self.updater.start_polling()
        log.info("Bot listening")
        self.updater.idle()

    def start(self, update, context):
        update.message.reply_text("Hi!")

