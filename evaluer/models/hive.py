from typing import Any, List, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class AssignmentStatus(str, Enum):
    NEW = "New"
    WORK_IN_PROGRESS = "Work In Progress"
    REDO = "Redo"
    SUBMITTED = "Submitted"
    AUTO_CHECKED = "AutoChecked"
    DONE = "Done"


class AssignmentResponseType(str, Enum):
    COMMENT = "Comment"
    WORK_IN_PROGRESS = "Work In Progress"
    SUBMISSION = "Submission"
    AUTO_CHECK = "AutoCheck"
    REDO = "Redo"
    DONE = "Done"


class ClearanceLevel(int, Enum):
    HANICH = 1
    CHECKER = 2
    SEGEL = 3
    ADMIN = 5


class AssignmentResponseContent(BaseModel):
    content: str
    field: int


class AssignmentResponse(BaseModel):
    id: int
    user: int
    contents: List[AssignmentResponseContent]
    file_name: Optional[str] = None
    date: datetime
    response_type: AssignmentResponseType
    autocheck_statuses: Optional[List[Any]] = None


class Assignment(BaseModel):
    id: int
    user: int
    exercise: int
    assignment_status: AssignmentStatus = AssignmentStatus.NEW
    student_assignment_status: AssignmentStatus = AssignmentStatus.NEW
    patbas: Optional[bool] = None
    description: Optional[str] = None
    submission_count: int = 0
    total_check_count: int = 0
    manual_check_count: int = 0


class BaseCourseComponent(BaseModel):
    id: int
    name: str


class Subject(BaseCourseComponent):
    pass


class Module(BaseCourseComponent):
    pass


class Exercise(BaseCourseComponent):
    pass
    parent_module: int


class TokenObtainResponse(BaseModel):
    access: str
    refresh: str


class TokenObtainRequest(BaseModel):
    username: str
    password: str


class CourseUser(BaseModel):
    id: int
    display_name: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
