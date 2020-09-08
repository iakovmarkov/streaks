from telegram.ext import (
    Updater,
    CallbackQueryHandler,
    CommandHandler,
)
from telegram import Update
from sqlalchemy.orm import Session
from models.User import User
from models.Streak import Streak
from utils.get_username import get_username
from utils.callbacks import CallbackKeys
from datetime import datetime, timedelta, time, timezone
import json
import logging
from commands import commands
from commands.Command import Command
import re

log = logging.getLogger(__name__)
nl = "\n"  # Python, why won't you allow this in the f-string?


def clean_message(update: Update):
    text = update.message.text
    match = re.search(r"(\/\w+) (.+)", text)
    if match:
        return match.group(2).strip()
    else:
        return text


class Bot:
    def __init__(self, args, session: Session):
        log.info("Creating Bot...")
        self.session = session
        self.updater = Updater(args.bot_token, use_context=True)

        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("help", self.help))
        self.register(dispatcher, commands.Create)
        self.register(dispatcher, commands.List)
        self.register(dispatcher, commands.Timezone)
        dispatcher.add_handler(CallbackQueryHandler(self.callback_handler))

        self.updater.start_polling()
        log.info("Bot listening")
        self.updater.idle()

    def handle(self, command: Command):
        return lambda update, context: command.run(
            bot=self, update=update, context=context
        )

    def register(self, dispatcher, command: Command):
        dispatcher.add_handler(CommandHandler(command.command, self.handle(command)))

    def start(self, update, context):
        lines = [
            "Hi. I am Streaks Bot.",
            "My purpose is to help you build new habits. You can add new habits using /create command. I will send you periodicall reminders, and you will mark them as done once you finish them.",
            "The reminder system is very flexible. You can create reminders for every N days, or schedule them on weekdays. Once a week you will receive a summary of your activity.",
            "To see a list of all commands, send /help. You also should send timezone - send /timezone.",
            "Remember - try to keep the number of goals small (under five), and the tasks themselves easily doable. This will help you build habits that last.",
        ]
        update.message.reply_text(f"{nl}{nl}".join(lines))

    def help(self, update, context):
        descr = []
        args = clean_message(update)

        command_list = [commands.Create, commands.List, commands.Timezone]

        if args:
            for command in command_list:
                if command.command == args:
                    update.message.reply_text(
                        command.help(bot=self, update=update, context=context)
                    )
                    return

        for command in command_list:
            descr.append(
                f"/{command.command} - {command.describe(bot=self, update=update, context=context)}"
            )

        update.message.reply_text(
            f"I know the following commands:{nl}{nl.join(descr)}{nl}To get more help, type `/help command`."
        )

    def callback_handler(self, update: Update, context):
        query = update.callback_query

        try:
            callback_data = json.loads(query.data)
            command = callback_data[CallbackKeys.COMMAND.value]
            payload = callback_data[CallbackKeys.PAYLOAD.value]

            if command == commands.Complete.command:
                commands.Complete.run(bot=self, update=update, payload=payload)
            elif command == commands.Delete.command:
                commands.Delete.run(bot=self, update=update, payload=payload)
            elif command == commands.Info.command:
                commands.Info.run(bot=self, update=update, payload=payload)
            else:
                log.warn(
                    f"Could not find handler for callback: {command} - {payload} from {get_username(update)}"
                )

        except Exception as e:
            self.session.rollback()
            log.error(
                f"Error handling command {command} from {get_username(update)}: {e}"
            )
            query.answer(text="Something went wrong.")
