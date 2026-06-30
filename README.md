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

First startup seeds ~55,700 rows from pre-generated CSVs (takes ~30s). Subsequent starts are instant.

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

## Public Access (Cloudflare Tunnel)

The legacy ERP is exposed publicly via Cloudflare Tunnel. Two modes:

### Option A — Named tunnel with custom domain (stable URL)

Named tunnel `erp-legacy` (ID: `25ead59b-d6db-4377-82a9-2d488d72ed65`) is configured to route to `localhost:8001`. The target domain is `the-super-really-working-decho-erp.com` — this domain must be **registered and using Cloudflare nameservers** for DNS to resolve.

Once the domain is active, start with:

```bash
cloudflared tunnel run --url http://localhost:8001 erp-legacy
```

Or create `~/.cloudflared/config.yml` to avoid the `--url` flag each time:

```yaml
tunnel: erp-legacy
credentials-file: ~/.cloudflared/25ead59b-d6db-4377-82a9-2d488d72ed65.json

ingress:
  - hostname: the-super-really-working-decho-erp.com
    service: http://localhost:8001
  - service: http_status:404
```

### Option B — Quick tunnel (no domain needed, URL changes each run)

```bash
cloudflared tunnel --url http://localhost:8001
```

Cloudflare assigns a random `https://*.trycloudflare.com` URL printed in the logs. Use this for ad-hoc testing without registering a domain.

---

### Foundry REST API Connector setup

| Field | Value |
|---|---|
| Base URL | your public tunnel URL |
| Auth | Bearer token: `changeme-legacy` (set via `LEGACY_API_TOKEN`) |
| Endpoint pattern | `/tables/{TABLE_NAME}/data` |
| Pagination | Offset/limit — params: `limit`, `offset` |
| Records path | `$.records` |
| Incremental param | `since=<ISO timestamp>` |

Test the public endpoint:

```bash
# Health check (no auth)
curl https://<tunnel-url>/health

# System info
curl -H "Authorization: Bearer changeme-legacy" https://<tunnel-url>/system/info

# LFA1 sample (5 rows)
curl -H "Authorization: Bearer changeme-legacy" "https://<tunnel-url>/tables/LFA1/data?limit=5"
```

---

## Seed Data

**Legacy ERP** — pre-generated CSV files in `legacy-erp/data/seed/` (20 files, ~55,700 rows). Anchored on real SAP Datasphere bike-industry content (Trek Cycle AG, G&M Bicycle, real product codes, 5,166 sales orders). All 10 SAP data quality issues baked in.

**Modern ERP** — pre-generated CSV files in `modern-erp/data/seed/` (14 files, ~43,000 rows). Clean S/4HANA Business Partner model. Loaded from CSVs on first startup if the BusinessPartner table is empty.

**To regenerate Legacy CSVs** (e.g. after updating source data):

```bash
cd legacy-erp/data
pip install faker pandas   # dev-only deps
python3 generate_seed.py
```

Source data lives in `legacy-erp/data/source/` (gitignored — copy of SAP Datasphere sample content).

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

# Modern: validate a batch (dry-run, no insert)
curl -X POST -H "Authorization: Bearer changeme-modern" -H "Content-Type: application/json" \
  -d '{"records": [{"BP_NUMBER": "0000000001", "bp_type": "VEND", "NAME1": "Test   "}]}' \
  http://localhost:8002/tables/BusinessPartner/validate

# Modern: load records (upsert mode)
curl -X POST -H "Authorization: Bearer changeme-modern" -H "Content-Type: application/json" \
  -d '{"records": [{"BP_NUMBER": "0000001234", "bp_type": "VEND", "NAME1": "Acme", "COUNTRY": "US", "CURRENCY": "USD"}], "mode": "upsert", "on_error": "reject_record"}' \
  http://localhost:8002/tables/BusinessPartner/load

# Modern: check load batch status
curl -H "Authorization: Bearer changeme-modern" \
  http://localhost:8002/tables/BusinessPartner/load-status/<batch_id>

# Modern: wipe all domain tables (keeps schema + reference data, useful for testing)
curl -X POST -H "Authorization: Bearer changeme-modern" http://localhost:8002/admin/wipe

# Modern: full reset (drop + recreate + reseed ~43k rows)
curl -X POST -H "Authorization: Bearer changeme-modern" http://localhost:8002/admin/reset
```
