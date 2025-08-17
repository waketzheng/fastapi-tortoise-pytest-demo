import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = "async_test"
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_URL = os.getenv(
    "DB_URL", f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {"models": {"models": ["models"]}},
    "use_tz": os.getenv("TORTOISE_USE_TZ", "").lower()
    not in ("0", "off", "f", "false"),
    "timezone": os.getenv("TIMEZONE", "Asia/Shanghai"),
}

ALLOW_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "https://www.domain.com",
]
