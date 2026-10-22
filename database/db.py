import os

import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import load_dotenv

from database.orm import Base
from backend.settings import DOTENV_PATH


load_dotenv(DOTENV_PATH)
db_url = os.getenv("DB_URL")

try:
    psql_engine = create_engine(db_url)
    Base.metadata.create_all(psql_engine)
    Session = sessionmaker(psql_engine)
except Exception:
    raise ConnectionError("Incorrect DB URL!")

@contextmanager
def get_db() -> sqlalchemy.orm.Session:
    db = Session()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()