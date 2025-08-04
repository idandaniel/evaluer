import math
from typing import Dict


class GradingCalculator:
    def __init__(
        self,
        base_score: float = 10.0,
        minimum_score: float = 2.0,
    ):
        self._base_score = base_score
        self._minimum_score = minimum_score

    def calculate_assignment_grade(self, response_grades: Dict[int, float]) -> float:
        if not response_grades:
            return 0.0

        redo_grades = [
            # First index is 0, log(1) = 1, so we start at 2
            max(response.grade - math.log(index + 2), self._minimum_score)
            for index, response in enumerate(response_grades)
        ]
        weighted_grade = 0 if not redo_grades else sum(redo_grades) / len(redo_grades)
        return weighted_grade

    def calculate_weighted_average(
        self, grades_by_id: Dict[int, float], weights_by_id: Dict[int, float]
    ) -> float:
        if not grades_by_id:
            return 0.0

        total_weighted_score = 0.0
        total_weight = 0.0

        for item_id, grade in grades_by_id.items():
            weight = weights_by_id.get(item_id, 1.0)
            total_weighted_score += grade * weight
            total_weight += weight

        return total_weighted_score / total_weight if total_weight > 0 else 0.0
