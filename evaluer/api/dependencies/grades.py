from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from evaluer.api.dependencies.weights import get_weight_provider
from evaluer.common.database.session import get_db_session
from evaluer.common.repositories.grading import (
    AssignmentGradeRepository,
    ModuleGradeRepository,
    OverallGradeRepository,
    ResponseGradeRepository,
    SubjectGradeRepository,
)
from evaluer.common.services.calculator import GradingCalculator
from evaluer.common.services.grades import GradeService
from evaluer.common.services.weights import WeightProvider

def get_grading_calculator() -> GradingCalculator:
    return GradingCalculator(base_score=10.0, minimum_score=2.0)


def get_response_grade_repo(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> ResponseGradeRepository:
    return ResponseGradeRepository(db)


def get_assignment_grade_repo(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> AssignmentGradeRepository:
    return AssignmentGradeRepository(db)


def get_module_grade_repo(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> ModuleGradeRepository:
    return ModuleGradeRepository(db)


def get_subject_grade_repo(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> SubjectGradeRepository:
    return SubjectGradeRepository(db)


def get_overall_grade_repo(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> OverallGradeRepository:
    return OverallGradeRepository(db)


def get_grade_service(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    weight_provider: Annotated[WeightProvider, Depends(get_weight_provider)],
    grading_calculator: Annotated[GradingCalculator, Depends(get_grading_calculator)],
    response_grade_repo: Annotated[
        ResponseGradeRepository, Depends(get_response_grade_repo)
    ],
    assignment_grade_repo: Annotated[
        AssignmentGradeRepository, Depends(get_assignment_grade_repo)
    ],
    module_grade_repo: Annotated[ModuleGradeRepository, Depends(get_module_grade_repo)],
    subject_grade_repo: Annotated[
        SubjectGradeRepository, Depends(get_subject_grade_repo)
    ],
    overall_grade_repo: Annotated[
        OverallGradeRepository, Depends(get_overall_grade_repo)
    ],
):
    return GradeService(
        db=db,
        weight_provider=weight_provider,
        grading_calculator=grading_calculator,
        response_grade_repo=response_grade_repo,
        assignment_grade_repo=assignment_grade_repo,
        module_grade_repo=module_grade_repo,
        subject_grade_repo=subject_grade_repo,
        overall_grade_repo=overall_grade_repo,
    )
