from sqlalchemy import Column, Integer, String
from database import Base


class Candidate(Base):

    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    skills = Column(String)

    match_score = Column(Integer)