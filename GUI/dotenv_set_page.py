import flet as ft
import os
from typing import Dict, Optional

from backend.settings import DOTENV_PATH
from GUI.utils import show_snack_message
from GUI.gui_configuration import DotenvSettingsPageStyle


def get_cur_dotenv_values() -> Optional[Dict[str, str]]:
    values = {}
    if os.path.exists(DOTENV_PATH):
        with open(DOTENV_PATH, "r") as f:
            for line in f.readlines():
                if line[0] == "#":
                    continue
                key, value = line.split("=")
                value = value.split()[0]
                value = value.split("#")[0]
                values[key] = value

        return values
    else:
        return None


def show_dotenv_window(page: ft.Page) -> list[ft.Control]:
    def remove_error(e: ft.ControlEventHandler[ft.TextField]):
        e.control.error = None

    cur_values = get_cur_dotenv_values()

    db_login_field = ft.TextField(
        label="DB login",
        value=cur_values["LOGIN"] if (cur_values and cur_values["LOGIN"]) else "postgres",
        on_change=remove_error
    )
    db_password_field = ft.TextField(
        label="DB password",
        value=cur_values["PASSWORD"]  if (cur_values and cur_values["PASSWORD"]) else "",
        on_change=remove_error
    )
    db_host_field = ft.TextField(
        label="Host",
        value=cur_values["HOST"] if (cur_values and cur_values["HOST"]) else "localhost",
        on_change=remove_error
    )
    db_name_field = ft.TextField(
        label="DB name",
        value=cur_values["DB_NAME"] if (cur_values and cur_values["DB_NAME"]) else "tasks_system_db",
        on_change=remove_error
    )
    db_port_field = ft.TextField(
        label="Port",
        value=cur_values["PORT"] if (cur_values and cur_values["PORT"]) else "5432",
        on_change=remove_error
    )
    fields = [db_login_field,
              db_password_field,
              db_host_field,
              db_port_field,
              db_name_field]

    async def go_back():
        page.views.pop()
        new_page = page.views[-1]
        await page.push_route(new_page.route)

    async def handle_changes():
        empty = False
        for field in fields:
            if not len(field.value):
                field.error = "Empty field!"
                empty = True
            else:
                field.error = None
        if not empty:
            with open(DOTENV_PATH, "w") as f:
                params = (f"LOGIN={db_login_field.value}\n"
                          f"PASSWORD={db_password_field.value}\n"
                          f"HOST={db_host_field.value}\n"
                          f"DB_NAME={db_name_field.value}\n"
                          f"PORT={db_port_field.value}\n"
                          "DMS=postgresql+psycopg2\n"
                          "DB_URL=${DMS}://${LOGIN}:${PASSWORD}@${HOST}:${PORT}/${DB_NAME}")
                f.write(params)
                show_snack_message(page, "Changes saved successfully!\nRestart the program to apply the changes.", "success")

                await go_back()

    back_button = ft.Button("Back", icon=ft.Icon(ft.Icons.ARROW_BACK_ROUNDED), on_click=go_back)
    submit_button = ft.Button("Save", on_click=handle_changes)


    return [
        ft.Row(
            controls=[back_button],
            margin=30,
            alignment=ft.CrossAxisAlignment.START
        ),
        ft.Column(
            controls=[
                ft.Text("Database configuration",
                        size=DotenvSettingsPageStyle.title_font_size,
                        margin=20
                        ),
                *fields,
                submit_button
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            align=ft.Alignment.CENTER
        )
    ]


if __name__ == '__main__':
    ft.run(show_dotenv_window)