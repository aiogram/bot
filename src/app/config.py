from envparse import env

TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")
DOMAIN = env.str("DOMAIN", default="example.com")

REDIS_HOST = env.str("REDIS_HOST", default="localhost")
REDIS_PORT = env.int("REDIS_PORT", default=6379)
REDIS_DB_FSM = env.int("REDIS_DB_FSM", default=0)
POSTGRES_HOST = env.str("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD", default="")
POSTGRES_USER = env.str("POSTGRES_USER", default="aiogram")
POSTGRES_DB = env.str("POSTGRES_DB", default="aiogram")
POSTGRES_URI = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
