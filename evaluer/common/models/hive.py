from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel


class FileInfo(BaseModel):
    name: str
    size: int
    content: str
    mime_type: str = "application/octet-stream"


class AssignmentResponseFiles(BaseModel):
    response_id: int
    files: List[FileInfo] = []
    has_files: bool = False
    total_size: int = 0


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
    assignment_id: int
    contents: List[AssignmentResponseContent]
    file_name: Optional[str] = None
    date: datetime
    response_type: AssignmentResponseType
    autocheck_statuses: Optional[List[Any]] = None


class Assignment(BaseModel):
    id: int
    user: int
    exercise: int
    assignment_status: Optional[AssignmentStatus] = AssignmentStatus.NEW
    student_assignment_status: Optional[AssignmentStatus] = AssignmentStatus.NEW
    patbas: Optional[bool] = None
    description: Optional[str] = None
    submission_count: int = 0
    total_check_count: int = 0
    manual_check_count: int = 0

    @property
    def exercise_id(self) -> int:
        return self.exercise


class BaseCourseComponent(BaseModel):
    id: int
    name: str


class Subject(BaseCourseComponent):
    pass


class Module(BaseCourseComponent):
    parent_subject: int

    @property
    def subject_id(self) -> int:
        return self.parent_subject


class Exercise(BaseCourseComponent):
    parent_module: int

    @property
    def module_id(self) -> int:
        return self.parent_module


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
