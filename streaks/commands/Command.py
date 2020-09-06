from telegram import Update


class Command:
    command = []

    def describe(bot, update: Update, context):
        pass

    def help(bot, update: Update, context):
        pass

    def run(bot, update: Update, context):
        pass
