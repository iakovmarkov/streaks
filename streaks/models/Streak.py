from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from models.User import User
from datetime import date
from utils.Pattern import patterns
import uuid

Base = declarative_base()

##
# `when` is a string, can be:
# `[n]d`, like "1d", "4d" or "6d", days=[n], from 1 to 30
# `[weekday]`, like "monday", "tuesday" or "mon", "tue
# `[weekday,weekday,weekday]`, similar to weekday - multiple weekdays, separated by comma
##


class Streak(Base):
    __tablename__ = "streaks"

    id = Column(String, primary_key=True)
    title = Column(String)
    user_id = Column(String, ForeignKey(User.id))
    when = Column(String, default="1d")
    prev_date = Column(DateTime)
    next_date = Column(Date)
    last_track_date = Column(DateTime)
    count_total = Column(Integer, default=0)
    count_streak = Column(Integer, default=0)
    longest = Column(Integer, default=0)

    def __init__(self, title, when, user):
        self.id = uuid.uuid4().hex
        self.title = title
        self.when = when
        self.user_id = user
        self.prev_date = date.today()
        self.next_date = self.calc_next_date()

    def calc_next_date(self):
        for pattern in patterns:
            if pattern.test(self=pattern, pattern_string=self.when):
                return pattern.get_next(
                    self=pattern,
                    pattern_string=self.when,
                    date=self.next_date,
                )

        return self.next_date or date.today()


def init(engine):
    Base.metadata.create_all(engine)
