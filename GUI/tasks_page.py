import os.path
import pickle
import sys
from datetime import timedelta, time

from backend.constraints import *
from backend.settings import data_dir
from GUI.gui_configuration import TasksPageStyle
from GUI.utils import *
from backend.dto import UserDTO


@ft.control
class UserWindow(ft.View):
    route: str = "/tasks"
    controller = None # UserControlle
    user_params = None # UserDTO
    FILTERS_SETTINGS_PATH = None # String constant
    tasks_table: ft.ResponsiveRow | None = None

    only_completed: ft.Checkbox | None = None
    only_in_process: ft.Checkbox | None = None
    only_overdue: ft.Checkbox | None = None
    horizontal_alignment = ft.CrossAxisAlignment.CENTER
    vertical_alignment = ft.MainAxisAlignment.CENTER

    def build(self):
        from backend.controller import UserController

        self.controller: UserController = self.page.session.store.get("user_controller")
        self.user_params: UserDTO = self.controller.get_user_params()
        self.padding = 50
        self.page.window.prevent_close = True
        self.page.window.on_event = lambda e: self.handle_close_window_event(e)

        self.tasks_table = ft.ResponsiveRow(columns=4,
                                            height=TasksPageStyle.task_table_height,
                                            width=TasksPageStyle.task_table_width,
                                            scroll=ft.ScrollMode.AUTO,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            data={"control_name": "tasks_table"})

        new_user: bool = self.page.session.store.get("new_user_check")
        if new_user:
            show_snack_message(self.page, "New account created successfully!", m_type='success')

        # Filters
        filter_values = None
        self.FILTERS_SETTINGS_PATH = data_dir / f"{self.user_params.uid}_filters_setting.dat"
        if os.path.exists(self.FILTERS_SETTINGS_PATH):
            filter_values = pickle.load(open(self.FILTERS_SETTINGS_PATH, 'rb'))
        self.only_completed = ft.Checkbox(label="Completed",
                                          value=filter_values[0] if filter_values else True,
                                          on_change=self.update_tasks_table)
        self.only_in_process = ft.Checkbox(label="In process",
                                           value=filter_values[1] if filter_values else True,
                                           on_change=self.update_tasks_table)
        self.only_overdue = ft.Checkbox(label="Overdue",
                                        value=filter_values[2] if filter_values else True,
                                        on_change=self.update_tasks_table)

        self.controls = self.work_window()

    def handle_close_window_event(self, e:ft.WindowEvent):
        if e.type.name == "CLOSE":
            self.save_filters_settings()

            self.page.window.prevent_close = False
            self.page.window.on_event = None
            sys.exit()


    def save_filters_settings(self):
        filter_values = [self.only_completed.value, self.only_in_process.value, self.only_overdue.value]
        with open(self.FILTERS_SETTINGS_PATH, 'wb') as f_s_f:
            # noinspection PyTypeChecker
            pickle.dump(filter_values, f_s_f)

    def update_tasks_table(self):
        self.tasks_table.controls.clear()
        for task in self.controller.get_user_tasks():
            task_status = get_task_status(task)
            if (self.only_completed.value and task_status == "completed") or \
                    (self.only_overdue.value and task_status == "overdue") or \
                    (self.only_in_process.value and task_status == "in process"):
                self.tasks_table.controls.append(self.task_preview_card(task))
                self.page.update()
        if not len(self.tasks_table.controls):
            self.tasks_table.controls.append(
                ft.Text("Tasks not found",
                        size=TasksPageStyle.void_tasks_msg_size,
                        align=ft.Alignment.CENTER,
                        col=4)
            )
        self.page.update()


    def task_dialog(self, task_data: TaskDTO) -> ft.AlertDialog:

        # ----------------------------
        # Text fields (title and content)
        def hide_title_error():
            t_title.error = None
        def hide_content_error():
            t_content.error = None
        t_title = ft.TextField(value=task_data.title,
                               text_size=TasksPageStyle.dialog_title_size,
                               multiline=True,
                               max_length=TITLE_MAX_LEN,
                               border=ft.InputBorder.UNDERLINE,
                               label=ft.Text("Title"),
                               on_change=hide_title_error)
        t_content = ft.TextField(value=task_data.body,
                                 text_size=TasksPageStyle.dialog_content_size,
                                 multiline=True,
                                 max_length=BODY_MAX_LEN,
                                 width=TasksPageStyle.dialog_card_width,
                                 label=ft.Text("Content"),
                                 on_change=hide_content_error)
        # ----------------------------

        # ----------------------------
        # Dates and time
        def handle_deadline_date(e: ft.Event[ft.DatePicker]):
            deadline_date_field.value = get_local_datetime(e.control.value).strftime("%Y-%m-%d")

        def handle_deadline_time(e: ft.Event[ft.DatePicker]):
            deadline_time_field.value = get_local_datetime(e.control.value).strftime("%H:%M:%S")

        creation_time = ft.Column(
            controls=[
                ft.Divider(),
                ft.Text(value="Creation time: " + task_data.created_at.strftime("%Y-%m-%d %H:%M:%S")),
                ft.Divider()
            ]
        ) if task_data.created_at else ft.Text()
        deadline_date_picker = ft.DatePicker(on_change=handle_deadline_date,
                                             first_date=datetime.now().date(),
                                             current_date=task_data.expires_at.date() if task_data.expires_at else
                                             get_local_datetime(datetime.now()).date())
        deadline_time_picker = ft.TimePicker(on_change=handle_deadline_time,
                                             value=task_data.expires_at.time() if task_data.expires_at else
                                             get_local_datetime(datetime.now()).time())

        tomorrow=datetime.combine(datetime.now().date() + timedelta(days=1), time(9))


        deadline_date_field = ft.TextField(
            value=task_data.expires_at.date().strftime("%Y-%m-%d") if task_data.expires_at
                    else tomorrow.strftime("%Y-%m-%d"),
            on_click=lambda e: self.page.show_dialog(deadline_date_picker),
            icon=ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED),
            width=TasksPageStyle.date_field_width,
            border=ft.UnderlineInputBorder()
        )
        deadline_time_field = ft.TextField(
            value=task_data.expires_at.time().strftime("%H:%M:%S") if task_data.expires_at
                    else tomorrow.strftime("%H:%M:%S"),
            on_click=lambda e: self.page.show_dialog(deadline_time_picker),
            icon=ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED),
            width=TasksPageStyle.time_field_width,
            border=ft.UnderlineInputBorder()
        )
        # ----------------------------

        def handle_task_data_changes():
            new_deadline = datetime.strptime(f"{deadline_date_field.value} {deadline_time_field.value}",
                                             "%Y-%m-%d %H:%M:%S")

            created_at = task_data.created_at

            new_task_data = TaskDTO(task_id=task_data.task_id,
                                    title=t_title.value,
                                    body=t_content.value,
                                    created_at=created_at,
                                    expires_at=new_deadline,
                                    status=task_data.status)
            self.controller.handle_task_changes(new_task_data)
            self.update_tasks_table()
            self.page.pop_dialog()

        def create_a_new_task():
            new_deadline = datetime.strptime(f"{deadline_date_field.value} {deadline_time_field.value}",
                                             "%Y-%m-%d %H:%M:%S")

            if t_title.value == "":
                t_title.error = ft.Text("Title can't be empty!")
            if t_content.value == "":
                t_content.error = ft.Text("Title can't be empty!")
            else:
                new_task_data = TaskDTO(task_id=task_data.task_id,
                                        title=str(t_title.value),
                                        body=str(t_content.value),
                                        expires_at=new_deadline)

                new_task_data.task_id = self.controller.add_new_task(new_task_data)

                self.update_tasks_table()
                self.page.pop_dialog()
                self.page.update()

        return ft.AlertDialog(
            title=ft.Container(
                content=t_title,
                width=TasksPageStyle.dialog_card_width
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        creation_time,
                        t_content,
                        ft.Row(
                            controls=[
                                deadline_date_field,
                                deadline_time_field
                            ],
                            tight=True,
                            spacing = 20,
                            align=ft.Alignment.CENTER, # Within it's parent (Column)
                            alignment=ft.MainAxisAlignment.CENTER # Of it's children
                        )
                    ],
                    tight=True
                ),
                width=TasksPageStyle.dialog_card_width
            ),
            actions=[
                ft.TextButton("Ok",
                              on_click=handle_task_data_changes if task_data.task_id else create_a_new_task)
            ]
        )


    def task_preview_card(self, task: TaskDTO) -> ft.Container:
        # ----------------------------
        # title cut
        # ----------------------------
        title_to_show = cut_str(task.title, TasksPageStyle.max_preview_title_len)
        # ----------------------------
        # content cut
        # ----------------------------
        content_to_show = task.body
        # if len(content_to_show) > TasksPageStyle.max_preview_content_len:
        #     content_to_show = content_to_show[:TasksPageStyle.max_preview_content_len-3] + "..."

        # ----------------------------
        # info
        # ----------------------------
        task_title = ft.Text(value=title_to_show,
                             size=TasksPageStyle.preview_title_size,
                             selectable=True,
                             align=ft.Alignment.CENTER)
        task_content = ft.Text(value=content_to_show,
                               size=TasksPageStyle.preview_content_size,
                               selectable=True,
                               max_lines=5,
                               overflow=ft.TextOverflow.ELLIPSIS)
        task_deadline = ft.Text(value=task.expires_at.strftime("%Y-%m-%d %H:%M:%S"),
                                selectable=True)

        # ----------------------------
        # status switch
        # ----------------------------
        def swap_task_status():
            swap_result = self.controller.toggle_task_status(task)
            title_cut = cut_str(task.title, TasksPageStyle.max_title_len_for_notif)
            text_to_show = f"Task {title_cut} {"completed successfully" if swap_result["completed"]
                                else "is in process now"}."
            if swap_result["success"]:
                show_snack_message(self.page, m_text=text_to_show, m_type='success' if swap_result["completed"]
                                        else 'info')
            else:
                show_snack_message(self.page, m_text=swap_result["content"], m_type='error')
            self.update_tasks_table()

        status_switch = ft.Button(
                            ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED if task.status
                                        else ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED),
                            on_click=swap_task_status
        )

        # ----------------------------
        # delete button
        # ----------------------------

        def delete_task():
            self.controller.delete_task(task)
            self.update_tasks_table()
            title_cut = cut_str(task.title, TasksPageStyle.max_title_len_for_notif)
            self.page.pop_dialog()
            show_snack_message(self.page, f"Task {title_cut} deleted successfully")

        def task_delete_dialog() -> ft.AlertDialog:
            dialog = ft.AlertDialog(
                title=ft.Text("Delete task"),
                content=ft.Text("Are you sure you want to delete this task?"),
                actions=[
                    ft.Button("Yes",
                              icon=ft.Icon(ft.Icons.DELETE_FOREVER_OUTLINED),
                              color=ft.Colors.RED,
                              on_click=delete_task),
                    ft.Button("No", on_click=self.page.pop_dialog)
                ]
            )
            return dialog

        delete_button = ft.Button(
            ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED),
            on_click=lambda: self.page.show_dialog(task_delete_dialog())
        )

        # ----------------------------
        # status color and icon
        # ----------------------------
        task_status = get_task_status(task)
        if task_status == "completed":
            status_color = ft.Colors.GREEN_700
            status_icon = ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                                  color=status_color,
                                  tooltip="Completed")
        elif task_status == "overdue":
            status_color = ft.Colors.RED
            status_icon = ft.Icon(ft.Icons.CANCEL_OUTLINED,
                                  color=status_color,
                                  tooltip="Overdue")
        else:
            status_color = ft.Colors.BLUE_GREY_300
            status_icon = ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED,
                                  color=status_color,
                                  tooltip="In process")
        # ----------------------------
        card = ft.Card(
            variant=ft.CardVariant.FILLED,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        task_content
                    ]
                ),
                padding=10,
                border_radius=10,
                width=TasksPageStyle.preview_card_width
            )
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    task_title,
                    card,
                    ft.Row(
                        controls=[
                            task_deadline,
                            status_icon
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Row(
                        controls=[
                            status_switch,
                            delete_button
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND
            ),
            width=TasksPageStyle.preview_card_width,
            height=TasksPageStyle.preview_card_height,
            border_radius=10,
            padding=10,
            margin=20,
            border=ft.Border.all(2, status_color),
            col=1,
            ink=True,
            on_click=lambda e: self.page.show_dialog(self.task_dialog(task)),
            data={"task_id": task.task_id}
        )


    def work_window(self):
        self.update_tasks_table()

        refresh_button = ft.Button(
                        icon=ft.Icon(ft.Icons.REFRESH_ROUNDED),
                        content="Refresh page",
                        on_click=self.work_window
        )

        async def exit_from_account():
            self.save_filters_settings()
            await self.page.push_route("/")

        exit_button = ft.Button(
            "Exit",
            icon=ft.Icon(ft.Icons.LOGOUT_ROUNDED),
            on_click=exit_from_account
        )

        add_button = ft.FloatingActionButton(
                    icon=ft.Icon(ft.Icons.ADD_ROUNDED, size=55),
                    on_click=lambda e: self.page.show_dialog(
                        self.task_dialog(TaskDTO(task_id=None, title="", body="", created_at=None, expires_at=None))
                    )
        )

        return [
                ft.Row(
                    controls=[
                        refresh_button,
                        exit_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Filters"),
                                self.only_completed,
                                self.only_in_process,
                                self.only_overdue
                            ]
                        ),
                        ft.Container(
                            content=self.tasks_table,
                            width=TasksPageStyle.task_table_width,
                            height=TasksPageStyle.task_table_height
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY
                ),
                ft.Row(
                    controls=[
                        add_button
                    ],
                    alignment=ft.CrossAxisAlignment.END
                )
            ]
