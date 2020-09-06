from telegram import Update


def getUserName(update: Update):
    return f"{update.message.from_user.username} ({update.message.from_user.id})"
