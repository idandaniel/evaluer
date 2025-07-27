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
    dear_student: bool = True
    date: datetime
    hide_checker_name: bool = False
    segel_only: bool = False
    response_type: AssignmentResponseType
    autocheck_statuses: Optional[List[Any]] = None


class Assignment(BaseModel):
    id: int
    user: int
    checker: Optional[int] = None
    checker_first_name: Optional[str] = None
    checker_last_name: Optional[str] = None
    is_subscribed: Optional[bool] = None
    exercise: int
    assignment_status: AssignmentStatus = AssignmentStatus.NEW
    student_assignment_status: AssignmentStatus = AssignmentStatus.NEW
    patbas: Optional[bool] = None
    description: Optional[str] = None
    submission_count: int = 0
    total_check_count: int = 0
    manual_check_count: int = 0
    notifications: List[Any] = []
    last_staff_updated: Optional[datetime] = None
    flagged: bool = False
    work_time: Optional[int] = None
    timer: Optional[str] = None


class Exercise(BaseModel):
    id: int
    name: str
    parent_module: int


class CourseTokenObtainPair(BaseModel):
    access: str
    refresh: str


class CourseTokenObtainPairRequest(BaseModel):
    username: str
    password: str


class TokenRefresh(BaseModel):
    access: str
    refresh: str


class CourseUser(BaseModel):
    id: int
    display_name: str
    clearance: int
    avatar_filename: Optional[str] = None
    gender: Optional[str] = None
    number: Optional[int] = None
    program: Optional[int] = None
    checkers_brief: Optional[str] = None
    current_assignment: Optional[int] = None
    current_assignment_options: List[int] = []
    mentor: Optional[int] = None
    classes: List[int] = []
    mentees: List[int] = []
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[str] = None
    status_date: Optional[datetime] = None
    queue: Optional[int] = None
    disable_queue: Optional[bool] = None
    user_queue: Optional[int] = None
    disable_user_queue: Optional[bool] = None
    override_queue: Optional[int] = None
    confirmed: Optional[bool] = None
    teacher: Optional[bool] = None
    hostname: Optional[str] = None