from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from .. import db
from ..auth import verify_token

router = APIRouter(prefix="/tables", tags=["tables"])


@router.get("", dependencies=[Depends(verify_token)])
async def list_tables():
    if db.current_profile is None:
        raise HTTPException(503, "No profile loaded")
    return db.current_profile.get_tables()


@router.get("/{name}/schema", dependencies=[Depends(verify_token)])
async def get_schema(name: str):
    if db.current_profile is None:
        raise HTTPException(503, "No profile loaded")
    schema = db.current_profile.get_schema(name.upper())
    if not schema or not schema.get("columns"):
        raise HTTPException(404, f"Table {name} not found")
    return schema


@router.get("/{name}/relationships", dependencies=[Depends(verify_token)])
async def get_relationships(name: str):
    if db.current_profile is None:
        raise HTTPException(503, "No profile loaded")
    return db.current_profile.get_relationships(name.upper())


@router.get("/{name}/data", dependencies=[Depends(verify_token)])
async def get_data(
    name: str,
    limit: int = Query(500, ge=1, le=5000),
    offset: int = Query(0, ge=0),
    since: Optional[str] = Query(None),
    session: AsyncSession = Depends(db.get_db),
):
    table_name = name.upper()
    try:
        count_result = await session.execute(text(f'SELECT COUNT(*) FROM "{table_name}"'))
        total = count_result.scalar()
        result = await session.execute(
            text(f'SELECT * FROM "{table_name}" LIMIT :limit OFFSET :offset'),
            {"limit": limit, "offset": offset},
        )
        rows = [dict(row._mapping) for row in result]
        return {"records": rows, "total": total, "has_more": (offset + limit) < total}
    except Exception as e:
        raise HTTPException(404, f"Table {table_name} not found or error: {str(e)}")


@router.get("/{name}/count", dependencies=[Depends(verify_token)])
async def get_count(name: str, session: AsyncSession = Depends(db.get_db)):
    try:
        result = await session.execute(text(f'SELECT COUNT(*) FROM "{name.upper()}"'))
        return {"table": name.upper(), "count": result.scalar()}
    except Exception as e:
        raise HTTPException(404, f"Table {name} not found: {str(e)}")
