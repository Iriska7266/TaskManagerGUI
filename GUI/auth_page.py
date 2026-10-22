import flet as ft
import pickle
import os

from GUI.gui_configuration import AuthPageStyle
from GUI.utils import show_snack_message
from backend.domain_models import UserModel
from backend.settings import LOCAL_USER_DATA


def get_auth_page(page: ft.Page) -> ft.Container:
    async def handle_auth(reg: bool=False):
        password_field.error = None
        page.update()
        if login_field.value == "":
            login_field.error = "Login is empty!"
            page.update()
        elif password_field.value == "":
            password_field.error = "Enter password!"
            page.update()
        else:
            try:
                from backend.controller import SystemController, UserController
            except Exception as e:
                show_snack_message(page, str(e), "error")
            else:
                control = SystemController()

                try:
                    check_result = control.authorise(login_field.value, password_field.value) if not reg else \
                                        control.register(login_field.value, password_field.value)
                except ConnectionError as e:
                    show_snack_message(page, str(e), "error")
                else:
                    if check_result["status"]:
                        # Saving user parameters
                        if data_save_check.value:
                            with open(LOCAL_USER_DATA, 'wb') as u_data_f:
                                # noinspection PyTypeChecker
                                pickle.dump(check_result["content"], u_data_f)

                        controller = UserController(check_result["content"])
                        page.session.store.set("user_controller", controller)
                        page.session.store.set("new_user_check", True if reg else False)
                        await page.push_route("/tasks")
                    else:
                        show_snack_message(page, check_result["content"], 'error')

    # Greet
    greet = ft.Text(value="Welcome to Task Manager!", size=AuthPageStyle.greet_size)

    def clear_login_error():
        login_field.error = None
    def clear_password_error():
        password_field.error = None

    # Fields
    login_field = ft.TextField(label="Login",
                               width=AuthPageStyle.login_width,
                               on_change=clear_login_error,
                               on_submit=handle_auth)
    password_field = ft.TextField(hint_text="Password",
                                  password=True,
                                  width=AuthPageStyle.password_width,
                                  on_change=clear_password_error,
                                  on_submit=handle_auth)
    if os.path.exists(LOCAL_USER_DATA):
        with open(LOCAL_USER_DATA, 'rb') as f:
            user_model: UserModel = pickle.load(f)
        login_field.value = user_model.login
        password_field.value = user_model.password_hash

    def toggle_password_visibility():
        password_field.password = not password_field.password
        page.update()

    # Checks
    show_password_check = ft.Checkbox(label="Show password",
                                      value=False,
                                      on_change=toggle_password_visibility)
    data_save_check = ft.Checkbox(label="Remember me")

    # Buttons
    log_in_btn = ft.Button("Log in",
                           width=AuthPageStyle.login_width,
                           on_click=lambda: page.run_task(handle_auth, reg=False))
    new_account_btn = ft.Button("Create account",
                                width=AuthPageStyle.password_width,
                                on_click=lambda: page.run_task(handle_auth, reg=True))

    async def go_to_dotenv_settings():
        await page.push_route("/db_conf")

    go_to_dotenv_settings_btn = ft.Button("DB settings",
                                          width=AuthPageStyle.go_to_dotenv_settings_width,
                                          on_click=go_to_dotenv_settings)

    return ft.Container(
        content=ft.Column(
            controls=[
                greet,
                ft.Text(height=AuthPageStyle.greet_margin),
                login_field,
                password_field,
                show_password_check,
                data_save_check,
                log_in_btn,
                new_account_btn,
                go_to_dotenv_settings_btn
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            intrinsic_width=True
        )
    )
