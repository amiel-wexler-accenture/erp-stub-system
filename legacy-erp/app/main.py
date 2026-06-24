from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from . import db
from .routers import tables, config


@asynccontextmanager
async def lifespan(app: FastAPI):
    from .profiles.sap_ecc import SapEccProfile
    profile = SapEccProfile()
    await profile.create_tables(db.engine)

    async with db.engine.connect() as conn:
        try:
            result = await conn.execute(text('SELECT COUNT(*) FROM "LFA1"'))
            count = result.scalar()
        except Exception:
            count = 0

    if count == 0:
        await profile.seed_data(db.engine)

    db.active_profile_id = "sap_ecc"
    db.current_profile = profile
    yield


app = FastAPI(title="Legacy ERP API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tables.router)
app.include_router(config.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/system/info")
async def system_info():
    if db.current_profile is None:
        return {
            "system_name": "ECC-1",
            "system_type": "SAP ECC",
            "version": "6.0 EHP8",
            "table_count": 0,
            "record_count": 0,
        }
    tables_meta = db.current_profile.get_tables()
    return {
        "system_name": db.current_profile.system_name,
        "system_type": db.current_profile.system_type,
        "version": db.current_profile.version,
        "table_count": len(tables_meta),
        "record_count": sum(t["record_count"] for t in tables_meta),
    }
