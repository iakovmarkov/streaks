from commands.Command import Command
from models.User import User
from models.Streak import Streak
from utils.getUserName import getUserName
import logging

log = logging.getLogger(__name__)


class Create(Command):
    command = "create"

    def describe(bot, update, context):
        return "[pattern] [text] - create a new goal to track. See `/help create` for more."

    def help(bot, update, context):
        return "[pattern] [text] - create a new goal to track"

    def run(bot, update, context):
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
        user = bot.session.query(User).get(uid) or User(id=uid)
        streak = Streak(title=text, user=uid, when=when)

        bot.session.add_all([user, streak])
        bot.session.commit()

        log.info(
            f"Saved streak ({streak.id}): {when} {text} from {getUserName(update)}"
        )
        update.message.reply_text(f'Will remind you "{text}" every {when}')
