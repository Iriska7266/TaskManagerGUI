from sqlalchemy import select, func, cast, Text
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import Session
from typing import List

from backend.dto import *
from database.db import get_db
from database.orm import User, Task


class UserRepository:
    def __init__(self, user: UserDTO):
        self.user = user

    def get_user_tasks(self) -> List[TaskDTO]:
        with get_db() as db:
            db: Session
            stmt = select(Task).join(Task.users).where(User.u_id == self.user.uid).order_by(Task.created_at)
            tasks = db.execute(stmt).scalars().all()
            return [TaskDTO.from_orm(task) for task in tasks]

    @staticmethod
    def get_task(task_id: int) -> TaskDTO:
        with get_db() as db:
            db: Session

            stmt = select(Task).where(Task.t_id == task_id)
            task = db.execute(stmt).scalars().first()
            if task is None:
                raise ValueError("Task is not found!")
            return TaskDTO.from_orm(task)

    def add_task(self, task: TaskDTO) -> int:
        with get_db() as db:
            db: Session
            stmt = func.add_task(self.user.uid,
                                   cast(task.title, Text),
                                   cast(task.body, Text),
                                   task.created_at,
                                   task.expires_at,
                                   task.status)
            result = db.execute(stmt).scalar_one()
            if result == -1:
                db.rollback()
                raise RuntimeError("Database failure!")
            else:
                db.commit()
                return result

    @staticmethod
    def delete_task(task: TaskDTO) -> None:
        with get_db() as db:
            db: Session

            task_db = db.get(Task, task.task_id)
            if task_db is None:
                raise ValueError("Task is not found!")
            db.delete(task_db)
            db.commit()

    @staticmethod
    def switch_task_status(task: TaskDTO) -> None:
        with get_db() as db:
            db: Session

            task_db = db.get(Task, task.task_id)
            if task_db is None:
                raise ValueError("Task is not found!")
            task_db.status = not task_db.status
            db.commit()
            db.refresh(task_db)

    @staticmethod
    def change_task_title(task: TaskDTO, new_title: str) -> None:
        with get_db() as db:
            db: Session

            task_db = db.get(Task, task.task_id)
            if task_db is None:
                raise ValueError("Task is not found!")
            task_db.title = new_title
            db.commit()
            db.refresh(task_db)

    @staticmethod
    def change_task_content(task: TaskDTO, new_content: str) -> None:
        with get_db() as db:
            db: Session

            task_db = db.get(Task, task.task_id)
            if task_db is None:
                raise ValueError("Task is not found!")
            task_db.t_content = new_content
            db.commit()
            db.refresh(task_db)

    @staticmethod
    def change_task_deadline(task: TaskDTO, new_deadline) -> None:
        with get_db() as db:
            db: Session

            task_db = db.get(Task, task.task_id)
            if task_db is None:
                raise ValueError("Task is not found!")
            task_db.expires_at = new_deadline
            db.commit()
            db.refresh(task_db)

    @staticmethod
    def update_task(task_data: TaskDTO):
        with get_db() as db:
            db: Session

            task_model = db.get(Task, task_data.task_id)

            task_model.title = task_data.title
            task_model.t_content = task_data.body
            task_model.expires_at = task_data.expires_at
            task_model.status = task_data.status

            db.commit()
            db.refresh(task_model)


class SystemRepository:
    @staticmethod
    def get_user_by_login(login: str) -> Optional[UserDTO]:
        with get_db() as db:
            db: Session
            try:
                stmt = select(User).where(User.u_login == login)
                user = db.execute(stmt).scalars().first()

                if not user is None:
                    db.refresh(user)
                    user_dto = UserDTO(user.u_id,
                                       user.u_login,
                                       user.u_password_hash,
                                       user.created_at)
                    return user_dto
                else:
                    return None
            except NoResultFound:
                return None

    @staticmethod
    def add_user(login: str, password_hash: str) -> Optional[UserDTO]:
        with get_db() as db:
            db: Session
            try:
                new_user = User(u_login=login, u_password_hash=password_hash)
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                user_data = UserDTO(new_user.u_id,
                                    new_user.u_login,
                                    new_user.u_password_hash,
                                    new_user.created_at)
                return user_data
            except IntegrityError:
                return None

    @staticmethod
    def get_all_users() -> List[UserDTO]:
        with get_db() as db:
            db: Session

            stmt = select(User)
            users_data = db.execute(stmt).scalars().all()
            return [UserDTO.from_orm(user_data) for user_data in users_data]