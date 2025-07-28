from typing import List
from fastapi import APIRouter, Depends

from evaluer.services.hive import HiveService
from evaluer.api.dependencies.hive import get_hive_service
from evaluer.core.models.hive import Subject

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get("", response_model=List[Subject])
def get_all_subjects(
    hive_service: HiveService = Depends(get_hive_service),
) -> List[Subject]:
    return hive_service.get_subjects()
