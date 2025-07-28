from functools import lru_cache

from evaluer.services.grading import GradingService


@lru_cache()
def get_grading_service() -> GradingService:
    return GradingService()
