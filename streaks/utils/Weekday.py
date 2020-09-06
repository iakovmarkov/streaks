from telegram import Update
from enum import Enum
import datetime


class Weekday(Enum):
    MONDAY = 0
    MON = 0
    TUESDAY = 1
    TUE = 1
    WEDNESDAY = 2
    WED = 2
    THURSDAY = 3
    THU = 3
    FRIDAY = 4
    FRI = 4
    SATURDAY = 5
    SAT = 5
    SUNDAY = 6
    SUN = 6

    def to_weekday(string: str):
        try:
            weekday = Weekday[string.upper()]
            return weekday
        except Exception:
            return None

    def next_weekday(date, weekday):
        days_ahead = weekday - date.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return date + datetime.timedelta(days_ahead)
