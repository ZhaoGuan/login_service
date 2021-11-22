import datetime
import uuid

from sqlalchemy import Table, ForeignKey, DATETIME, Boolean, ARRAY, Enum
from sqlalchemy import Column, String, JSON, INTEGER, BOOLEAN, TEXT, DATE, DateTime, Date, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry, relationship
# 3.7 新增
from dataclasses import dataclass, field
import os

from app.db.mysql.EnumTypes import PermissionLevel

PATH = os.path.dirname(os.path.abspath(__file__))
mapper_registry = registry()
Base = mapper_registry.generate_base()


@mapper_registry.mapped
@dataclass
class UserTable:
    __table__ = Table(
        "user",
        mapper_registry.metadata,
        Column('id', UUID(as_uuid=True), primary_key=True, unique=True),
        Column("email", String(length=100), unique=True, nullable=False),
        Column("name", String(length=100)),
        Column("permission_level", Enum(PermissionLevel), nullable=False),
        Column("phone_number", String(length=20)),
        Column("last_fetch", DateTime),
        Column("token", String()),
        Column("refresh_token", String()),
        Column("token_uri", String()),
        Column("client_id", String()),
        Column("scopes", ARRAY(String())),
        Column("create_time", DateTime),
        Column("last_login", DateTime),
        Column("exp", DateTime),
    )
    id: str = field(default=uuid.uuid4())
    email: str = field(default=None)
    name: str = field(default=None)
    permission_level: INTEGER = field(default=None)
    phone_number: str = field(default=None)
    last_fetch: str = field(default=None)
    token: str = field(default=None)
    refresh_token: str = field(default=None)
    token_uri: str = field(default=None)
    client_id: str = field(default=None)
    client_secret: str = field(default=None)
    scopes: str = field(default=None)
    create_time: DateTime = field(default=datetime.datetime.now())
    last_login: DateTime = field(default=None)
    exp: DateTime = field(default=None)

    def to_dict(self):
        return dict(
            user_id=str(self.id),
            email=self.email,
            username=self.name
        )