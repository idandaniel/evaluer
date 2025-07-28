from typing import Dict, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from evaluer.core.database.models import ResponseGrade


class GradingRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def save_response_grade(self, response_id: int, grade: int) -> None:
        stmt = select(ResponseGrade).where(ResponseGrade.response_id == response_id)
        result = await self._db_session.execute(stmt)
        existing_grade = result.scalar_one_or_none()
        
        if existing_grade:
            existing_grade.grade = grade
        else:
            new_grade = ResponseGrade(response_id=response_id, grade=grade)
            self._db_session.add(new_grade)
        
        await self._db_session.commit()

    async def get_response_grade(self, response_id: int) -> Optional[int]:
        stmt = select(ResponseGrade).where(ResponseGrade.response_id == response_id)
        result = await self._db_session.execute(stmt)
        grade_record = result.scalar_one_or_none()
        
        return grade_record.grade if grade_record else None

    async def get_all_response_grades(self) -> Dict[int, int]:
        stmt = select(ResponseGrade)
        result = await self._db_session.execute(stmt)
        grade_records = result.scalars().all()
        return {record.response_id: record.grade for record in grade_records}

    async def get_response_grades_by_ids(self, response_ids: List[int]) -> Dict[int, int]:
        stmt = select(ResponseGrade).where(ResponseGrade.response_id.in_(response_ids))
        result = await self._db_session.execute(stmt)
        grade_records = result.scalars().all()
        return {record.response_id: record.grade for record in grade_records}
