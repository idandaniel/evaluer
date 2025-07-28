from typing import Dict, List

from evaluer.models.hive import AssignmentResponse, AssignmentResponseType

BASE_SCORE = 10
DEFAULT_REDO_PENALTY = 1
PENALTY_EXPONENT = 1.5
MAX_TOTAL_PENALTY = 6
MINIMUM_SCORE = 3


class GradingService:
    def __init__(self) -> None:
        self._response_grades: Dict[int, int] = {}

    def set_response_grade(self, response_id: int, grade: int) -> None:
        self._response_grades[response_id] = grade

    def get_response_grade(self, response_id: int) -> int:
        return self._response_grades.get(response_id, DEFAULT_REDO_PENALTY)

    def get_all_response_grades(self) -> Dict[int, int]:
        return self._response_grades.copy()

    def calculate_assignment_grade(self, responses: List[AssignmentResponse]) -> float:
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

        num_redos = len(redo_responses)
        total_penalty = num_redos**PENALTY_EXPONENT

        capped_penalty = min(total_penalty, MAX_TOTAL_PENALTY)
        final_score = BASE_SCORE - capped_penalty

        return max(final_score, MINIMUM_SCORE)
