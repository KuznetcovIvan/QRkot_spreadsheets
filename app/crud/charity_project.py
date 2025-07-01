from typing import Union

from sqlalchemy import Integer, cast, extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[dict[str, Union[int, str]]]:
        projects = await session.execute(
            select(
                CharityProject.name,
                cast(
                    (
                        extract('year', CharityProject.close_date) -
                        extract('year', CharityProject.create_date)
                    ) * 365 +
                    (
                        extract('month', CharityProject.close_date) -
                        extract('month', CharityProject.create_date)
                    ) * 30 +
                    (
                        extract('day', CharityProject.close_date) -
                        extract('day', CharityProject.create_date)
                    ), Integer
                ).label('days_delta'),
                CharityProject.description,
            )
            .where(CharityProject.fully_invested.is_(True))
            .order_by('days_delta')
        )
        return [
            {'name': name,
             'days': days,
             'description': description}
            for name, days, description in projects.all()
        ]


charity_project_crud = CRUDCharityProject(CharityProject)
