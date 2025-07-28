from typing import Dict, List

from evaluer.models.hive import AssignmentResponse, AssignmentResponseType
from evaluer.repositories.grading import GradingRepository

BASE_SCORE = 10
REDO_PENALTY_FACTOR = 0.9
MINIMUM_SCORE = 3


class GradingService:
    def __init__(self, grading_repository: GradingRepository) -> None:
        self._grading_repository = grading_repository

    async def set_response_grade(self, response_id: int, grade: int) -> None:
        await self._grading_repository.save_response_grade(response_id, grade)

    async def get_response_grade(self, response_id: int) -> int:
        grade = await self._grading_repository.get_response_grade(response_id)
        return grade if grade is not None else 0

    async def get_all_response_grades(self) -> Dict[int, int]:
        return await self._grading_repository.get_all_response_grades()

    async def calculate_assignment_grade(self, responses: List[AssignmentResponse]) -> float:
        redo_responses = [
            response
            for response in responses
            if response.response_type == AssignmentResponseType.REDO
        ]

        is_completed = any(
            response.response_type == AssignmentResponseType.DONE for response in responses
        )

        if not is_completed:
            return 0

        if not redo_responses:
            return BASE_SCORE

        response_ids = [response.id for response in redo_responses]
        response_grades = await self._grading_repository.get_response_grades_by_ids(response_ids)

        total_weighted_score = 0.0
        total_weight = 0.0
        
        for redo_count, response in enumerate(redo_responses):
            response_grade = response_grades.get(response.id, 0)  # Default to 0 if no grade found
            
            weight = 1.0 / (2 ** redo_count)
            weighted_score = response_grade * weight
            
            total_weighted_score += weighted_score
            total_weight += weight
        
        weighted_average = total_weighted_score / total_weight if total_weight > 0 else 0
        final_score = weighted_average * REDO_PENALTY_FACTOR
        
        return max(final_score, MINIMUM_SCORE)
