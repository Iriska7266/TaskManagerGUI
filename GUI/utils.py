import pytz
import flet as ft

from datetime import datetime

from backend.dto import TaskDTO
from GUI.gui_configuration import NotificationStyle


def cut_str(text: str, max_len: int) -> str:
    return text[:max_len-3] + "..." if len(text) > max_len else text


def get_local_datetime(dt: datetime) -> datetime:
    """Copied from Flet GH repository, Issue #6145.
    Convert datetime (potentially in UTC) to local date.

    This handles the case where Flet's DatePicker returns datetime in UTC,
    and we need to convert it to the user's local timezone before extracting the date.
    """
    if dt.tzinfo is not None:
        # Convert to local timezone before extracting date
        return dt.astimezone()
    return dt

def get_task_status(task: TaskDTO) -> str:
    """Returns 'completed', 'overdue' or 'in process' depending on task's status"""
    if task.status:
        return "completed"
    else:
        cur_time = get_local_datetime(datetime.now(pytz.UTC)) if task.expires_at.tzinfo else datetime.now()
        deadline = get_local_datetime(task.expires_at)
        if deadline < cur_time:
            return "overdue"
        else:
            return "in process"

def show_snack_message(page: ft.Page, m_text: str, m_type: str="info") -> None:
    message_types = {'info': {"icon": ft.Icons.INFO_OUTLINED,
                              "color": ft.Colors.GREY,
                              "border_color": ft.Colors.BLUE_GREY},
                        'success': {"icon": ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                                    "color": ft.Colors.GREEN_700,
                                    "border_color": ft.Colors.GREEN},
                        'error': {"icon": ft.Icons.CANCEL_OUTLINED,
                                  "color": ft.Colors.RED_500,
                                  "border_color": ft.Colors.RED_700}
                     }
    if not m_type in message_types.keys():
        raise ValueError("Not supported message type! Allowed are: 'info', 'success', 'error'")

    config = message_types[m_type]
    is_long_message = False
    l = len(m_text)
    if l > NotificationStyle.small_text_len:
        if l > NotificationStyle.long_text_len:
            m_text = m_text[:NotificationStyle.long_text_len-3] + "..."
        is_long_message = True

    page.show_dialog(
        ft.SnackBar(
            content=ft.Row(
                controls=[
                    ft.Icon(config['icon'], color=config['color']),
                    ft.Text(m_text, color=ft.Colors.WHITE)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            show_close_icon=True,
            close_icon_color=ft.Colors.WHITE,
            behavior=ft.SnackBarBehavior.FLOATING,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            duration=3500,
            bgcolor=ft.Colors.SURFACE,
            width=NotificationStyle.broad_message_width if is_long_message else NotificationStyle.narrow_message_width,
            shape=ft.RoundedRectangleBorder(
                radius=10,
                side=ft.BorderSide(color=config['border_color'])
            )
        )
    )