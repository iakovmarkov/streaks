from telegram import Update
from enum import Enum
import datetime
import re


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


def next_weekday(date, weekday: Weekday):
    days_ahead = weekday - date.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return date + datetime.timedelta(days_ahead)


class Pattern:
    def test(self, pattern_string: str):
        pass

    def get_next(self, pattern_string: str, date):
        pass


class PatternRegular(Pattern):
    def test(self, pattern_string: str):
        return re.search(r"\d[d]", pattern_string)

    def get_next(self, pattern_string: str, date):
        if date is None:
            return datetime.datetime.now()
        days = re.search(r"\d", pattern_string.lower()).group()
        return date + datetime.timedelta(days=int(days))


class PatternWeekday(Pattern):
    def test(self, pattern_string: str):
        return to_weekday(pattern_string)

    def get_next(self, pattern_string: str, date):
        return next_weekday(datetime.date.today(), to_weekday(pattern_string).value)


class PatternWeekdayList(Pattern):
    def test(self, pattern_string: str):
        parts = pattern_string.split(",")
        if len(parts) > 1:
            for part in parts:
                if to_weekday(part) == None:
                    return False
            return True
        else:
            return False

    def get_next(self, pattern_string: str, date):
        parts = pattern_string.split(",")
        today = datetime.date.today()
        closest_next = datetime.date.today() + datetime.timedelta(days=7)

        for part in parts:
            part_next = next_weekday(today, to_weekday(part).value)
            if closest_next > part_next:
                closest_next = part_next

        return closest_next


patterns = [PatternRegular, PatternWeekday, PatternWeekdayList]


def getUserName(update: Update):
    return f"{update.message.from_user.username} ({update.message.from_user.id})"
