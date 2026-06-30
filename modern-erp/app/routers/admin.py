from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from .. import db as db_module
from ..auth import verify_token
from ..seed import s4hana

router = APIRouter(tags=["admin"])

_WIPEABLE_TABLES = [t["name"] for t in s4hana.get_tables() if t.get("load_supported")]


@router.post("/admin/reset", dependencies=[Depends(verify_token)])
async def reset_all():
    """Drop all tables, recreate schema, and reseed with default data."""
    try:
        await s4hana.drop_tables(db_module.engine)
        await s4hana.create_tables(db_module.engine)
        await s4hana.seed_data(db_module.engine)
        return {"message": "Database reset and reseeded successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/admin/wipe", dependencies=[Depends(verify_token)])
async def wipe_all():
    """Truncate all writable domain tables, leaving schema and reference data intact."""
    async with db_module.AsyncSessionLocal() as session:
        try:
            for table in reversed(_WIPEABLE_TABLES):
                await session.execute(text(f'TRUNCATE TABLE "{table}" CASCADE'))
            await session.commit()
            return {
                "message": "All domain tables wiped",
                "tables_cleared": _WIPEABLE_TABLES,
            }
        except Exception as e:
            await session.rollback()
            raise HTTPException(500, str(e))


@router.get("/config/profiles", dependencies=[Depends(verify_token)])
async def list_profiles():
    return [
        {
            "id": "s4hana",
            "name": "SAP S/4HANA",
            "description": "SAP S/4HANA 2023 — Business Partner unified model",
            "active": True,
        }
    ]


@router.post("/config/profiles/{profile_id}/activate", dependencies=[Depends(verify_token)])
async def activate_profile(profile_id: str):
    if profile_id != "s4hana":
        raise HTTPException(404, f"Profile {profile_id} not found")
    return {"activated": profile_id, "tables": s4hana.get_tables()}
