import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = "async_test"
DB_URL = os.getenv(
    "APP_DB_URL", f"postgres://postgres:postgres@127.0.0.1:5432/{DB_NAME}"
)

ALLOW_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "https://www.domain.com",
]
