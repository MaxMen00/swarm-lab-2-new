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

SERVICE_NAME = read_value(
    env_name="SERVICE_NAME",
    default="api-gateway",
)

HOSTNAME = read_value(
    env_name="HOSTNAME",
    default="unknown",
)

DATA_SERVICE_URL = read_value(
    file_path="/run/configs/data_service_url",
    env_name="DATA_SERVICE_URL",
    default="http://data-service:8000"
)

LOAD_SERVICE_URL = read_value(
    file_path="/run/configs/load_service_url",
    env_name="LOAD_SERVICE_URL",
    default="http://load-service:8000"
)

ML_SERVICE_URL = read_value(
    file_path="/run/configs/ml_service_url",
    env_name="ML_SERVICE_URL",
    default="http://ml-service:8000"
)

HTTP_TIMEOUT_SECONDS = float(read_value(
    file_path="/run/configs/http_timeout_seconds",
    env_name="HTTP_TIMEOUT_SECONDS",
    default="10"
))