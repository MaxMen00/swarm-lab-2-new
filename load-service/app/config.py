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
    default="load-service",
)

HOSTNAME = read_value(
    env_name="HOSTNAME",
    default="unknown",
)