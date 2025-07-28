from typing import List
from pydantic import BaseModel, Field

from evaluer.models.hive import AssignmentResponseType


class AssignmentResponseWithGrade(BaseModel):
    id: int
    response_type: AssignmentResponseType
    content: str
    grade: float


class AssignmentDetail(BaseModel):
    assignment_id: int
    responses: List[AssignmentResponseWithGrade]
    total_grade: float


class UpdateGradeRequest(BaseModel):
    grade: float = Field(ge=1, le=10, description="Grade must be between 1 and 10")
