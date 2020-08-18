from datetime import datetime
from ReminderTimeslot import ReminderTimeslot

def sendMessages(db):
    morningUsers = db.users.find_one()
    print(morningUsers)
    print(datetime.utcnow().hour)