from typing import List, Type, Union
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from evaluer.common.database.models import (
    ResponseGrade,
    AssignmentGrade,
    ModuleGrade,
    SubjectGrade,
    OverallGrade,
)


class GradingRepository:
    def __init__(
        self,
        db: AsyncSession,
        model: Type[DeclarativeBase],
        conflict_columns: List[str],
    ) -> None:
        self.db = db
        self.model = model
        self.conflict_columns = conflict_columns

    async def upsert(self, grade: float, **values: Union[int, str, float]) -> None:
        stmt = (
            insert(self.model)
            .values(grade=grade, **values)
            .on_conflict_do_update(
                index_elements=self.conflict_columns,
                set_={"grade": grade},
            )
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_by_filters(
        self, **filters: Union[int, str, float]
    ) -> List[DeclarativeBase]:
        stmt = select(self.model)
        for column, value in filters.items():
            stmt = stmt.where(getattr(self.model, column) == value)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_grade(self, **filters: Union[int, str, float]) -> float:
        stmt = select(self.model.grade)
        for column, value in filters.items():
            stmt = stmt.where(getattr(self.model, column) == value)
        result = await self.db.execute(stmt)
        grade = result.scalar_one_or_none()
        return grade if grade else 0


class ResponseGradeRepository(GradingRepository):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, ResponseGrade, ["response_id", "student_id"])

    async def upsert(
        self, student_id: int, response_id: int, assignment_id: int, grade: float
    ) -> None:
        await super().upsert(
            grade=grade,
            student_id=student_id,
            response_id=response_id,
            assignment_id=assignment_id,
        )

    async def get_all_for_assignment(
        self, assignment_id: int, student_id: int
    ) -> List[ResponseGrade]:
        return await self.get_by_filters(
            assignment_id=assignment_id, student_id=student_id
        )


class AssignmentGradeRepository(GradingRepository):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, AssignmentGrade, ["assignment_id", "student_id"])

    async def upsert(
        self, student_id: int, assignment_id: int, module_id: int, grade: float
    ) -> None:
        await super().upsert(
            grade=grade,
            student_id=student_id,
            assignment_id=assignment_id,
            module_id=module_id,
        )

    async def get_all_for_module(
        self, module_id: int, student_id: int
    ) -> List[AssignmentGrade]:
        return await self.get_by_filters(module_id=module_id, student_id=student_id)


class ModuleGradeRepository(GradingRepository):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, ModuleGrade, ["module_id", "student_id"])

    async def upsert(
        self, student_id: int, module_id: int, subject_id: int, grade: float
    ) -> None:
        await super().upsert(
            grade=grade,
            student_id=student_id,
            module_id=module_id,
            subject_id=subject_id,
        )

    async def get_all_for_subject(
        self, subject_id: int, student_id: int
    ) -> List[ModuleGrade]:
        return await self.get_by_filters(subject_id=subject_id, student_id=student_id)


class SubjectGradeRepository(GradingRepository):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, SubjectGrade, ["subject_id", "student_id"])

    async def upsert(self, student_id: int, subject_id: int, grade: float) -> None:
        await super().upsert(grade=grade, student_id=student_id, subject_id=subject_id)

    async def get_all_for_student(self, student_id: int) -> List[SubjectGrade]:
        return await self.get_by_filters(student_id=student_id)


class OverallGradeRepository(GradingRepository):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, OverallGrade, ["student_id"])

    async def upsert(self, student_id: int, grade: float) -> None:
        await super().upsert(grade=grade, student_id=student_id)

    async def get(self, student_id: int) -> float:
        return await self.get_grade(student_id=student_id)
