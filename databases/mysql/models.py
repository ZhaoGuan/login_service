#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from datetime import datetime
import asyncio
from sqlalchemy import Table, ForeignKey
from sqlalchemy import Column, String, JSON, INTEGER, BOOLEAN, TEXT, DATETIME
from sqlalchemy.orm import registry, relationship
# 3.7 新增
from dataclasses import dataclass, field
import os
from databases.mysql.db import db

PATH = os.path.dirname(os.path.abspath(__file__))
mapper_registry = registry()
Base = mapper_registry.generate_base()

# 自动建表
mapper_registry.metadata.create_all(db.engine)
# 异步
# async def async_main():
#     async with async_db.engine.begin() as conn:
#         await conn.run_sync(mapper_registry.metadata.create_all)

# 数据迁移还不清楚
# asyncio.run(async_main())
