from sqlalchemy import Column, Float, Integer, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class ResponseGrade(Base):
    __tablename__ = "response_grades"
    __table_args__ = (
        UniqueConstraint(
            "response_id", "student_id", name="uq_response_grades_response_student"
        ),
    )

    id = Column(Integer, primary_key=True)
    response_id = Column(Integer, nullable=False, index=True)
    assignment_id = Column(Integer, nullable=False, index=True)
    student_id = Column(Integer, nullable=False, index=True)
    grade = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AssignmentGrade(Base):
    __tablename__ = "assignment_grades"
    __table_args__ = (
        UniqueConstraint(
            "assignment_id",
            "student_id",
            name="uq_assignment_grades_assignment_student",
        ),
    )

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, nullable=False, index=True)
    module_id = Column(Integer, nullable=False, index=True)
    student_id = Column(Integer, nullable=False, index=True)
    grade = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ModuleGrade(Base):
    __tablename__ = "module_grades"
    __table_args__ = (
        UniqueConstraint(
            "module_id", "student_id", name="uq_module_grades_module_student"
        ),
    )

    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, nullable=False, index=True)
    subject_id = Column(Integer, nullable=False, index=True)
    student_id = Column(Integer, nullable=False, index=True)
    grade = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SubjectGrade(Base):
    __tablename__ = "subject_grades"
    __table_args__ = (
        UniqueConstraint(
            "subject_id", "student_id", name="uq_subject_grades_subject_student"
        ),
    )

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, nullable=False, index=True)
    student_id = Column(Integer, nullable=False, index=True)
    grade = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class OverallGrade(Base):
    __tablename__ = "overall_grades"
    __table_args__ = (UniqueConstraint("student_id", name="uq_overall_grades_student"),)

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False, index=True)
    grade = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
