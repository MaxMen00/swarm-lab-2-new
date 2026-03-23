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


GPU_NODE = read_value(
    file_path="/run/configs/gpu_node",
    env_name="GPU_NODE",
    default="false"
).lower() == "true"

SERVICE_NAME = read_value(
    file_path="/run/configs/service_name",
    env_name="SERVICE_NAME",
    default="ml-service"
)

HOSTNAME = read_value(
    env_name="HOSTNAME",
    default="unknown"
)

REDIS_HOST = read_value(
    file_path="/run/configs/redis_host",
    env_name="REDIS_HOST",
    default="redis",
)

REDIS_PORT = int(
    read_value(
        file_path="/run/configs/redis_port",
        env_name="REDIS_PORT",
        default="6379",
    )
)

REDIS_DB = int(
    read_value(
        file_path="/run/configs/redis_db",
        env_name="REDIS_DB",
        default="0",
    )
)

REDIS_CACHE_TTL_SECONDS = int(
    read_value(
        file_path="/run/configs/redis_cache_ttl_seconds",
        env_name="REDIS_CACHE_TTL_SECONDS",
        default="300",
    )
)

REDIS_USERNAME = read_value(
    file_path="/run/secrets/redis_app_username",
    env_name="REDIS_USERNAME",
    required=True
)

REDIS_APP_PASSWORD = read_value(
    file_path="/run/secrets/redis_app_password",
    env_name="REDIS_APP_PASSWORD",
    required=True
)