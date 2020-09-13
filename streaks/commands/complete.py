from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from commands.Command import Command
from commands.info import Info
from utils.callbacks import CallbackKeys
from models.User import User
from models.Streak import Streak
from datetime import datetime, timedelta, time, timezone
from telegram import Update, ParseMode
import logging
import json

log = logging.getLogger(__name__)


def get_markup(streak: Streak):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
            f"📈 Current streak: {streak.count_streak}",
            callback_data=json.dumps(
                {
                    CallbackKeys.COMMAND.value: Info.command,
                    CallbackKeys.PAYLOAD.value: streak.id,
                }
            ),
        )]
    ])
class Complete(Command):
    command = "_c"

    def run(bot, update: Update, payload):
        query = update.callback_query
        streak_id = payload
        uid = query.message.chat.id
        streak = bot.session.query(Streak).filter(
            Streak.id == streak_id, Streak.user_id == uid
        )

        if streak.count() == 0:
            query.answer(text="Something went wrong.")
            log.warn(f"Could not complete for {streak_id} for {uid}")
            return

        streak = streak.first()

        if streak.last_track_date and streak.last_track_date > streak.prev_date:
            log.warn(
                f"Streak {streak_id} already tracked after it's been sent, ignoring"
            )
            query.answer(text="This has been already tracked")
            query.edit_message_text(
                text=f"<del>{query.message.text}</del>",
                parse_mode=ParseMode.HTML,
                reply_markup=get_markup(streak=streak),
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
            reply_markup=get_markup(streak=streak),
        )

        bot.session.add(streak)
        bot.session.commit()
