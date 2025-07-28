from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends

from evaluer.clients.hive import HiveClient
from evaluer.services.hive import HiveService
from evaluer.services.grading import GradingService
from evaluer.dependencies.hive import get_authenticated_hive_client, get_hive_service
from evaluer.dependencies.grading import get_grading_service
from evaluer.models.api import (
    AssignmentDetail,
    AssignmentResponseWithGrade,
    UpdateGradeRequest,
)
from evaluer.models.hive import (
    AssignmentResponseType, 
    CourseUser, 
    ClearanceLevel,
    AssignmentResponseFiles,
)

router = APIRouter(tags=["Students"])


@router.get("/students", response_model=List[CourseUser])
def get_all_students(
    hive_service: HiveService = Depends(get_hive_service),
) -> List[CourseUser]:
    students = hive_service.get_users_by_clearance(clearance=ClearanceLevel.HANICH)
    return students


@router.get(
    "/students/{student_id}/assignments/{exercise_id}", response_model=AssignmentDetail
)
async def get_assignment_with_grades(
    student_id: int,
    exercise_id: int,
    hive_service: HiveService = Depends(get_hive_service),
    grading_service: GradingService = Depends(get_grading_service),
) -> AssignmentDetail:
    assignment = hive_service.get_student_assignment_by_exercise(
        student_id=student_id, exercise_id=exercise_id
    )

    if not assignment:
        raise HTTPException(
            status_code=404, detail="Assignment not found for this student"
        )

    responses = hive_service.get_assignment_responses(assignment_id=assignment.id)
    response_grades_db = await grading_service.get_all_response_grades()

    responses_with_grades = [
        AssignmentResponseWithGrade(
            id=response.id,
            response_type=response.response_type,
            content=response.contents[0].content if response.contents else "",
            grade=response_grades_db.get(response.id, 0),  # Default to 0 if no grade found
        )
        for response in responses
    ]

    total_grade = await grading_service.calculate_assignment_grade(responses)

    return AssignmentDetail(
        assignment_id=assignment.id,
        responses=responses_with_grades,
        total_grade=total_grade,
    )


@router.put(
    "/students/{student_id}/assignments/{assignment_id}/responses/{response_id}/grade"
)
async def update_response_grade(
    student_id: int,
    assignment_id: int,
    response_id: int,
    request: UpdateGradeRequest,
    hive_client: HiveClient = Depends(get_authenticated_hive_client),
    grading_service: GradingService = Depends(get_grading_service),
) -> Dict[str, str]:
    assignment = hive_client.get_student_assignment(
        student_id=student_id, assignment_id=assignment_id
    )

    if not assignment:
        raise HTTPException(
            status_code=404, detail="Assignment not found for this student"
        )

    responses = hive_client.get_assignment_responses(assignment_id=assignment_id)
    response = next((r for r in responses if r.id == response_id), None)

    if not response:
        raise HTTPException(
            status_code=404, detail="Response not found for this assignment"
        )

    if response.response_type != AssignmentResponseType.REDO:
        raise HTTPException(
            status_code=400, detail="Grade can only be updated for redo responses"
        )

    await grading_service.set_response_grade(response_id, request.grade)
    
    return {"message": "Grade updated successfully"}


@router.get(
    "/students/{student_id}/assignments/{assignment_id}/responses/{response_id}/files",
    response_model=AssignmentResponseFiles,
)
def get_student_assignment_response_files(
    student_id: int,
    assignment_id: int,
    response_id: int,
    hive_service: HiveService = Depends(get_hive_service),
) -> AssignmentResponseFiles:
    # Get the response to extract the filename
    responses = hive_service.get_assignment_responses(assignment_id=assignment_id)
    response = next((r for r in responses if r.id == response_id), None)
    response_filename = response.file_name if response else None
    
    return hive_service.get_assignment_response_files(
        assignment_id=assignment_id, response_id=response_id, response_filename=response_filename
    )
