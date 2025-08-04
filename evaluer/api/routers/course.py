from typing import List

from fastapi import Depends, APIRouter

from evaluer.api.dependencies.hive import get_hive_client
from evaluer.common.clients.hive import HiveClient
from evaluer.common.models.hive import (
    AssignmentResponse,
    AssignmentResponseFiles,
    ClearanceLevel,
)

router = APIRouter(prefix="/course", tags=["Course"])


@router.get("/subjects")
def get_course_subjects(
    hive_client: HiveClient = Depends(get_hive_client),
):
    return hive_client.get_subjects()


@router.get("/students")
def get_course_students(
    hive_client: HiveClient = Depends(get_hive_client),
):
    return hive_client.get_users_by_clearance(ClearanceLevel.HANICH)


@router.get("/modules")
def get_course_modules_by_subject(
    subject_id: int, hive_client: HiveClient = Depends(get_hive_client)
):
    return hive_client.get_modules_by_subject(subject_id=subject_id)


@router.get("/exercises")
def get_course_exercises_by_module(
    module_id: int, hive_client: HiveClient = Depends(get_hive_client)
):
    return hive_client.get_exercises_by_module(module_id=module_id)


@router.get("/assignments")
def get_course_assignments_by_module(
    exercise_id: int,
    student_id: int,
    hive_client: HiveClient = Depends(get_hive_client),
):
    return hive_client.get_student_assignment_by_exercise(
        exercise_id=exercise_id, student_id=student_id
    )


@router.get("/assignments/{assignment_id}/responses")
def get_course_assignment_responses(
    assignment_id: int,
    hive_client: HiveClient = Depends(get_hive_client),
) -> List[AssignmentResponse]:
    return hive_client.get_assignment_responses(assignment_id=assignment_id)


@router.get(
    "/assignments/{assignment_id}/responses/{response_id}/files",
    response_model=AssignmentResponseFiles,
)
def get_assignment_response_files(
    assignment_id: int,
    response_id: int,
    hive_client: HiveClient = Depends(get_hive_client),
) -> AssignmentResponseFiles:
    return hive_client.get_assignment_response_files(
        assignment_id=assignment_id,
        response_id=response_id,
    )
