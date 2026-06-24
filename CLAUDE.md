## ERP Stub System

Three fully independent services. No shared database, no shared code, no shared state. They are as separate as real SAP ECC and S/4HANA would be.

### Tech Stack
- *Backend*: Python 3.14+, FastAPI, SQLAlchemy 2.0 (async), asyncpg, PostgreSQL 16
- *Frontend*: React 18, TypeScript, Vite, CSS-in-JS via inline styles + CSS variables (no Tailwind), shadcn/ui, Legend State (reactive state), TanStack Query + Table, React Router v6
- *Infrastructure*: Docker, docker-compose (5 services: 2 APIs + 2 DBs + 1 frontend)
- *Seed Data*: Faker library, deterministic seeding (Faker.seed(42), random.seed(42))
- *Auth*: Bearer token per server, configurable via env var

---

## Server 1: Legacy ERP Server

### Persona
READ-ONLY. Pretends to be an old SAP ECC system running for 15+ years with accumulated data debt.

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | /health | Health check (no auth) |
| GET | /system/info | `{system_name, system_type, version, table_count, record_count}` |
| GET | /tables | All tables with name, domain, record_count, primary_keys |
| GET | /tables/{name}/schema | Column definitions: name, type, nullable, description, sample_values |
| GET | /tables/{name}/relationships | FK relationships to other tables |
| GET | /tables/{name}/data | Paginated extraction. Params: limit (default 500), offset (default 0), since (ISO timestamp). Response: `{records, total, has_more}` |
| GET | /tables/{name}/count | Row count for reconciliation |
| GET | /config/profiles | List available personas |
| POST | /config/profiles/{id}/activate | Switch persona (drop + recreate + reseed). Returns new table inventory. |

### `/system/info` contract
The `system_name` field must return `"ECC-1"` for the SAP ECC profile. This matches the registered system identifier in the FloX Foundry source table registry. Other profiles should use consistent identifiers (`ORACLE-EBS-1`, `DYNAMICS-AX-1`, `GENERIC-1`).

### Data Model (SAP ECC Profile — Default)

**⚠️ Column schemas are fixed by the FloX Foundry dataset schemas.** The exact column names below must be matched precisely — FloX's ingestion pipeline maps to these field names.

---

#### Vendor Master (8 tables)

**LFA1** — General Vendor Data (primary key: MANDT + LIFNR)
All 88 columns must be present. Key columns:
`MANDT, LIFNR, LAND1, NAME1, NAME2, NAME3, NAME4, ORT01, ORT02, PFACH, PSTL2, PSTLZ, REGIO, SORTL, STRAS, ADRNR, MCOD1, MCOD2, MCOD3, ANRED, BAHNS, BBBNR, BBSNR, BEGRU, BRSCH, BUBKZ, DATLT, DTAMS, DTAWS, ERDAT, ERNAM, ESRNR, KONZS, KTOKK, KUNNR, LNRZA, LOEVM, SPERR, SPERM, SPRAS, STCD1, STCD2, STKZA, STKZU, TELBX, TELF1, TELF2, TELFX, TELTX, TELX1, XCPDK, XZEMP, VBUND, FISKN, STCEG, STKZN, SPERQ, GBORT, GBDAT, SEXKZ, KRAUS, REVDB, QSSYS, KTOCK, PFORT, WERKS, LTSNA, WERKR, PLKAL, DUEFL, TXJCD, SPERZ, SCACD, SFRGR, LZONE, XLFZA, DLGRP, STCD3, STCD4, STCD5, PROFS, EMNFR, LFURL, CONFS, UPDAT, UPTIM, NODEL, PODKZB`

**LFB1** — Vendor per Company Code (PK: MANDT + LIFNR + BUKRS). ~3,000 rows.

**LFBK** — Vendor Bank Details (PK: MANDT + LIFNR + BANKS + BANKL + BANKN). ~2,000 rows.

**LFAS** — Vendor per Purchasing Org (PK: MANDT + LIFNR + EKORG). ~2,500 rows.

**LFM1** — Vendor Purchasing Data (PK: MANDT + LIFNR + EKORG). ~2,500 rows.

**LFM2** — Vendor Purchasing per Material Group (PK: MANDT + LIFNR + EKORG + WERKS). ~3,000 rows.

**LFB5** — Vendor Dunning Data per Company Code (PK: MANDT + LIFNR + BUKRS + MABER). ~1,500 rows.

**LFBW** — Vendor Withholding Tax (PK: MANDT + LIFNR + BUKRS + WITHT). ~1,000 rows.

Total vendor master: ~18,000 rows.

---

#### Customer Master (4 tables)

**KNA1** — General Customer Data (PK: MANDT + KUNNR). ~2,000 rows.
**KNB1** — Customer per Company Code (PK: MANDT + KUNNR + BUKRS). ~2,500 rows.
**KNVV** — Customer Sales Area (PK: MANDT + KUNNR + VKORG + VTWEG + SPART). ~3,000 rows.
**KNBK** — Customer Bank Details (PK: MANDT + KUNNR + BANKS + BANKL). ~2,000 rows.

Total customer master: ~9,500 rows.

---

#### Material Master (3 tables)

**MARA** — General Material Data (PK: MANDT + MATNR). ~2,000 rows.
**MARC** — Material per Plant (PK: MANDT + MATNR + WERKS). ~5,000 rows.
**MAKT** — Material Descriptions (PK: MANDT + MATNR + SPRAS). ~3,000 rows.

Total material master: ~10,000 rows.

---

#### Finance (3 tables)

**SKA1** — G/L Account Chart of Accounts (PK: MANDT + KTOPL + SAKNR). ~400 rows.
**SKAT** — G/L Account Descriptions (PK: MANDT + SPRAS + KTOPL + SAKNR). ~500 rows.
**CSKS** — Cost Centers (PK: MANDT + KOSTL + DATBI). ~300 rows.

Total finance: ~1,200 rows.

---

#### Purchasing (2 tables)

**EKKO** — Purchase Order Headers (PK: MANDT + EBELN). ~5,000 rows.
**EKPO** — Purchase Order Line Items (PK: MANDT + EBELN + EBELP). ~15,000 rows.

Total purchasing: ~20,000 rows.

---

### Data Quality Issues (CRITICAL — this is the whole point)

Deliberately inject all 10 problems. Without them, the migration demo has no drama:

1. *Trailing spaces* (~20% of STRING fields): `"ACME Corp   "`
2. *Inconsistent nulls*: Mix of SQL NULL, `""`, and `"N/A"` across different rows for the same logical "missing" concept
3. *Near-duplicate records* (~2%): Same company name, slight address variation — different LIFNR, same NAME1
4. *Orphan foreign keys* (~1%): EKKO rows where LIFNR has no matching LFA1 row
5. *Invalid codes* (~3%): LAND1 values not in ISO-3166, BRSCH values not in valid industry code list
6. *Dates as strings*: ERDAT stored as `"20180315"` or `"15.03.2018"` not ISO dates
7. *Unicode edge cases*: NAME1 values containing ü, é, ñ, 日本語, Arabic script
8. *Blocked/deleted markers* (~5%): `LOEVM="X"` on LFA1 rows — must be filtered before migration
9. *Wrong client values* (~0.5%): `MANDT="200"` mixed into MANDT="100" partition
10. *Leading-zero padded IDs*: LIFNR is always 10-char zero-padded: `"0000001234"`

Row-level targeting: each quality issue should be applied at the row level during seeding, not uniformly. A given row might have 0, 1, or 2 issues — this makes the distribution realistic and forces real per-record handling.

---

### Profile Switching

When activated: drop all tables → create new schema → reseed. Returns new table inventory.

**Oracle EBS profile:** `AP_SUPPLIERS, AR_CUSTOMERS, MTL_SYSTEM_ITEMS_B, PO_HEADERS_ALL, GL_CODE_COMBINATIONS`. Sequence-based integer PKs. Oracle naming (VENDOR_ID, CREATION_DATE, ORG_ID). System name: `"ORACLE-EBS-1"`.

**Dynamics AX profile:** `VendTable, CustTable, InventTable, PurchTable, LedgerTable`. PascalCase columns (AccountNum, VendGroup, DataAreaId). UUID RecId columns. System name: `"DYNAMICS-AX-1"`.

**Generic Legacy profile:** `vendors, customers, materials, purchase_orders`. Snake_case columns. System name: `"GENERIC-1"`.

---

## Server 2: Modern ERP Server

### Persona
READ + WRITE. Pretends to be a modern S/4HANA-style system — clean data model, strict validation, proper types.

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | /health | Health check (no auth) |
| GET | /system/info | `{system_name, api_version, supports_validation, max_batch_size}` |
| GET | /tables | All tables with `load_supported`, `validate_supported` flags |
| GET | /tables/{name}/schema | Column definitions WITH validation rules per column |
| GET | /tables/{name}/relationships | FK relationships |
| GET | /tables/{name}/data | Paginated read |
| GET | /tables/{name}/count | Row count |
| POST | /tables/{name}/validate | Validate batch. Returns per-record results + summary. Does NOT insert. |
| POST | /tables/{name}/load | Load records. Modes: insert / upsert / update_only. Returns batch_id. |
| GET | /tables/{name}/load-status/{batch_id} | Check load batch status |
| GET | /tables/{name}/load-history | Recent load operations |
| DELETE | /tables/{name}/data | Reset table to seed state |
| POST | /admin/reset | Reset entire DB to seed state |
| GET | /config/profiles | List target profiles |
| POST | /config/profiles/{id}/activate | Switch target persona |

### Data Model (S/4HANA Profile — Default)

**Business Partner** (6 tables — the key transformation challenge: vendors + customers unified):
- `BusinessPartner` — master (BP_NUMBER PK, bp_type: VEND/CUST/BOTH)
- `BPRole` — role assignments
- `BPBankAccount` — bank details
- `BPAddress` — address
- `BPCompanyCode` — company code extension
- `BPPurchasingOrg` — purchasing org extension

~1,080 rows total.

**Product** (3 tables):
- `Product` — master (PRODUCT_NUMBER PK, clean types)
- `ProductPlant` — plant-level data
- `ProductValuation` — valuation area data

~800 rows total.

**Finance** (3 tables):
- `GLAccount`, `CostCenter`, `ProfitCenter`

~180 rows total.

**Purchasing** (2 tables):
- `PurchaseOrder`, `PurchaseOrderItem`

~400 rows total.

**Reference tables** (6 tables — enforce FK integrity during validation):
- `Country` — 249 ISO-3166 alpha-2 codes
- `Currency` — 180 ISO-4217 codes
- `UnitOfMeasure` — standard UoM list
- `CompanyCode`, `Plant`, `PurchasingOrganization` — org structure

### Validation Engine

`POST /tables/{name}/validate` — validates a batch, returns per-record results, inserts nothing.

Rules:
- Required fields: null/empty on non-nullable columns → ERROR
- Pattern: BP_NUMBER must match `^[0-9]{10}$`
- Allowed values: bp_type must be `VEND`, `CUST`, or `BOTH`
- ISO codes: COUNTRY and CURRENCY validated against reference tables
- FK integrity: referenced PKs must exist in PostgreSQL
- Unique: no duplicate PKs within batch or vs. existing rows
- String hygiene: no trailing spaces or control characters
- Date reasonableness: not in the far future (> today + 1 year)
- Cross-field: if bp_type=VEND, BPPurchasingOrg data expected

Response shape:
```json
{
  "batch_size": 100,
  "passed": 82,
  "failed": 18,
  "records": [
    {"index": 0, "status": "PASS", "errors": [], "warnings": []},
    {"index": 1, "status": "FAIL", "errors": [{"rule": "required", "field": "BP_NUMBER", "message": "..."}], "warnings": []}
  ],
  "summary": {
    "by_rule": {"required": 5, "pattern": 3, "iso_code": 4, "string_hygiene": 6},
    "by_column": {"BP_NUMBER": 8, "COUNTRY": 4, "NAME1": 6}
  }
}
```

### Load Engine

`POST /tables/{name}/load`

```json
{
  "records": [...],
  "mode": "upsert",       // insert | upsert | update_only
  "on_error": "reject_record"  // reject_record | reject_batch | log_and_continue
}
```

Returns:
```json
{
  "batch_id": "uuid",
  "inserted": 70,
  "updated": 12,
  "rejected": 0,
  "errors": []
}
```

Load results stored in internal `load_history` table.

### Pre-Seeded State

~500 records already loaded (simulates a prior migration cycle). ~10% overlap with legacy data by name/tax ID to test upsert deduplication. Seeded deterministically.

---

## ERP Admin UI (React Frontend)

### Purpose
Visual credibility for demos. Makes the two API servers look like real ERP systems. This is NOT the product — FloX is the product.

### Design
- Legacy side: amber/orange theme (`#f59e0b` base). "Old, warning" aesthetic.
- Modern side: blue/green theme (`#3b82f6` base). "Clean, modern" aesthetic.
- Demo-optimized: key numbers large, data quality issues visually highlighted. Looks good at 1920×1080.

### Pages

**`/`** — Side-by-side overview: both systems' name/type/version/table count/record count/active profile. Visual emphasis on the gap.

**`/legacy`** — System info card, profile switcher, table list grouped by domain. Click table to explore.

**`/legacy/tables/:name`** — Tabs:
- Schema: columns with types + descriptions
- Data: paginated grid. DQ visual callouts:
  - Trailing space cells: amber dot marker (⚠ shown as overlay)
  - NULL / "" / "N/A" values: grey `NULL` badge
  - LOEVM="X" rows: red row background
- Relationships: FK list

**`/modern`** — Same layout with blue theme. Extra "Recent Loads" section.

**`/modern/tables/:name`** — Tabs:
- Schema: columns + validation rules as colored badges (REQUIRED red, PATTERN yellow, ISO_CODE blue)
- Data: clean grid
- Load History: batch operations list

**`/load-manager`** — All load batches across all tables. Status badges (completed/partial/failed). Drill into rejected records and error details.

**`/config`** — Profile switchers for both systems, reset buttons, connection health indicators.

### State Management
Use Legend State for reactive global state (API connection status, active profiles). TanStack Query for server data caching. Avoid prop drilling.

---

## Infrastructure

### Docker Compose

| Service | Image | Port | Purpose |
|---|---|---|---|
| legacy-db | postgres:16-alpine | 5433 | Legacy DB |
| modern-db | postgres:16-alpine | 5434 | Modern DB |
| legacy-erp | Custom FastAPI | 8001 | Legacy API |
| modern-erp | Custom FastAPI | 8002 | Modern API |
| erp-admin-ui | Custom nginx+React | 3000 | Frontend |

API servers healthcheck-gated on their DB. Frontend depends on both APIs.

### File Structure

```
erp-stub-system/
├── legacy-erp/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── app/
│       ├── main.py
│       ├── auth.py
│       ├── db.py
│       ├── schemas.py          # Pydantic response models
│       ├── routers/
│       │   ├── tables.py
│       │   └── config.py
│       └── profiles/
│           ├── base.py         # abstract profile interface
│           ├── sap_ecc.py      # schema + seed (authoritative: matches LFA1..LFBW)
│           ├── oracle_ebs.py
│           ├── dynamics_ax.py
│           └── generic.py
├── modern-erp/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── app/
│       ├── main.py
│       ├── auth.py
│       ├── db.py
│       ├── schemas.py
│       ├── routers/
│       │   ├── tables.py       # includes validate + load
│       │   └── admin.py
│       ├── validation/
│       │   └── engine.py       # all validation rules
│       └── seed/
│           └── s4hana.py
├── erp-admin-ui/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── api/                # typed Axios clients
│       ├── pages/
│       └── components/
├── docker-compose.yml
└── .env.example
```

### Environment Variables

```env
# Legacy server
LEGACY_API_TOKEN=changeme-legacy
DATABASE_URL=postgresql+asyncpg://postgres:postgres@legacy-db:5432/legacy

# Modern server
MODERN_API_TOKEN=changeme-modern
DATABASE_URL=postgresql+asyncpg://postgres:postgres@modern-db:5432/modern

# Frontend (Vite)
VITE_LEGACY_API_URL=http://localhost:8001
VITE_LEGACY_TOKEN=changeme-legacy
VITE_MODERN_API_URL=http://localhost:8002
VITE_MODERN_TOKEN=changeme-modern
```

### Seed Data
- Faker with mixed locales: en_US, en_GB, de_DE, fr_FR, ja_JP, pt_BR
- `Faker.seed(42)`, `random.seed(42)` — deterministic, same data every run
- Bulk INSERT (not row-by-row) for performance, indexes created after seeding
- Industry domains: manufacturing, retail, logistics, chemicals, automotive, electronics, pharma
- Cross-server correlation: ~10% of legacy company names/tax IDs appear as existing BPs in modern server (tests upsert dedup)

### Auth
Bearer token per server from env var. Return `401` with `{"detail": "Unauthorized"}` if missing or invalid. Both servers enable CORS for all origins (`*`) — this is a demo environment, security is not a concern.

### Deployment (TBC)


---

## Key Design Principles

1. *The data quality gap IS the demo* — without messy legacy data and strict target validation, FloX has nothing to solve
2. *Realistic enough for ERP consultants* — SAP field names (LFA1, LIFNR, MANDT) must be recognizable to someone who's worked with real SAP
3. *Column schemas are locked by Foundry* — the LFA1 schema in Foundry has 88 columns with exact SAP names; the seed generator must match these exactly
4. *Profile-switchable* — same API contract, completely different data model underneath
5. *Deterministic seeds* — demos must be exactly reproducible
6. *Frontend is window dressing* — FloX/Foundry is where the real work happens
7. *System name matters* — `/system/info` must return `system_name: "ECC-1"` for SAP profile to match FloX's registered source config
