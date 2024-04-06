from database import Base
from sqlalchemy import  Column, Integer, String

class Robot(Base):
    __tablename__ = "robots"

    id = Column(Integer, primary_key=True, index=True)
    start_number = Column(Integer)
    start_time = Column(String)
    duration = Column(String)
