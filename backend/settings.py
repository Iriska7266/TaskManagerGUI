import os
from pathlib import Path


data_dir = os.getenv("FLET_APP_STORAGE_DATA")

if data_dir:
    data_dir = Path(data_dir)
else:
    data_dir = Path(os.getenv("APPDATA")) / "TaskManager" / "data"
os.makedirs(data_dir, exist_ok=True)

LOCAL_USER_DATA = data_dir / "local_user_data.dat"
DOTENV_PATH = data_dir / ".env"
SETTINGS_PATH = data_dir / "settings.dat"