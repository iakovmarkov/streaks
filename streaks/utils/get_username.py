from telegram import Update


def get_username(update: Update):
    try:
        return f"{update.message.from_user.username} ({update.message.from_user.id})"
    except Exception:
        return ""
