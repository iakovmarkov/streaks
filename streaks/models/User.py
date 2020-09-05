from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import time

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    timezone = Column(Integer, default=0)
    morning_time = Column(Time, default=time(9, 0))
    evening_time = Column(Time, default=time(22, 00))


def init(engine):
    Base.metadata.create_all(engine)
