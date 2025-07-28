from typing import List
from fastapi import APIRouter, Depends

from evaluer.services.hive import HiveService
from evaluer.api.dependencies.hive import get_hive_service
from evaluer.core.models.hive import Module, Exercise

router = APIRouter(tags=["Modules"])


@router.get("/subjects/{subject_id}/modules", response_model=List[Module])
def get_modules_by_subject(
    subject_id: int,
    hive_service: HiveService = Depends(get_hive_service),
) -> List[Module]:
    return hive_service.get_modules_by_subject(subject_id)


@router.get("/modules/{module_id}/exercises", response_model=List[Exercise])
def get_exercises_by_module(
    module_id: int,
    hive_service: HiveService = Depends(get_hive_service),
) -> List[Exercise]:
    return hive_service.get_exercises_by_module(module_id)
