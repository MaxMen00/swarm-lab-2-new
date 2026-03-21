from datetime import datetime, timezone

from app.config import HOSTNAME, SERVICE_NAME
from app.clients.data_service import DataServiceClient
from app.clients.load_service import LoadServiceClient
from app.clients.ml_service import MlServiceClient


async def build_info() -> dict:
    return {
        "service": SERVICE_NAME,
        "hostname": HOSTNAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


async def build_info_services(
    data_client: DataServiceClient,
    load_client: LoadServiceClient,
    ml_client: MlServiceClient,
) -> dict:
    data_info = {
        "status": "down",
        "hostname": "unknown",
        "db_status": "not-ready",
    }
    try:
        response = await data_client.health()
        data_info = {
            "status": response.get("status", "ok"),
            "hostname": response.get("hostname", "unknown"),
            "db_status": response.get("db_status", "not-ready"),
        }
    except Exception:
        pass

    load_info = {
        "status": "down",
        "hostname": "unknown",
    }
    try:
        response = await load_client.health()
        load_info = {
            "status": response.get("status", "ok"),
            "hostname": response.get("hostname", "unknown"),
        }
    except Exception:
        pass

    ml_info = {
        "status": "down",
        "hostname": "unknown",
    }
    try:
        response = await ml_client.health()
        ml_info = {
            "status": response.get("status", "ok"),
            "hostname": response.get("hostname", "unknown"),
        }
    except Exception:
        pass

    return {
        "service": SERVICE_NAME,
        "hostname": HOSTNAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "upstreams": {
            "data-service": data_info,
            "load-service": load_info,
            "ml-service": ml_info,
        },
    }