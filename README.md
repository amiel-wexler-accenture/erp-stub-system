# erp-stub-system

Two independent ERP stub services (Legacy + Modern) plus a React admin UI — used to demo data migration with FloX Foundry.

---

## Running Locally (no Docker)

### Prerequisites

- Python 3.12+
- Node 22+
- Two PostgreSQL 16 databases (or use the one-liner below)

**Quick Postgres setup using Docker (DBs only):**
```bash
docker run -d --name legacy-db -e POSTGRES_DB=legacy -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5433:5432 postgres:16-alpine
docker run -d --name modern-db -e POSTGRES_DB=modern -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5434:5432 postgres:16-alpine
```

---

### Legacy ERP (port 8001)

```bash
cd legacy-erp
pip install -e .

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/legacy \
LEGACY_API_TOKEN=changeme-legacy \
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

First startup seeds ~58,000 rows (takes ~30s). Subsequent starts are instant.

---

### Modern ERP (port 8002)

```bash
cd modern-erp
pip install -e .

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5434/modern \
MODERN_API_TOKEN=changeme-modern \
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

---

### React Admin UI (port 5173)

```bash
cd erp-admin-ui
npm install

VITE_LEGACY_API_URL=http://localhost:8001 \
VITE_LEGACY_TOKEN=changeme-legacy \
VITE_MODERN_API_URL=http://localhost:8002 \
VITE_MODERN_TOKEN=changeme-modern \
npm run dev
```

Open http://localhost:5173

---

## Running with Docker

```bash
cp .env.example .env
docker compose up --build
```

| Service    | URL                    |
|------------|------------------------|
| Legacy ERP | http://localhost:8001  |
| Modern ERP | http://localhost:8002  |
| Admin UI   | http://localhost:3000  |

---

## Quick API checks

```bash
# Health (no auth)
curl http://localhost:8001/health
curl http://localhost:8002/health

# System info
curl -H "Authorization: Bearer changeme-legacy" http://localhost:8001/system/info
curl -H "Authorization: Bearer changeme-modern" http://localhost:8002/system/info

# Legacy: list tables
curl -H "Authorization: Bearer changeme-legacy" http://localhost:8001/tables

# Legacy: LFA1 data (check DQ issues)
curl -H "Authorization: Bearer changeme-legacy" "http://localhost:8001/tables/LFA1/data?limit=20"

# Legacy: switch to Oracle EBS profile
curl -X POST -H "Authorization: Bearer changeme-legacy" http://localhost:8001/config/profiles/oracle_ebs/activate

# Modern: validate a record
curl -X POST -H "Authorization: Bearer changeme-modern" -H "Content-Type: application/json" \
  -d '{"records": [{"BP_NUMBER": "0000000001", "bp_type": "VEND", "NAME1": "Test   "}]}' \
  http://localhost:8002/tables/BusinessPartner/validate
```
