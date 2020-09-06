from commands.Command import Command
from models.User import User
from models.Streak import Streak
from datetime import datetime, timedelta, time, timezone
from telegram import Update, ParseMode
import logging

log = logging.getLogger(__name__)


class Complete(Command):
    command = "_c"

    def run(bot, update: Update, payload):
        query = update.callback_query
        streak_id = payload
        streak = bot.session.query(Streak).get(streak_id)

        if streak.last_track_date and streak.last_track_date > streak.prev_date:
            log.warn(
                f"Streak {streak_id} already tracked after it's been sent, ignoring"
            )
            query.answer(text="This has been already tracked")
            query.edit_message_text(
                text=f"<del>{query.message.text}</del>",
                parse_mode=ParseMode.HTML,
                reply_markup=None,
            )
            return

        streak.last_track_date = datetime.now()
        streak.count_total += 1

        if streak.prev_date > datetime.now() - timedelta(hours=23, minutes=45):
            streak.count_streak += 1

            if streak.count_streak > streak.longest:
                streak.longest = streak.count_streak

            log.info(
                f"Tracking {streak_id}. {streak.count_streak} times, total {streak.count_total}."
            )
            query.answer(text="✅ Done!")
        else:
            streak.count_streak = 1
            log.info(f"Reset {streak_id} to 1.")
            query.answer(
                text=f"Looks like you've lost your streak of {streak.count_streak}. Starting from beginning."
            )
        query.edit_message_text(
            text=f"✅ <del>{query.message.text}</del>",
            parse_mode=ParseMode.HTML,
            reply_markup=None,
        )

        bot.session.add(streak)
        bot.session.commit()
