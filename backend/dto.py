from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped

from database.orm import Task as TaskORM
from database.orm import User as UserORM


@dataclass
class TaskDTO:
    task_id: Optional[int] | Mapped[int]
    title: str | Mapped[str]
    body: str | Mapped[str]
    expires_at: Optional[datetime | Mapped[datetime]]
    status: bool = False
    created_at: Optional[datetime | Mapped[datetime]] = field(default_factory= lambda: datetime.now())

    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Content: {self.body}\n"
                f"Created: {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}\n"
                f"Expires: {self.expires_at.strftime("%Y-%m-%d %H:%M:%S")}\n"
                f"Status: {"Completed" if self.status else "In process"}")

    @classmethod
    def from_orm(cls, task_orm: TaskORM) -> "TaskDTO":
        return cls(
            task_id=task_orm.t_id,
            title=task_orm.title,
            body=task_orm.t_content,
            expires_at=task_orm.expires_at,
            status=task_orm.status,
            created_at=task_orm.created_at
        )


@dataclass
class UserDTO:
    uid: int | Mapped[int]
    login: str | Mapped[str]
    password_hash: str | Mapped[str]
    created_at: datetime | Mapped[datetime] = datetime.now()

    def __str__(self):
        return (f"ID: {self.uid};\n"
                f"Login: {self.login};\n"
                f"Password hash: {self.password_hash};\n"
                f"Creation time: {self.created_at}")

    @classmethod
    def from_orm(cls, user_orm: UserORM) -> "UserDTO":
        return cls(
            uid=user_orm.u_id,
            login=user_orm.u_login,
            password_hash=user_orm.u_password_hash,
            created_at=user_orm.created_at
        )