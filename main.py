import os
import flet as ft
from pathlib import Path
from pickle import dump

from backend.settings import DOTENV_PATH, SETTINGS_PATH


work_dir = Path(__file__).resolve().parent


async def start(page: ft.Page):
    page.window.maximized = True
    page.title = "Task Manager"
    page.window.icon = str(work_dir / "Icon.ico")
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window.maximized = True
    page.update()

    # Page alignment
    # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def auth_page():
        from GUI.auth_page import get_auth_page
        return get_auth_page(page)

    def db_settings():
        from GUI.dotenv_set_page import show_dotenv_window
        return show_dotenv_window(page)

    auth_view = ft.View(
            route="/",
            controls=[auth_page()],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    page.views.append(auth_view)

    def route_change():
        page.views.clear()
        page.views.append(auth_view)
        auth_view.padding = 50

        from GUI.tasks_page import UserWindow

        settings = {"width": page.width, "height": page.height}

        with open(SETTINGS_PATH, "wb") as f:
            dump(settings, f)

        if page.route == "/db_conf":
            page.views.append(
                ft.View(
                    route="/db_conf",
                    controls=[
                        *db_settings()
                    ],
                    spacing=150
                )
            )
        if page.route == "/tasks":
            page.views.append(
                UserWindow()
            )

    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    if not os.path.exists(DOTENV_PATH):
        await page.push_route("/db_conf")
    else:
        await page.push_route("/")


if __name__ == '__main__':
    ft.run(start)
