from fastapi import APIRouter, Depends
from app.core.auth import authenticate_request as get_current_user
import asyncpg
import os

router = APIRouter()

@router.get("/properties")
async def get_properties(current_user = Depends(get_current_user)):
    tenant_id = current_user.tenant_id
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    try:
        rows = await conn.fetch(
            "SELECT id, name FROM properties WHERE tenant_id = $1", tenant_id
        )
        return [{"id": r["id"], "name": r["name"]} for r in rows]
    finally:
        await conn.close()