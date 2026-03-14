import os


POSTGRES_DB=os.getenv("POSTGRES_DB")
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

SERVICE_NAME = os.getenv("SERVICE_NAME", "backend")
GPU_NODE = os.getenv("GPU_NODE", "false").lower() == "true"
HOSTNAME = os.getenv("HOSTNAME", "unknown")

DB_INIT_RETRIES = int(os.getenv("DB_INIT_RETRIES", "30"))
DB_INIT_DELAY_SECONDS = float(os.getenv("DB_INIT_DELAY_SECONDS", "2"))

DB_POOL_MIN_SIZE = int(os.getenv("DB_POOL_MIN_SIZE", "1"))
DB_POOL_MAX_SIZE = int(os.getenv("DB_POOL_MAX_SIZE", "10"))
DB_COMMAND_TIMEOUT = float(os.getenv("DB_COMMAND_TIMEOUT", "30"))