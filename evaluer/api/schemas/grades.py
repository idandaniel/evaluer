from pydantic import BaseModel, Field


class UpdateAssignmentGradeRequest(BaseModel):
    student_id: int
    response_id: int
    assignment_id: int
    module_id: int
    subject_id: int
    new_grade: float = Field(ge=1, le=10, description="Grade must be between 1 and 10")
