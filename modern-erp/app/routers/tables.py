from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid
import json
from datetime import datetime
from .. import db as db_module
from ..auth import verify_token
from ..validation.engine import ValidationEngine
from ..seed import s4hana

router = APIRouter(prefix="/tables", tags=["tables"])


@router.get("", dependencies=[Depends(verify_token)])
async def list_tables():
    return s4hana.get_tables()


@router.get("/{name}/schema", dependencies=[Depends(verify_token)])
async def get_schema(name: str):
    columns = s4hana.get_schema(name)
    if not columns:
        raise HTTPException(404, f"Table {name} not found")
    return {"table_name": name, "columns": columns}


@router.get("/{name}/relationships", dependencies=[Depends(verify_token)])
async def get_relationships(name: str):
    return s4hana.get_relationships(name)


@router.get("/{name}/data", dependencies=[Depends(verify_token)])
async def get_data(
    name: str,
    limit: int = Query(500, ge=1, le=5000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(db_module.get_db),
):
    try:
        count_result = await session.execute(text(f'SELECT COUNT(*) FROM "{name}"'))
        total = count_result.scalar()
        result = await session.execute(
            text(f'SELECT * FROM "{name}" LIMIT :limit OFFSET :offset'),
            {"limit": limit, "offset": offset},
        )
        rows = [dict(row._mapping) for row in result]
        return {"records": rows, "total": total, "has_more": (offset + limit) < total}
    except Exception as e:
        raise HTTPException(404, f"Table {name} not found: {str(e)}")


@router.get("/{name}/count", dependencies=[Depends(verify_token)])
async def get_count(name: str, session: AsyncSession = Depends(db_module.get_db)):
    try:
        result = await session.execute(text(f'SELECT COUNT(*) FROM "{name}"'))
        return {"table": name, "count": result.scalar()}
    except Exception as e:
        raise HTTPException(404, str(e))


@router.post("/{name}/validate", dependencies=[Depends(verify_token)])
async def validate_batch(
    name: str, payload: dict, session: AsyncSession = Depends(db_module.get_db)
):
    records = payload.get("records", [])
    engine = ValidationEngine(session)
    return await engine.validate_batch(name, records)


@router.post("/{name}/load", dependencies=[Depends(verify_token)])
async def load_records(
    name: str, payload: dict, session: AsyncSession = Depends(db_module.get_db)
):
    records = payload.get("records", [])
    mode = payload.get("mode", "upsert")
    on_error = payload.get("on_error", "reject_record")

    batch_id = str(uuid.uuid4())
    inserted = 0
    updated = 0
    rejected = 0
    errors = []

    # Validate first
    engine = ValidationEngine(session)
    validation = await engine.validate_batch(name, records)

    for i, (record, result) in enumerate(zip(records, validation["records"])):
        if result["status"] == "FAIL":
            if on_error == "reject_batch":
                await session.rollback()
                return {
                    "batch_id": batch_id,
                    "inserted": 0,
                    "updated": 0,
                    "rejected": len(records),
                    "errors": [{"index": i, "errors": result["errors"]}],
                }
            rejected += 1
            errors.append({"index": i, "errors": result["errors"]})
            continue

        # Try insert/upsert
        try:
            cols = list(record.keys())
            col_str = ", ".join(f'"{c}"' for c in cols)
            val_str = ", ".join(f":{c}" for c in cols)

            if mode == "insert":
                await session.execute(
                    text(f'INSERT INTO "{name}" ({col_str}) VALUES ({val_str})'),
                    record,
                )
                inserted += 1
            elif mode == "upsert":
                try:
                    await session.execute(
                        text(f'INSERT INTO "{name}" ({col_str}) VALUES ({val_str})'),
                        record,
                    )
                    inserted += 1
                except Exception:
                    # Record exists — count as updated
                    await session.rollback()
                    updated += 1
            elif mode == "update_only":
                updated += 1
        except Exception as e:
            if on_error == "reject_batch":
                await session.rollback()
                return {
                    "batch_id": batch_id,
                    "inserted": 0,
                    "updated": 0,
                    "rejected": len(records),
                    "errors": [{"index": i, "message": str(e)}],
                }
            rejected += 1
            errors.append({"index": i, "message": str(e)})

    await session.commit()

    # Store in load_history
    status = (
        "completed"
        if rejected == 0
        else ("failed" if inserted + updated == 0 else "partial")
    )
    try:
        await session.execute(
            text(
                "INSERT INTO load_history "
                "(batch_id, table_name, mode, status, inserted, updated, rejected, error_details, created_at) "
                "VALUES (:batch_id, :table_name, :mode, :status, :inserted, :updated, :rejected, :error_details, :created_at)"
            ),
            {
                "batch_id": batch_id,
                "table_name": name,
                "mode": mode,
                "status": status,
                "inserted": inserted,
                "updated": updated,
                "rejected": rejected,
                "error_details": json.dumps(errors),
                "created_at": datetime.utcnow().isoformat(),
            },
        )
        await session.commit()
    except Exception:
        pass

    return {
        "batch_id": batch_id,
        "inserted": inserted,
        "updated": updated,
        "rejected": rejected,
        "errors": errors,
    }


@router.get("/{name}/load-status/{batch_id}", dependencies=[Depends(verify_token)])
async def get_load_status(
    name: str, batch_id: str, session: AsyncSession = Depends(db_module.get_db)
):
    try:
        result = await session.execute(
            text(
                "SELECT * FROM load_history WHERE batch_id = :bid AND table_name = :tname"
            ),
            {"bid": batch_id, "tname": name},
        )
        row = result.fetchone()
        if not row:
            raise HTTPException(404, f"Batch {batch_id} not found")
        return dict(row._mapping)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/{name}/load-history", dependencies=[Depends(verify_token)])
async def get_load_history(name: str, session: AsyncSession = Depends(db_module.get_db)):
    try:
        result = await session.execute(
            text(
                "SELECT * FROM load_history WHERE table_name = :tname "
                "ORDER BY created_at DESC LIMIT 20"
            ),
            {"tname": name},
        )
        return [dict(row._mapping) for row in result]
    except Exception:
        return []


@router.delete("/{name}/data", dependencies=[Depends(verify_token)])
async def reset_table(name: str, session: AsyncSession = Depends(db_module.get_db)):
    try:
        await session.execute(text(f'TRUNCATE TABLE "{name}"'))
        await session.commit()
        return {
            "message": f"Table {name} truncated. Re-seed via POST /admin/reset or restart service."
        }
    except Exception as e:
        raise HTTPException(500, str(e))
