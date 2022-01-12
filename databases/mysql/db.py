#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from sqlalchemy.orm import sessionmaker, session, scoped_session
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from urllib.parse import quote_plus as urlquote
import settings
from contextlib import contextmanager

local_db_config = f'sqlite:///{settings.TEMP_DIR}/local.db'


class DB:
    db = None
    MYSQL_HOST = None
    MYSQL_PORT = None
    MYSQL_USER = None
    MYSQL_PASSWORD = None
    MYSQL_DB = None

    def __init__(self, env=None, is_async=True):
        self.is_async = is_async
        self.db_config = self.mysql_config(env)
        if self.is_async:
            self.engine = create_async_engine(self.db_config, echo=True, pool_pre_ping=True)
        else:
            self.engine = create_engine(self.db_config, echo=True, pool_pre_ping=True)

    def mysql_config(self, env):
        if env:
            setting_list = list(
                filter(lambda m: not m.startswith("__") and not m.endswith("__") and m.startswith(env), dir(settings)))
        else:
            setting_list = list(filter(lambda m: not m.startswith("__") and not m.endswith("__"), dir(settings)))
        """获取MYSQL配置"""
        for config in setting_list:
            if "MYSQL_HOST" in config:
                self.MYSQL_HOST = getattr(settings, config)
            if "MYSQL_PORT" in config:
                self.MYSQL_PORT = getattr(settings, config)
            if "MYSQL_USER" in config:
                self.MYSQL_USER = getattr(settings, config)
            if "MYSQL_PASSWORD" in config:
                self.MYSQL_PASSWORD = getattr(settings, config)
            if "MYSQL_DB" in config:
                self.MYSQL_DB = getattr(settings, config)
        if self.MYSQL_DB and self.MYSQL_HOST and self.MYSQL_PORT and self.MYSQL_USER and self.MYSQL_PASSWORD:
            """密码有特殊字符的时候用urlquote转义"""
            if self.is_async:
                return f'mysql+aiomysql://{self.MYSQL_USER}:{urlquote(self.MYSQL_PASSWORD)}@{self.MYSQL_HOST}/{self.MYSQL_DB}'
            else:
                return f'mysql+pymysql://{self.MYSQL_USER}:{urlquote(self.MYSQL_PASSWORD)}@{self.MYSQL_HOST}/{self.MYSQL_DB}'
        else:
            assert False, "MYSQL配置内容不全"

    def __call__(self, *args, **kwargs):
        return self.session()

    def session(self):
        if self.is_async:
            return sessionmaker(self.engine, AsyncSession, expire_on_commit=False)()
        else:
            return sessionmaker(self.engine, expire_on_commit=False)()

    def close_db(self):
        return self.db.close_all()


async_db = DB(settings.ENV)
db = DB(settings.ENV, is_async=False)
