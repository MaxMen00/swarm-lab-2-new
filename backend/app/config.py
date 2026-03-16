import os
from pathlib import Path


def read_value(
    *,
    file_path: str | None = None,
    env_name: str | None = None,
    default: str | None = None,
    required: bool = False,
) -> str | None:
    if file_path:
        path = Path(file_path)
        if path.exists():
            value = path.read_text(encoding="utf-8").strip()
            if value:
                return value

    if env_name:
        value = os.getenv(env_name)
        if value is not None and value != "":
            return value

    if default is not None:
        return default

    if required:
        source = file_path or env_name or "unknown source"
        raise RuntimeError(f"Required config value is missing: {source}")

    return None


POSTGRES_DB = read_value(
    file_path="/run/configs/pg_db_name",
    env_name="POSTGRES_DB",
    required=True,
)

POSTGRES_USER = read_value(
    file_path="/run/configs/pg_db_user",
    env_name="POSTGRES_USER",
    required=True,
)

POSTGRES_PASSWORD = read_value(
    file_path="/run/secrets/pg_password",
    env_name="POSTGRES_PASSWORD",
    required=True,
)

POSTGRES_HOST = read_value(
    env_name="POSTGRES_HOST",
    default="db",
)

POSTGRES_PORT = int(
    read_value(
        env_name="POSTGRES_PORT",
        default="5432",
    )
)

SERVICE_NAME = read_value(
    env_name="SERVICE_NAME",
    default="backend",
)

GPU_NODE = read_value(
    env_name="GPU_NODE",
    default="false",
).lower() == "true"

HOSTNAME = read_value(
    env_name="HOSTNAME",
    default="unknown",
)

DB_INIT_RETRIES = int(
    read_value(
        env_name="DB_INIT_RETRIES",
        default="30",
    )
)

DB_INIT_DELAY_SECONDS = float(
    read_value(
        env_name="DB_INIT_DELAY_SECONDS",
        default="2",
    )
)

DB_POOL_MIN_SIZE = int(
    read_value(
        env_name="DB_POOL_MIN_SIZE",
        default="1",
    )
)

DB_POOL_MAX_SIZE = int(
    read_value(
        env_name="DB_POOL_MAX_SIZE",
        default="10",
    )
)

DB_COMMAND_TIMEOUT = float(
    read_value(
        env_name="DB_COMMAND_TIMEOUT",
        default="30",
    )
)