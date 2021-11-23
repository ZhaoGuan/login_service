from datetime import datetime
from sqlalchemy.dialects.mssql.information_schema import columns
from sqlalchemy import select, update, func, text, or_, and_, between, desc
from sqlalchemy.orm import selectinload

from app.db.mysql.Users import UserTable
from app.db.service.base_service import BaseSql


class UserSql(BaseSql):
    def __init__(self, db_session):
        super().__init__(UserTable, db_session=db_session)

    async def get_by_email(self, email) -> UserTable:
        async with self.session.begin():
            result = await self.session.execute(select(self.model).where(self.model.email==email))
            return result.scalar()

    async def get_by_uuid(self, uuid) -> UserTable:
        async with self.session.begin():
            result = await self.session.execute(select(self.model).where(self.model.id==uuid))
            return result.scalar()