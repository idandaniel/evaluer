from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class ResponseGrade(Base):
    __tablename__ = "response_grades"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, unique=True, nullable=False, index=True)
    grade = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
