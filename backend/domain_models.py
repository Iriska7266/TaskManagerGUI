import datetime
from typing import List, Iterator

from backend.constraints import *
from backend.dto import *


class TaskModel:
    def __init__(self, task_id: int, title: str, body: str, expires_at: datetime,
                 status: bool = False, created_at: datetime = lambda: pytz.UTC.localize(datetime.now())):
        check = self.__check_title__(title)
        if check:
            raise ValueError(check)
        check = self.__check_body__(body)
        if check:
            raise ValueError(check)

        self.task_id: int = task_id
        self.title: str = title
        self.body: str = body
        self.created_at: datetime = created_at
        self.expires_at: datetime = expires_at
        self.status: bool = status

    def change_title(self, new_title: str) -> Optional[str]:
        check = self.__check_title__(new_title)
        if check:
            return check
        self.title = new_title
        return None

    def change_body(self, new_body: str) -> Optional[str]:
        check = self.__check_body__(new_body)
        if check:
            return check
        self.body = new_body
        return None

    def change_deadline(self, new_deadline: datetime) -> None:
        self.expires_at = new_deadline
        return None

    def get_dto(self):
        return TaskDTO(task_id=self.task_id,
                       title=self.title,
                       body=self.body,
                       expires_at=self.expires_at,
                       status=self.status,
                       created_at=self.created_at)

    @staticmethod
    def __check_title__(f_title: str) -> Optional[str]:
        l = len(f_title)
        if not l:
            return "Task title can't be empty!"
        if l > TITLE_MAX_LEN:
            return f"Task title can't be more than {TITLE_MAX_LEN} characters!"

    @staticmethod
    def __check_body__(f_body: str) -> Optional[str]:
        l = len(f_body)
        if not l:
            return "Task content can't be empty!"
        if l > BODY_MAX_LEN:
            return f"Task content can't be more than {BODY_MAX_LEN} characters!"

    def toggle_status(self) -> None:
        self.status = not self.status

    def __str__(self):
        return (f"Task #{self.task_id} {self.title}\n"
                f"Content: {self.body}\n"
                f"Created: {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}\n"
                f"Expires: {self.expires_at.strftime("%Y-%m-%d %H:%M:%S")}\n"
                f"Status: {"Completed" if self.status else "In process"}")


class UserModel:
    def __init__(self,
                 uid: int,
                 login: str,
                 password_hash: str,
                 created_at: datetime = datetime.now()):
        self.uid: int = uid
        self.login: str = login
        self.password_hash: str = password_hash
        self.created_at: datetime = created_at
        self.tasks: List[TaskModel] = []

    def __str__(self):
        return (f"User #{self.uid}\n"
                f"Login: {self.login}\n"
                f"Password hash: {self.password_hash}\n"
                f"Registration time: {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}\n"
                f"Total tasks: {len(self.tasks)}")

    def add_task(self, new_task_params: TaskDTO) -> TaskModel:
        new_task = TaskModel(**vars(new_task_params))
        self.tasks.append(new_task)
        return new_task

    def get_all_tasks(self) -> Iterator[TaskDTO]:
        for task in self.tasks:
            task_info = TaskDTO(task.task_id, task.title, task.body, task.expires_at, task.status, task.created_at)
            yield task_info

    def get_active_tasks(self) -> Iterator[TaskDTO]:
        for task in self.tasks:
            if not task.status:
                task_info = TaskDTO(task.task_id, task.title, task.body, task.expires_at, task.status, task.created_at)
                yield task_info

    def get_dto(self):
        return UserDTO(self.uid,
                       self.login,
                       self.password_hash,
                       self.created_at)

    def get_tasks_count(self) -> int:
        return len(self.tasks)

    def get_task_by_number(self, task_number: int) -> Optional[TaskDTO]:
        try:
            task = self.tasks[task_number]
        except IndexError:
            return None
        else:
            return TaskDTO(task.task_id, task.title, task.body, task.expires_at, task.status, task.created_at)

    def delete_task(self, task_number: int) -> Optional[TaskDTO]:
        try:
            task = self.tasks.pop(task_number)
        except IndexError:
            return None
        else:
            return TaskDTO(task.task_id, task.title, task.body, task.expires_at, task.status, task.created_at)

    def toggle_task(self, task_number: int) -> Optional[TaskDTO]:
        try:
            task = self.tasks[task_number]
            task.toggle_status()
        except IndexError:
            return None
        else:
            return TaskDTO(task.task_id, task.title, task.body, task.expires_at, task.status, task.created_at)

    def edit_task_title(self, task_number: int, new_title: str) -> Optional[str]:
        return self.tasks[task_number].change_title(new_title)

    def edit_task_body(self, task_number: int, new_body: str) -> Optional[str]:
        return self.tasks[task_number].change_body(new_body)

    def edit_task_deadline(self, task_number: int, new_deadline: datetime) -> Optional[str]:
        return self.tasks[task_number].change_deadline(new_deadline)


class SystemModel:
    def __init__(self):
        self.users: List[UserModel] = []
        self.tasks_count = 0


    def add_user(self, new_user: UserDTO) -> Optional[UserModel]:
        new_user = UserModel(**vars(new_user))
        self.users.append(new_user)

        return new_user

    def authorise(self, user_params: UserDTO) -> Optional[UserModel]:
        for user in self.users:
            if user.login == user_params.login:
                if user.password_hash == user_params.password_hash:
                    return user
                else:
                    return None

    def delete_user(self):
        pass