from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from . import db as db_module
from .routers import tables, admin
from .seed import s4hana


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables and seed if empty
    await s4hana.create_tables(db_module.engine)
    count = 0
    async with db_module.engine.connect() as conn:
        try:
            result = await conn.execute(text('SELECT COUNT(*) FROM "BusinessPartner"'))
            count = result.scalar()
        except Exception:
            count = 0
    if count == 0:
        await s4hana.seed_data(db_module.engine)
    yield


app = FastAPI(title="Modern ERP API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tables.router)
app.include_router(admin.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/system/info")
async def system_info():
    return {
        "system_name": "S4H-1",
        "api_version": "2024.1",
        "supports_validation": True,
        "max_batch_size": 1000,
    }
