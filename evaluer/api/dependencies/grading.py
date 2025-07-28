from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from evaluer.core.database.session import get_db_session
from evaluer.repositories.grading import GradingRepository
from evaluer.services.grading import GradingService


def get_grading_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> GradingRepository:
    return GradingRepository(db_session)


def get_grading_service(
    grading_repository: Annotated[GradingRepository, Depends(get_grading_repository)]
) -> GradingService:
    return GradingService(grading_repository)
