from telegram import Update
from enum import Enum
from utils.Weekday import Weekday
import datetime
import re


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
        return Weekday.to_weekday(pattern_string)

    def get_next(self, pattern_string: str, date):
        return Weekday.next_weekday(
            datetime.date.today(), Weekday.to_weekday(pattern_string).value
        )


class PatternWeekdayList(Pattern):
    def test(self, pattern_string: str):
        parts = pattern_string.split(",")
        if len(parts) > 1:
            for part in parts:
                if Weekday.to_weekday(part) == None:
                    return False
            return True
        else:
            return False

    def get_next(self, pattern_string: str, date):
        parts = pattern_string.split(",")
        today = datetime.date.today()
        closest_next = datetime.date.today() + datetime.timedelta(days=7)

        for part in parts:
            part_next = Weekday.next_weekday(today, Weekday.to_weekday(part).value)
            if closest_next > part_next:
                closest_next = part_next

        return closest_next


patterns = [PatternRegular, PatternWeekday, PatternWeekdayList]
