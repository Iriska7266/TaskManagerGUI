from dataclasses import dataclass


@dataclass
class DotenvSettingsPageStyle:
    title_font_size: int = 25


@dataclass
class AuthPageStyle:
    greet_size: int = 25
    greet_margin: int = 20

    login_width: int = 300
    password_width: int = 300
    go_to_dotenv_settings_width: int = 300


@dataclass
class TasksPageStyle:
    # Task table
    task_table_height: int = 780
    task_table_width: int = 1160

    # Notification
    max_title_len_for_notif: int = 45

    # Cards
    preview_card_width: int = 250
    preview_card_height: int = 350
    max_preview_title_len: int = 30
    max_preview_content_len: int = 80
    preview_title_size: int = 24
    preview_content_size: int = 20

    # Dialog task window
    dialog_card_width: int = 600
    # dialog height is adaptive to task content
    dialog_title_size: int = 24
    dialog_content_size: int = 20
    date_field_width: int = 130
    time_field_width: int = 105

    # Void tasks table message
    void_tasks_msg_size: int = 30

@dataclass
class NotificationStyle:
    narrow_message_width: int = 300
    broad_message_width: int = 700

    small_text_len = 30
    long_text_len = 85
