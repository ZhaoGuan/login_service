#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from sqlalchemy import delete, select, update, func
from sqlalchemy.orm import session
from sqlalchemy.orm.query import Query
# 多对一
from sqlalchemy.orm import selectinload
# 一对多
from sqlalchemy.orm import joinedload
# 子查询
from sqlalchemy.orm import subqueryload


class BaseSql:
    def __init__(self, model, db_session: session):
        self.model = model
        self.session = db_session

    async def get_all(self) -> Query:
        async with self.session.begin():
            query_result = await self.session.execute(select(self.model).order_by(self.model.id.desc()))
            return query_result.scalars()

    async def get_id_count(self, action) -> int:
        count_query = await self.session.execute(action.with_only_columns(func.count("id")))
        count_result = count_query.first()[0]
        return count_result

    async def get_count(self, action, module_attr) -> int:
        count_query = await self.session.execute(action.with_only_columns(func.count(module_attr)))
        count_result = count_query.first()[0]
        return count_result

    async def get_all_page(self, page_index, page_size) -> (Query, int):
        async with self.session.begin():
            query_result = await self.session.execute(
                select(self.model).order_by(self.model.id.desc()).limit(page_size).offset((page_index - 1) * page_size))
            result = query_result.scalars()
            count_query = await self.session.execute(func.count(self.model.id))
            count_result = count_query.first()[0]
            return result, count_result

    async def query(self, action) -> Query:
        async with self.session.begin():
            query_result = await self.session.execute(action)
            return query_result.scalar()

    async def query_all(self, action) -> Query:
        async with self.session.begin():
            query_result = await self.session.execute(action)
            return query_result.scalars()

    async def id_query(self, the_id) -> Query:
        async with self.session.begin():
            query_result = await self.session.execute(select(self.model).where(self.model.id == the_id))
            return query_result.scalar()

    async def name_query(self, name) -> Query:
        async with self.session.begin():
            query_result = await self.session.execute(select(self.model).where(self.model.name == name))
            return query_result.scalar()

    async def select_page(self, select_action, page_index, page_size) -> (Query, int):
        async with self.session.begin():
            query_result = await self.session.execute(
                select_action.order_by(self.model.id.desc()).limit(page_size).offset((page_index - 1) * page_size))
            total = await self.get_id_count(select_action)
            return query_result.scalars(), total

    async def search_select_page(self, select_action, page_index, page_size) -> (Query, int):
        async with self.session.begin():
            query_result = await self.session.execute(
                select_action.order_by(self.model.id.desc()).limit(page_size).offset((page_index - 1) * page_size))
            return query_result.scalars(), await self.get_id_count(select_action)

    async def add(self, model) -> (bool, [str, None]):
        async with self.session.begin():
            try:
                self.session.add(model)
                await self.session.flush()
                await self.session.commit()
                new_id = model.id
                return new_id
            except Exception as e:
                print(e)
                await self.session.rollback()
                return False

    async def update(self, update_action):
        async with self.session.begin():
            try:
                await self.session.execute(update_action)
                await self.session.commit()
            except Exception as e:
                print(e)
                await self.session.rollback()

    async def id_list_delete(self, id_list):
        async with self.session.begin():
            try:
                await self.session.execute(update(self.model).where(self.model.id.in_(id_list)).values(isDelete=1))
                await self.session.flush()
                await self.session.commit()
                return True
            except Exception as e:
                print(e)
                await self.session.rollback()
                return False

    async def id_delete(self, delete_id) -> (bool, [str, None]):
        async with self.session.begin():
            try:
                await self.session.execute(delete(self.model).filter(self.model.id == delete_id))
                await self.session.commit()
                return True
            except Exception as e:
                print(e)
                await self.session.rollback()
                return False
