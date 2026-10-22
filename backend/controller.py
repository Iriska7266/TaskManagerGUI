from typing import Dict

from backend.domain_models import *
from database.repository import *


class UserController:
    def __init__(self, model: UserModel):
        self.model = model
        self.repo = UserRepository(model.get_dto())

        self.update_user_tasks_list()

        self.fail_source = ""
        self.tip_source = ""

    def get_user_params(self):
        return self.model.get_dto()

    def add_new_task(self, task_data: TaskDTO) -> int|str:
        try:
            task_id = self.repo.add_task(task_data)
        except RuntimeError as e:
            return str(e)
        else:
            return task_id

    def handle_task_changes(self, task_data: TaskDTO):
        self.repo.update_task(task_data)

    def update_user_tasks_list(self):
        self.model.tasks.clear()
        tasks = self.repo.get_user_tasks()
        for task in tasks:
            self.model.add_task(task)

    def toggle_task_status(self, task: TaskDTO) -> Dict[str, bool | str]:
        try:
            self.repo.switch_task_status(task)
        except ValueError as e:
            return {"success": False, "content": str(e)}
        else:
            if task.status:
                return {"success": True, "completed": False}
            else:
                return {"success": True, "completed": True}

    def delete_task(self, task: TaskDTO) -> Dict[str, bool | str]:
        try:
            self.repo.delete_task(task)
        except ValueError as e:
            return {"status": False, "content": str(e)}
        else:
            return {"status": True, "content": f"Task {task.title} removed successfully."}

    def get_user_tasks(self) -> Iterator[TaskDTO]:
        self.update_user_tasks_list()

        for task in self.model.tasks:
            yield task.get_dto()


class SystemController:
    def __init__(self):
        self.model = SystemModel()
        self.repo = SystemRepository()

    def authorise(self, login: str, password: str) -> Dict[str, bool|str|UserModel]:
        user_data = self.repo.get_user_by_login(login)

        if user_data is None:
            return {"status": False, "content": "No such user!"}
        else:
            # Check password
            if password == user_data.password_hash:
                user_model = UserModel(**vars(user_data))

                return {"status": True, "content": user_model}
            else:
                return {"status": False, "content": "Wrong password!"}

    def register(self, login: str, password: str) -> Dict[str, bool|str|UserModel]:
        user_model = self.repo.get_user_by_login(login)

        if user_model is None:
            user_data = self.repo.add_user(login, password)
            user_model = self.model.add_user(user_data)

            return {"status": True, "content": user_model}
        else:
            return {"status": False, "content": "Login is already busy!"}
