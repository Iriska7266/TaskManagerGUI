from datetime import datetime
from typing import List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (Identity, DateTime, Boolean, ForeignKey,
                        Table, Column, func, text)


class Base(DeclarativeBase):
    pass


user_tasks_table = Table(
    "user_tasks",
    Base.metadata,
    Column("u_id",
           ForeignKey("accounts.u_id", ondelete="CASCADE", onupdate="CASCADE"),
           primary_key=True),
    Column("t_id",
           ForeignKey("tasks.t_id", ondelete="CASCADE", onupdate="CASCADE"),
           primary_key=True),
)


class User(Base):
    __tablename__ = "accounts"

    u_id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    u_login: Mapped[str]
    u_password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 nullable=False)

    tasks: Mapped[List["Task"]] = relationship(
                                    secondary=user_tasks_table,
                                    back_populates="users")


class Task(Base):
    __tablename__ = "tasks"

    t_id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    title: Mapped[str]
    t_content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(),
                                                 nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False)
    status: Mapped[bool] = mapped_column(Boolean,
                                         server_default=text("false"))

    users: Mapped[List["User"]] = relationship(
                                        secondary=user_tasks_table,
                                        back_populates="tasks")
