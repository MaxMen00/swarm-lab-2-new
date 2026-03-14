import asyncpg
from fastapi import APIRouter, Depends, HTTPException

from app.config import HOSTNAME
from app.deps import get_db_conn
from app.schemas import CreateItemResponse, ItemIn, ItemsListResponse

router = APIRouter(tags=["items"])


@router.get("/api/items", response_model=ItemsListResponse)
async def get_items(conn: asyncpg.Connection = Depends(get_db_conn)):
    try:
        rows = await conn.fetch(
            """
            SELECT id, text, created_at
            FROM items
            ORDER BY id DESC
            """
        )
        return {
            "backend_hostname": HOSTNAME,
            "items": [
                {
                    "id": row["id"],
                    "text": row["text"],
                    "created_at": row["created_at"],
                }
                for row in rows
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}") from e


@router.post("/api/items", response_model=CreateItemResponse)
async def create_item(
    item: ItemIn,
    conn: asyncpg.Connection = Depends(get_db_conn),
):
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO items (text)
            VALUES ($1)
            RETURNING id, text, created_at
            """,
            item.text,
        )
        if row is None:
            raise HTTPException(status_code=500, detail="Insert failed")

        return {
            "backend_hostname": HOSTNAME,
            "item": {
                "id": row["id"],
                "text": row["text"],
                "created_at": row["created_at"],
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}") from e