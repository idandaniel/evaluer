from fastapi import APIRouter, Depends, HTTPException

from evaluer.api.dependencies.grades import get_grade_service
from evaluer.api.dependencies.hive import (
    HiveResourceValidation,
    get_hive_client,
    validate_hive_resources,
)
from evaluer.api.schemas.grades import UpdateAssignmentGradeRequest
from evaluer.common.clients.hive import HiveClient
from evaluer.common.models.hive import AssignmentResponseType
from evaluer.common.services.grades import GradeService

router = APIRouter(prefix="/grades", tags=["Grades"])


@router.put("/assignment")
async def update_student_assignment_response_grade(
    update_grade_request: UpdateAssignmentGradeRequest,
    grade_service: GradeService = Depends(get_grade_service),
    hive_client: HiveClient = Depends(get_hive_client),
):
    validate_hive_resources(
        request_dict=update_grade_request.model_dump(),
        hive_client=hive_client,
        validations=(
            HiveResourceValidation(resource_type="user", field_name="student_id"),
            HiveResourceValidation(resource_type="module", field_name="module_id"),
            HiveResourceValidation(resource_type="subject", field_name="subject_id"),
            HiveResourceValidation(
                resource_type="assignment", field_name="assignment_id"
            ),
            HiveResourceValidation(
                resource_type="assignment_response",
                field_name="response_id",
                depends_on={"assignment_id": "field:assignment_id"},
            ),
        ),
    )

    assignment_response = hive_client.get_assignment_response(
        assignment_id=update_grade_request.assignment_id,
        response_id=update_grade_request.response_id
    )
    if assignment_response.response_type != AssignmentResponseType.REDO:
        raise HTTPException(
            status_code=400, detail="Assignment response's type must be redo"
        )
    
    await grade_service.update_response_grade(**update_grade_request.model_dump())


@router.get(
    "/assignments/{assignment_id}/responses/{response_id}", response_model=float
)
async def get_student_assignment_response_grade(
    student_id: int,
    assignment_id: int,
    response_id: int,
    grade_service: GradeService = Depends(get_grade_service),
    hive_client: HiveClient = Depends(get_hive_client),
) -> float:
    validate_hive_resources(
        request_dict={
            "student_id": student_id,
            "response_id": response_id,
            "assignment_id": assignment_id,
        },
        hive_client=hive_client,
        validations=(
            HiveResourceValidation(resource_type="user", field_name="student_id"),
            HiveResourceValidation(
                resource_type="assignment", field_name="assignment_id"
            ),
            HiveResourceValidation(
                resource_type="assignment_response",
                field_name="response_id",
                depends_on={"assignment_id": "field:assignment_id"},
            ),
        ),
    )
    return await grade_service.get_assignment_response_grade(
        student_id=student_id, assignment_id=assignment_id, response_id=response_id
    )


@router.get("/assignments/{assignment_id}", response_model=float)
async def get_student_assignment_grade(
    student_id: int,
    assignment_id: int,
    grade_service: GradeService = Depends(get_grade_service),
    hive_client: HiveClient = Depends(get_hive_client),
) -> float:
    validate_hive_resources(
        request_dict={
            "student_id": student_id,
            "assignment_id": assignment_id,
        },
        hive_client=hive_client,
        validations=(
            HiveResourceValidation(resource_type="user", field_name="student_id"),
            HiveResourceValidation(
                resource_type="assignment", field_name="assignment_id"
            ),
        ),
    )
    return await grade_service.get_assignment_grade(
        student_id=student_id, assignment_id=assignment_id
    )


@router.get("/modules", response_model=float)
async def get_student_module_grade(
    student_id: int,
    module_id: int,
    grade_service: GradeService = Depends(get_grade_service),
    hive_client: HiveClient = Depends(get_hive_client),
) -> float:
    validate_hive_resources(
        request_dict={"student_id": student_id, "module_id": module_id},
        hive_client=hive_client,
        validations=(
            HiveResourceValidation(resource_type="user", field_name="student_id"),
            HiveResourceValidation(resource_type="module", field_name="module_id"),
        ),
    )
    return await grade_service.get_module_grade(
        student_id=student_id, module_id=module_id
    )


@router.get("/overall", response_model=float)
async def get_student_overall_grade(
    student_id: int,
    grade_service: GradeService = Depends(get_grade_service),
    hive_client: HiveClient = Depends(get_hive_client),
) -> float:
    validate_hive_resources(
        request_dict={"student_id": student_id},
        hive_client=hive_client,
        validations=(
            HiveResourceValidation(resource_type="user", field_name="student_id"),
        ),
    )
    return await grade_service.get_overall_grade(student_id=student_id)
