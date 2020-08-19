from datetime import datetime
from ReminderTimeslot import ReminderTimeslot
from telegram.bot import Bot
import logging

log = logging.getLogger(__name__)

reminderTimes = {
    ReminderTimeslot.MORNING: 8,
    ReminderTimeslot.AFTERNOON: 15,
    ReminderTimeslot.EVENING: 22,
}

def sendMessages(args, db):
    currentHour = datetime.utcnow().hour
    log.info(f'Running sendMessages, current hour is {currentHour} GMT')
    bot = Bot(args.botToken)

    for timeSlot in reminderTimes:
        time = reminderTimes.get(timeSlot)
        tz = currentHour - time
        filter = { "tz": tz }
        timeslotUsers = db.users.find(filter)
        log.info(f'Processing messages for {timeSlot.value} ({reminderTimes.get(timeSlot)}), will send to {db.users.count_documents(filter)} users with timezone {tz}')

        for user in timeslotUsers:
            filter = { "user_id": user["user_id"], "when": timeSlot.value }
            reminders = db.reminders.find(filter)
            for reminder in reminders:
                bot.send_message(
                    chat_id = reminder["user_id"],
                    text = reminder["text"]
                )