from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from evaluer.common.repositories.grading import (
    AssignmentGradeRepository,
    ModuleGradeRepository,
    OverallGradeRepository,
    ResponseGradeRepository,
    SubjectGradeRepository,
)
from evaluer.common.services.calculator import GradingCalculator
from evaluer.common.services.weights import WeightProvider


class GradeProtocol(Protocol):
    grade: float


class WeightedGradeProtocol(Protocol):
    grade: float
    subject_id: int | None = None
    module_id: int | None = None
    assignment_id: int | None = None


class GradeService:
    def __init__(
        self,
        db: AsyncSession,
        weight_provider: WeightProvider,
        grading_calculator: GradingCalculator,
        response_grade_repo: ResponseGradeRepository,
        assignment_grade_repo: AssignmentGradeRepository,
        module_grade_repo: ModuleGradeRepository,
        subject_grade_repo: SubjectGradeRepository,
        overall_grade_repo: OverallGradeRepository,
    ):
        self.db = db
        self._weight_provider = weight_provider
        self._grading_calculator = grading_calculator
        self._response_grade_repo = response_grade_repo
        self._assignment_grade_repo = assignment_grade_repo
        self._module_grade_repo = module_grade_repo
        self._subject_grade_repo = subject_grade_repo
        self._overall_grade_repo = overall_grade_repo

    async def update_response_grade(
        self,
        student_id: int,
        response_id: int,
        assignment_id: int,
        module_id: int,
        subject_id: int,
        new_grade: float,
    ):
        await self._response_grade_repo.upsert(
            student_id=student_id,
            response_id=response_id,
            assignment_id=assignment_id,
            grade=new_grade,
        )
        await self.recalculate_assignment_grade(
            student_id=student_id,
            assignment_id=assignment_id,
            module_id=module_id,
            subject_id=subject_id,
        )

    async def recalculate_assignment_grade(
        self, student_id: int, assignment_id: int, module_id: int, subject_id: int
    ):
        response_grades = await self._response_grade_repo.get_all_for_assignment(
            student_id=student_id, assignment_id=assignment_id
        )
        grade = self._grading_calculator.calculate_assignment_grade(
            response_grades=response_grades
        )
        await self._assignment_grade_repo.upsert(
            student_id=student_id,
            assignment_id=assignment_id,
            module_id=module_id,
            grade=grade,
        )
        await self.recalculate_module_grade(student_id, module_id, subject_id)

    async def recalculate_module_grade(
        self, student_id: int, module_id: int, subject_id: int
    ):
        assignments = await self._assignment_grade_repo.get_all_for_module(
            module_id=module_id, student_id=student_id
        )
        assignment_grades = {
            assignment.assignment_id: assignment.grade for assignment in assignments
        }
        weights = self._weight_provider.get_weights_for_items(
            "exercise", list(assignment_grades.keys())
        )
        grade = self._grading_calculator.calculate_weighted_average(
            grades_by_id=assignment_grades, weights_by_id=weights
        )
        print(f"Module grade: {grade}")
        await self._module_grade_repo.upsert(
            student_id=student_id,
            module_id=module_id,
            subject_id=subject_id,
            grade=grade,
        )
        await self.recalculate_subject_grade(student_id, subject_id)

    async def recalculate_subject_grade(self, student_id: int, subject_id: int):
        modules = await self._module_grade_repo.get_all_for_subject(
            subject_id=subject_id, student_id=student_id
        )
        module_grades = {module.module_id: module.grade for module in modules}
        weights = self._weight_provider.get_weights_for_items(
            "module", list(module_grades.keys())
        )
        grade = self._grading_calculator.calculate_weighted_average(
            grades_by_id=module_grades, weights_by_id=weights
        )
        await self._subject_grade_repo.upsert(
            student_id=student_id, subject_id=subject_id, grade=grade
        )
        await self.recalculate_overall_grade(student_id)

    async def recalculate_overall_grade(self, student_id: int):
        subjects = await self._subject_grade_repo.get_all_for_student(
            student_id=student_id
        )
        subject_grades = {subject.subject_id: subject.grade for subject in subjects}
        subject_ids = list(subject_grades.keys())
        weights = self._weight_provider.get_weights_for_items("subject", subject_ids)
        grade = self._grading_calculator.calculate_weighted_average(
            grades_by_id=subject_grades, weights_by_id=weights
        )
        await self._overall_grade_repo.upsert(student_id=student_id, grade=grade)

    async def get_assignment_response_grade(
        self, student_id: int, assignment_id: int, response_id: int
    ) -> float:
        return await self._response_grade_repo.get_grade(
            student_id=student_id, assignment_id=assignment_id, response_id=response_id
        )

    async def get_assignment_grade(self, student_id: int, assignment_id: int) -> float:
        result = await self._assignment_grade_repo.get_grade(
            student_id=student_id, assignment_id=assignment_id
        )
        return result if result is not None else 0.0

    async def get_module_grade(self, student_id: int, module_id: int) -> float:
        return await self._module_grade_repo.get_grade(
            student_id=student_id, module_id=module_id
        )

    async def get_subject_grade(self, student_id: int, subject_id: int) -> float:
        return await self._subject_grade_repo.get_grade(
            student_id=student_id, subject_id=subject_id
        )

    async def get_overall_grade(self, student_id: int) -> float:
        return await self._overall_grade_repo.get(student_id=student_id)

    async def set_assignment_grade(
        self, student_id: int, assignment_id: int, module_id: int, grade: float
    ) -> None:
        await self._assignment_grade_repo.upsert(
            student_id=student_id,
            assignment_id=assignment_id,
            module_id=module_id,
            grade=grade,
        )
