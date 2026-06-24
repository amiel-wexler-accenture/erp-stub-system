"""
S/4HANA seed data module for the modern ERP stub.

Creates and seeds 19 tables deterministically (Faker.seed(42), random.seed(42)).
All inserts are bulk in batches of 500 using SQLAlchemy Core.
"""

from faker import Faker
import random
import uuid
from datetime import date, timedelta
from sqlalchemy import Table, Column, String, Integer, Numeric, MetaData, text
from sqlalchemy.ext.asyncio import AsyncEngine

# ---------------------------------------------------------------------------
# MetaData
# ---------------------------------------------------------------------------

metadata = MetaData()

# ---------------------------------------------------------------------------
# Reference data constants
# ---------------------------------------------------------------------------

COUNTRIES = [
    ("US", "United States"), ("GB", "United Kingdom"), ("DE", "Germany"),
    ("FR", "France"), ("JP", "Japan"), ("BR", "Brazil"), ("CN", "China"),
    ("IN", "India"), ("CA", "Canada"), ("AU", "Australia"), ("MX", "Mexico"),
    ("IT", "Italy"), ("ES", "Spain"), ("NL", "Netherlands"), ("SE", "Sweden"),
    ("NO", "Norway"), ("DK", "Denmark"), ("FI", "Finland"), ("CH", "Switzerland"),
    ("AT", "Austria"), ("BE", "Belgium"), ("PL", "Poland"), ("CZ", "Czech Republic"),
    ("PT", "Portugal"), ("RU", "Russia"), ("ZA", "South Africa"),
    ("KR", "South Korea"), ("SG", "Singapore"), ("HK", "Hong Kong"),
    ("TW", "Taiwan"), ("AR", "Argentina"), ("CL", "Chile"), ("CO", "Colombia"),
    ("PE", "Peru"), ("VE", "Venezuela"), ("EG", "Egypt"), ("NG", "Nigeria"),
    ("KE", "Kenya"), ("SA", "Saudi Arabia"), ("AE", "United Arab Emirates"),
    ("IL", "Israel"), ("TR", "Turkey"), ("TH", "Thailand"), ("MY", "Malaysia"),
    ("ID", "Indonesia"), ("PH", "Philippines"), ("VN", "Vietnam"),
    ("PK", "Pakistan"), ("BD", "Bangladesh"), ("NZ", "New Zealand"),
]

COUNTRY_CODES = [c[0] for c in COUNTRIES]

CURRENCIES = [
    ("USD", "US Dollar"), ("EUR", "Euro"), ("GBP", "British Pound"),
    ("JPY", "Japanese Yen"), ("BRL", "Brazilian Real"), ("CNY", "Chinese Yuan"),
    ("INR", "Indian Rupee"), ("CAD", "Canadian Dollar"),
    ("AUD", "Australian Dollar"), ("MXN", "Mexican Peso"),
    ("CHF", "Swiss Franc"), ("SEK", "Swedish Krona"),
    ("NOK", "Norwegian Krone"), ("DKK", "Danish Krone"),
    ("PLN", "Polish Zloty"), ("CZK", "Czech Koruna"),
    ("HUF", "Hungarian Forint"), ("RUB", "Russian Ruble"),
    ("ZAR", "South African Rand"), ("KRW", "South Korean Won"),
    ("SGD", "Singapore Dollar"), ("HKD", "Hong Kong Dollar"),
    ("TWD", "Taiwan Dollar"), ("ARS", "Argentine Peso"),
    ("CLP", "Chilean Peso"), ("COP", "Colombian Peso"),
    ("SAR", "Saudi Riyal"), ("AED", "UAE Dirham"),
    ("TRY", "Turkish Lira"), ("THB", "Thai Baht"),
]

CURRENCY_CODES = [c[0] for c in CURRENCIES]

UOMS = [
    ("EA", "Each"), ("KG", "Kilogram"), ("G", "Gram"), ("LB", "Pound"),
    ("OZ", "Ounce"), ("L", "Litre"), ("ML", "Millilitre"), ("M", "Metre"),
    ("CM", "Centimetre"), ("MM", "Millimetre"), ("M2", "Square Metre"),
    ("M3", "Cubic Metre"), ("PC", "Piece"), ("BOX", "Box"), ("PAL", "Pallet"),
    ("ROL", "Roll"), ("SET", "Set"), ("PR", "Pair"), ("DZ", "Dozen"),
    ("HR", "Hour"),
]

UOM_CODES = [u[0] for u in UOMS]

COMPANY_CODES = [
    ("1000", "Global Corp US", "US", "USD"),
    ("2000", "Global Corp DE", "DE", "EUR"),
    ("3000", "Global Corp GB", "GB", "GBP"),
    ("4000", "Global Corp JP", "JP", "JPY"),
    ("5000", "Global Corp BR", "BR", "BRL"),
]

PLANTS = [
    ("P001", "Plant US East",   "1000", "US"),
    ("P002", "Plant US West",   "1000", "US"),
    ("P003", "Plant Germany",   "2000", "DE"),
    ("P004", "Plant France",    "2000", "FR"),
    ("P005", "Plant UK",        "3000", "GB"),
    ("P006", "Plant Japan",     "4000", "JP"),
    ("P007", "Plant Brazil",    "5000", "BR"),
    ("P008", "Plant Canada",    "1000", "CA"),
    ("P009", "Plant Australia", "1000", "AU"),
    ("P010", "Plant Mexico",    "1000", "MX"),
]

PLANT_CODES = [p[0] for p in PLANTS]

PURCH_ORGS = [
    ("PO01", "Global Procurement US", "1000"),
    ("PO02", "Global Procurement DE", "2000"),
    ("PO03", "Global Procurement GB", "3000"),
    ("PO04", "Global Procurement JP", "4000"),
    ("PO05", "Global Procurement BR", "5000"),
]

PURCH_ORG_CODES = [p[0] for p in PURCH_ORGS]

COMPANY_CODE_KEYS = [c[0] for c in COMPANY_CODES]

# Names that overlap with legacy system (~10% of BPs)
LEGACY_OVERLAP_NAMES = [
    "ACME Corp", "Global Industries", "Tech Solutions", "Premier Supplies",
    "Alpha Manufacturing", "Beta Logistics", "Delta Chemicals", "Omega Electronics",
    "Sigma Pharma", "Gamma Retail", "Pacific Traders", "Atlantic Distributors",
    "Continental Materials", "Nordic Supplies", "Eastern Holdings",
    "Western Enterprises", "Central Trading", "United Commodities",
    "Allied Products", "National Resources", "Standard Industries",
    "Universal Components", "Precision Parts", "Quality Systems",
    "Advanced Technology", "Modern Solutions", "Prime Services",
    "Elite Manufacturing", "Superior Goods", "Excellence Corp",
]

INCOTERMS = ["EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"]
PAYMENT_TERMS = ["NT30", "NT60", "NT90", "2/10", "N/30"]
RECON_ACCOUNTS = [
    "0001410000", "0001420000", "0001430000",
    "0001440000", "0001450000", "0001460000",
]
MRP_TYPES = ["PD", "VB", "ND", "MK", "VV"]
LOT_SIZES = ["EX", "FX", "HB", "MB", "PK", "WB"]
VALUATION_CLASSES = ["3000", "3001", "3002", "7920", "7921"]
ACCOUNT_TYPES = ["A", "D", "K", "M", "S"]
CONTROLLING_AREA = "CO01"
CHART_OF_ACCOUNTS = "INT"
PRODUCT_GROUPS = ["MECH", "ELEC", "CHEM", "PACK", "SERV", "RAW", "CONS", "SEMI"]
DIVISIONS = ["01", "02", "03", "04", "05"]
PRODUCT_TYPES = ["FERT", "HALB", "ROH", "NLAG", "DIEN"]
PO_STATUSES = ["OPEN", "PARTIAL", "CLOSED", "CANCELLED"]
BP_TYPES = ["VEND", "CUST", "BOTH"]

# ---------------------------------------------------------------------------
# Table definitions
# ---------------------------------------------------------------------------

country_ref = Table("Country", metadata,
    Column("code", String(2)),
    Column("name", String(255)),
)

currency = Table("Currency", metadata,
    Column("code", String(3)),
    Column("name", String(255)),
)

uom = Table("UnitOfMeasure", metadata,
    Column("code", String(10)),
    Column("description", String(255)),
)

company_code = Table("CompanyCode", metadata,
    Column("code", String(4)),
    Column("name", String(255)),
    Column("country", String(2)),
    Column("currency", String(3)),
)

plant = Table("Plant", metadata,
    Column("code", String(4)),
    Column("name", String(255)),
    Column("company_code", String(4)),
    Column("country", String(2)),
)

purch_org = Table("PurchasingOrganization", metadata,
    Column("code", String(4)),
    Column("name", String(255)),
    Column("company_code", String(4)),
)

bp = Table("BusinessPartner", metadata,
    Column("BP_NUMBER", String(10)),
    Column("bp_type", String(4)),
    Column("NAME1", String(255)),
    Column("NAME2", String(255)),
    Column("COUNTRY", String(2)),
    Column("CURRENCY", String(3)),
    Column("TAX_NUMBER", String(20)),
    Column("LANGUAGE", String(2)),
    Column("created_at", String(20)),
)

bp_role = Table("BPRole", metadata,
    Column("BP_NUMBER", String(10)),
    Column("ROLE_CODE", String(6)),
    Column("VALID_FROM", String(10)),
    Column("VALID_TO", String(10)),
)

bp_bank = Table("BPBankAccount", metadata,
    Column("BP_NUMBER", String(10)),
    Column("BANK_COUNTRY", String(2)),
    Column("BANK_KEY", String(15)),
    Column("BANK_ACCOUNT", String(18)),
    Column("IBAN", String(34)),
    Column("SWIFT", String(11)),
)

bp_address = Table("BPAddress", metadata,
    Column("BP_NUMBER", String(10)),
    Column("STREET", String(255)),
    Column("CITY", String(255)),
    Column("POSTAL_CODE", String(10)),
    Column("COUNTRY", String(2)),
    Column("REGION", String(3)),
    Column("ADDR_TYPE", String(2)),
)

bp_company = Table("BPCompanyCode", metadata,
    Column("BP_NUMBER", String(10)),
    Column("COMPANY_CODE", String(4)),
    Column("RECONCILIATION_ACCOUNT", String(10)),
    Column("PAYMENT_TERMS", String(4)),
    Column("CURRENCY", String(3)),
)

bp_purch = Table("BPPurchasingOrg", metadata,
    Column("BP_NUMBER", String(10)),
    Column("PURCH_ORG", String(4)),
    Column("INCOTERMS", String(3)),
    Column("PAYMENT_TERMS", String(4)),
    Column("CURRENCY", String(3)),
)

product = Table("Product", metadata,
    Column("PRODUCT_NUMBER", String(10)),
    Column("PRODUCT_TYPE", String(4)),
    Column("BASE_UNIT", String(10)),
    Column("WEIGHT", String(10)),
    Column("WEIGHT_UNIT", String(10)),
    Column("VOLUME", String(10)),
    Column("VOLUME_UNIT", String(10)),
    Column("PRODUCT_GROUP", String(9)),
    Column("DIVISION", String(2)),
    Column("ERDAT", String(10)),
)

product_plant = Table("ProductPlant", metadata,
    Column("PRODUCT_NUMBER", String(10)),
    Column("PLANT", String(4)),
    Column("MRP_TYPE", String(2)),
    Column("SAFETY_STOCK", String(10)),
    Column("REORDER_POINT", String(10)),
    Column("LOT_SIZE", String(10)),
)

product_val = Table("ProductValuation", metadata,
    Column("PRODUCT_NUMBER", String(10)),
    Column("VALUATION_AREA", String(4)),
    Column("VALUATION_CLASS", String(4)),
    Column("STANDARD_PRICE", String(15)),
    Column("PRICE_UNIT", String(5)),
    Column("CURRENCY", String(3)),
)

gl_account = Table("GLAccount", metadata,
    Column("ACCOUNT_NUMBER", String(10)),
    Column("CHART_OF_ACCOUNTS", String(4)),
    Column("ACCOUNT_TYPE", String(1)),
    Column("DESCRIPTION", String(255)),
    Column("CREATED_AT", String(20)),
)

cost_center = Table("CostCenter", metadata,
    Column("COST_CENTER", String(10)),
    Column("CONTROLLING_AREA", String(4)),
    Column("COMPANY_CODE", String(4)),
    Column("DESCRIPTION", String(255)),
    Column("VALID_FROM", String(10)),
    Column("VALID_TO", String(10)),
)

profit_center = Table("ProfitCenter", metadata,
    Column("PROFIT_CENTER", String(10)),
    Column("CONTROLLING_AREA", String(4)),
    Column("DESCRIPTION", String(255)),
    Column("SEGMENT", String(10)),
)

po = Table("PurchaseOrder", metadata,
    Column("PO_NUMBER", String(10)),
    Column("VENDOR", String(10)),
    Column("COMPANY_CODE", String(4)),
    Column("PURCH_ORG", String(4)),
    Column("CURRENCY", String(3)),
    Column("DOCUMENT_DATE", String(10)),
    Column("STATUS", String(10)),
)

po_item = Table("PurchaseOrderItem", metadata,
    Column("PO_NUMBER", String(10)),
    Column("ITEM_NUMBER", String(6)),
    Column("PRODUCT", String(10)),
    Column("PLANT", String(4)),
    Column("QUANTITY", String(10)),
    Column("UNIT", String(10)),
    Column("NET_PRICE", String(15)),
    Column("CURRENCY", String(3)),
    Column("DELIVERY_DATE", String(10)),
)

load_history = Table("load_history", metadata,
    Column("batch_id", String(36)),
    Column("table_name", String(100)),
    Column("mode", String(20)),
    Column("status", String(20)),
    Column("inserted", Integer()),
    Column("updated", Integer()),
    Column("rejected", Integer()),
    Column("error_details", String(5000)),
    Column("created_at", String(30)),
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BATCH_SIZE = 500

def _fmt_date(d: date) -> str:
    return d.isoformat()

def _random_date(fake: Faker, start_year: int = 2015, end_year: int = 2024) -> str:
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = (end - start).days
    return _fmt_date(start + timedelta(days=random.randint(0, delta)))

async def _bulk_insert(conn, table, rows: list) -> None:
    if not rows:
        return
    for i in range(0, len(rows), BATCH_SIZE):
        await conn.execute(table.insert(), rows[i : i + BATCH_SIZE])

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def create_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


async def drop_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


async def seed_data(engine: AsyncEngine) -> None:
    fake = Faker(["en_US", "en_GB", "de_DE", "fr_FR", "ja_JP", "pt_BR"])
    Faker.seed(42)
    random.seed(42)

    async with engine.begin() as conn:

        # ── Reference tables ────────────────────────────────────────────────
        await _bulk_insert(conn, country_ref,
            [{"code": c, "name": n} for c, n in COUNTRIES])

        await _bulk_insert(conn, currency,
            [{"code": c, "name": n} for c, n in CURRENCIES])

        await _bulk_insert(conn, uom,
            [{"code": c, "description": d} for c, d in UOMS])

        await _bulk_insert(conn, company_code,
            [{"code": c, "name": n, "country": co, "currency": cu}
             for c, n, co, cu in COMPANY_CODES])

        await _bulk_insert(conn, plant,
            [{"code": c, "name": n, "company_code": cc, "country": co}
             for c, n, cc, co in PLANTS])

        await _bulk_insert(conn, purch_org,
            [{"code": c, "name": n, "company_code": cc}
             for c, n, cc in PURCH_ORGS])

        # ── BusinessPartner (300 rows) ──────────────────────────────────────
        bp_rows = []
        bp_numbers = []
        bp_type_map = {}  # bp_number -> bp_type
        for n in range(300):
            bp_num = f"{n + 1:010d}"
            bp_numbers.append(bp_num)
            bp_t = random.choice(BP_TYPES)
            bp_type_map[bp_num] = bp_t

            # First 30 rows use legacy-overlap names
            if n < 30:
                name1 = LEGACY_OVERLAP_NAMES[n]
                name2 = ""
            else:
                name1 = fake.company()
                name2 = fake.company_suffix() if random.random() < 0.3 else ""

            country = random.choice(COUNTRY_CODES)
            cur = random.choice(CURRENCY_CODES)
            lang = random.choice(["EN", "DE", "FR", "JA", "PT", "ZH"])
            tax = fake.numerify("##-#######")
            created = _random_date(fake)

            bp_rows.append({
                "BP_NUMBER": bp_num,
                "bp_type": bp_t,
                "NAME1": name1,
                "NAME2": name2,
                "COUNTRY": country,
                "CURRENCY": cur,
                "TAX_NUMBER": tax,
                "LANGUAGE": lang,
                "created_at": created,
            })
        await _bulk_insert(conn, bp, bp_rows)

        # ── BPRole (~400 rows, 1-2 per BP) ─────────────────────────────────
        role_rows = []
        for bp_num in bp_numbers:
            n_roles = random.randint(1, 2)
            bt = bp_type_map[bp_num]
            if bt == "VEND":
                role_pool = ["FLVN01"]
            elif bt == "CUST":
                role_pool = ["FLCU01"]
            else:
                role_pool = ["FLVN01", "FLCU01"]

            chosen_roles = random.sample(role_pool, min(n_roles, len(role_pool)))
            vf = _random_date(fake, 2010, 2020)
            vt = _random_date(fake, 2025, 2030)
            for rc in chosen_roles:
                role_rows.append({
                    "BP_NUMBER": bp_num,
                    "ROLE_CODE": rc,
                    "VALID_FROM": vf,
                    "VALID_TO": vt,
                })
        await _bulk_insert(conn, bp_role, role_rows)

        # ── BPBankAccount (~200 rows, ~2/3 of BPs get a bank account) ──────
        bank_rows = []
        for bp_num in random.sample(bp_numbers, 200):
            bk_country = random.choice(COUNTRY_CODES)
            bk_key = fake.numerify("########")
            bk_acct = fake.numerify("##################")
            # Simple IBAN-style string (not cryptographically valid)
            iban = f"{bk_country}{fake.numerify('##')}{fake.numerify('##################')}"
            swift = fake.lexify("????????", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:8] + "XXX"
            bank_rows.append({
                "BP_NUMBER": bp_num,
                "BANK_COUNTRY": bk_country,
                "BANK_KEY": bk_key[:15],
                "BANK_ACCOUNT": bk_acct[:18],
                "IBAN": iban[:34],
                "SWIFT": swift[:11],
            })
        await _bulk_insert(conn, bp_bank, bank_rows)

        # ── BPAddress (300 rows, one per BP) ───────────────────────────────
        addr_rows = []
        for bp_num in bp_numbers:
            addr_rows.append({
                "BP_NUMBER": bp_num,
                "STREET": fake.street_address()[:255],
                "CITY": fake.city()[:255],
                "POSTAL_CODE": fake.postcode()[:10],
                "COUNTRY": random.choice(COUNTRY_CODES),
                "REGION": fake.lexify("???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:3],
                "ADDR_TYPE": "01",
            })
        await _bulk_insert(conn, bp_address, addr_rows)

        # ── BPCompanyCode (~250 rows) ───────────────────────────────────────
        bpc_rows = []
        for bp_num in random.sample(bp_numbers, 250):
            cc = random.choice(COMPANY_CODE_KEYS)
            bpc_rows.append({
                "BP_NUMBER": bp_num,
                "COMPANY_CODE": cc,
                "RECONCILIATION_ACCOUNT": random.choice(RECON_ACCOUNTS),
                "PAYMENT_TERMS": random.choice(PAYMENT_TERMS)[:4],
                "CURRENCY": random.choice(CURRENCY_CODES),
            })
        await _bulk_insert(conn, bp_company, bpc_rows)

        # ── BPPurchasingOrg (~200 rows, vendor BPs only) ───────────────────
        vendor_bps = [n for n in bp_numbers if bp_type_map[n] in ("VEND", "BOTH")]
        sample_vendors = random.sample(vendor_bps, min(200, len(vendor_bps)))
        bpp_rows = []
        for bp_num in sample_vendors:
            bpp_rows.append({
                "BP_NUMBER": bp_num,
                "PURCH_ORG": random.choice(PURCH_ORG_CODES),
                "INCOTERMS": random.choice(INCOTERMS)[:3],
                "PAYMENT_TERMS": random.choice(PAYMENT_TERMS)[:4],
                "CURRENCY": random.choice(CURRENCY_CODES),
            })
        await _bulk_insert(conn, bp_purch, bpp_rows)

        # ── Product (200 rows) ─────────────────────────────────────────────
        product_rows = []
        product_numbers = []
        for n in range(200):
            pnum = f"P{n + 1:09d}"
            product_numbers.append(pnum)
            w = f"{random.uniform(0.1, 100):.3f}"
            v = f"{random.uniform(0.01, 10):.4f}"
            product_rows.append({
                "PRODUCT_NUMBER": pnum,
                "PRODUCT_TYPE": random.choice(PRODUCT_TYPES),
                "BASE_UNIT": random.choice(UOM_CODES),
                "WEIGHT": w,
                "WEIGHT_UNIT": random.choice(["KG", "LB", "G"]),
                "VOLUME": v,
                "VOLUME_UNIT": random.choice(["L", "M3", "ML"]),
                "PRODUCT_GROUP": random.choice(PRODUCT_GROUPS),
                "DIVISION": random.choice(DIVISIONS),
                "ERDAT": _random_date(fake, 2010, 2023),
            })
        await _bulk_insert(conn, product, product_rows)

        # ── ProductPlant (~300 rows, 1-2 plants per product) ───────────────
        pp_rows = []
        for pnum in product_numbers:
            n_plants = random.randint(1, 2)
            chosen_plants = random.sample(PLANT_CODES, n_plants)
            for plt in chosen_plants:
                pp_rows.append({
                    "PRODUCT_NUMBER": pnum,
                    "PLANT": plt,
                    "MRP_TYPE": random.choice(MRP_TYPES),
                    "SAFETY_STOCK": str(random.randint(0, 500)),
                    "REORDER_POINT": str(random.randint(0, 200)),
                    "LOT_SIZE": random.choice(LOT_SIZES),
                })
        await _bulk_insert(conn, product_plant, pp_rows)

        # ── ProductValuation (~200 rows, one per product) ──────────────────
        pv_rows = []
        for pnum in product_numbers:
            val_area = random.choice(PLANT_CODES)
            price = f"{random.uniform(1, 9999):.2f}"
            pv_rows.append({
                "PRODUCT_NUMBER": pnum,
                "VALUATION_AREA": val_area,
                "VALUATION_CLASS": random.choice(VALUATION_CLASSES),
                "STANDARD_PRICE": price,
                "PRICE_UNIT": "1",
                "CURRENCY": random.choice(CURRENCY_CODES),
            })
        await _bulk_insert(conn, product_val, pv_rows)

        # ── GLAccount (~80 rows) ────────────────────────────────────────────
        gl_rows = []
        gl_account_numbers = []
        for n in range(80):
            acct_num = f"{(n + 1) * 10000:010d}"
            gl_account_numbers.append(acct_num)
            acct_type = random.choice(ACCOUNT_TYPES)
            descs = {
                "A": "Asset Account",
                "D": "Accounts Receivable",
                "K": "Accounts Payable",
                "M": "Material Account",
                "S": "G/L Account",
            }
            desc = f"{descs[acct_type]} {n + 1:04d}"
            gl_rows.append({
                "ACCOUNT_NUMBER": acct_num,
                "CHART_OF_ACCOUNTS": CHART_OF_ACCOUNTS,
                "ACCOUNT_TYPE": acct_type,
                "DESCRIPTION": desc,
                "CREATED_AT": _random_date(fake, 2000, 2020),
            })
        await _bulk_insert(conn, gl_account, gl_rows)

        # ── CostCenter (~60 rows) ───────────────────────────────────────────
        cc_rows = []
        cc_domains = ["Administration", "Finance", "IT", "HR", "Operations",
                      "Sales", "Marketing", "R&D", "Logistics", "Procurement"]
        for n in range(60):
            cc_num = f"CC{n + 1:08d}"
            domain = cc_domains[n % len(cc_domains)]
            cc_rows.append({
                "COST_CENTER": cc_num,
                "CONTROLLING_AREA": CONTROLLING_AREA,
                "COMPANY_CODE": random.choice(COMPANY_CODE_KEYS),
                "DESCRIPTION": f"{domain} Cost Center {n + 1:03d}",
                "VALID_FROM": _random_date(fake, 2000, 2015),
                "VALID_TO": _random_date(fake, 2030, 2040),
            })
        await _bulk_insert(conn, cost_center, cc_rows)

        # ── ProfitCenter (~40 rows) ─────────────────────────────────────────
        pc_rows = []
        segments = ["MFCT", "SERV", "DIST", "RETL", "CORP"]
        for n in range(40):
            pc_num = f"PC{n + 1:08d}"
            seg = random.choice(segments)
            pc_rows.append({
                "PROFIT_CENTER": pc_num,
                "CONTROLLING_AREA": CONTROLLING_AREA,
                "DESCRIPTION": f"Profit Center {n + 1:03d} ({seg})",
                "SEGMENT": seg,
            })
        await _bulk_insert(conn, profit_center, pc_rows)

        # ── PurchaseOrder (~150 rows) ────────────────────────────────────────
        # Only use vendor BPs for POs
        available_vendors = vendor_bps[:150] if len(vendor_bps) >= 150 else vendor_bps
        po_rows = []
        po_numbers = []
        for n in range(150):
            po_num = f"PO{n + 1:08d}"
            po_numbers.append(po_num)
            vendor = available_vendors[n % len(available_vendors)]
            cc = random.choice(COMPANY_CODE_KEYS)
            # Match purch org to company code where possible
            matching_pos = [p[0] for p in PURCH_ORGS if p[2] == cc]
            chosen_po = random.choice(matching_pos) if matching_pos else random.choice(PURCH_ORG_CODES)
            po_rows.append({
                "PO_NUMBER": po_num,
                "VENDOR": vendor,
                "COMPANY_CODE": cc,
                "PURCH_ORG": chosen_po,
                "CURRENCY": random.choice(CURRENCY_CODES),
                "DOCUMENT_DATE": _random_date(fake, 2022, 2024),
                "STATUS": random.choice(PO_STATUSES),
            })
        await _bulk_insert(conn, po, po_rows)

        # ── PurchaseOrderItem (~400 rows, 2-3 items per PO) ─────────────────
        poi_rows = []
        for po_num in po_numbers:
            n_items = random.randint(2, 3)
            for item_idx in range(n_items):
                item_num = f"{(item_idx + 1) * 10:06d}"
                prod = random.choice(product_numbers)
                plt = random.choice(PLANT_CODES)
                qty = f"{random.randint(1, 1000)}"
                price = f"{random.uniform(1, 9999):.2f}"
                poi_rows.append({
                    "PO_NUMBER": po_num,
                    "ITEM_NUMBER": item_num,
                    "PRODUCT": prod,
                    "PLANT": plt,
                    "QUANTITY": qty,
                    "UNIT": random.choice(UOM_CODES),
                    "NET_PRICE": price,
                    "CURRENCY": random.choice(CURRENCY_CODES),
                    "DELIVERY_DATE": _random_date(fake, 2024, 2026),
                })
        await _bulk_insert(conn, po_item, poi_rows)


# ---------------------------------------------------------------------------
# Metadata helpers
# ---------------------------------------------------------------------------

# Table metadata excluding load_history (internal table)
_TABLE_META = [
    {
        "name": "BusinessPartner",
        "domain": "Business Partner",
        "record_count": 300,
        "primary_keys": ["BP_NUMBER"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "BPRole",
        "domain": "Business Partner",
        "record_count": 400,
        "primary_keys": ["BP_NUMBER", "ROLE_CODE"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "BPBankAccount",
        "domain": "Business Partner",
        "record_count": 200,
        "primary_keys": ["BP_NUMBER", "BANK_COUNTRY", "BANK_KEY", "BANK_ACCOUNT"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "BPAddress",
        "domain": "Business Partner",
        "record_count": 300,
        "primary_keys": ["BP_NUMBER"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "BPCompanyCode",
        "domain": "Business Partner",
        "record_count": 250,
        "primary_keys": ["BP_NUMBER", "COMPANY_CODE"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "BPPurchasingOrg",
        "domain": "Business Partner",
        "record_count": 200,
        "primary_keys": ["BP_NUMBER", "PURCH_ORG"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "Product",
        "domain": "Product",
        "record_count": 200,
        "primary_keys": ["PRODUCT_NUMBER"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "ProductPlant",
        "domain": "Product",
        "record_count": 300,
        "primary_keys": ["PRODUCT_NUMBER", "PLANT"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "ProductValuation",
        "domain": "Product",
        "record_count": 200,
        "primary_keys": ["PRODUCT_NUMBER", "VALUATION_AREA"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "GLAccount",
        "domain": "Finance",
        "record_count": 80,
        "primary_keys": ["ACCOUNT_NUMBER", "CHART_OF_ACCOUNTS"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "CostCenter",
        "domain": "Finance",
        "record_count": 60,
        "primary_keys": ["COST_CENTER", "CONTROLLING_AREA"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "ProfitCenter",
        "domain": "Finance",
        "record_count": 40,
        "primary_keys": ["PROFIT_CENTER", "CONTROLLING_AREA"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "PurchaseOrder",
        "domain": "Purchasing",
        "record_count": 150,
        "primary_keys": ["PO_NUMBER"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "PurchaseOrderItem",
        "domain": "Purchasing",
        "record_count": 400,
        "primary_keys": ["PO_NUMBER", "ITEM_NUMBER"],
        "load_supported": True,
        "validate_supported": True,
    },
    {
        "name": "Country",
        "domain": "Reference",
        "record_count": 50,
        "primary_keys": ["code"],
        "load_supported": False,
        "validate_supported": False,
    },
    {
        "name": "Currency",
        "domain": "Reference",
        "record_count": 30,
        "primary_keys": ["code"],
        "load_supported": False,
        "validate_supported": False,
    },
    {
        "name": "UnitOfMeasure",
        "domain": "Reference",
        "record_count": 20,
        "primary_keys": ["code"],
        "load_supported": False,
        "validate_supported": False,
    },
    {
        "name": "CompanyCode",
        "domain": "Reference",
        "record_count": 5,
        "primary_keys": ["code"],
        "load_supported": False,
        "validate_supported": False,
    },
    {
        "name": "Plant",
        "domain": "Reference",
        "record_count": 10,
        "primary_keys": ["code"],
        "load_supported": False,
        "validate_supported": False,
    },
    {
        "name": "PurchasingOrganization",
        "domain": "Reference",
        "record_count": 5,
        "primary_keys": ["code"],
        "load_supported": False,
        "validate_supported": False,
    },
]

# Column schema definitions keyed by table name
_SCHEMA_MAP: dict[str, list[dict]] = {
    "BusinessPartner": [
        {"name": "BP_NUMBER", "type": "string(10)", "nullable": False,
         "description": "10-digit zero-padded business partner number",
         "validation_rules": ["required", "pattern:^[0-9]{10}$"]},
        {"name": "bp_type", "type": "string(4)", "nullable": False,
         "description": "Business partner type: VEND, CUST, or BOTH",
         "validation_rules": ["required", "allowed_values:VEND,CUST,BOTH"]},
        {"name": "NAME1", "type": "string(255)", "nullable": False,
         "description": "Primary name",
         "validation_rules": ["required", "string_hygiene"]},
        {"name": "NAME2", "type": "string(255)", "nullable": True,
         "description": "Secondary name",
         "validation_rules": ["string_hygiene"]},
        {"name": "COUNTRY", "type": "string(2)", "nullable": False,
         "description": "ISO 3166-1 alpha-2 country code",
         "validation_rules": ["required", "iso_code:country"]},
        {"name": "CURRENCY", "type": "string(3)", "nullable": False,
         "description": "ISO 4217 currency code",
         "validation_rules": ["required", "iso_code:currency"]},
        {"name": "TAX_NUMBER", "type": "string(20)", "nullable": True,
         "description": "Tax identification number",
         "validation_rules": []},
        {"name": "LANGUAGE", "type": "string(2)", "nullable": True,
         "description": "Language key",
         "validation_rules": []},
        {"name": "created_at", "type": "string(20)", "nullable": True,
         "description": "Creation date",
         "validation_rules": ["date_reasonableness"]},
    ],
    "BPRole": [
        {"name": "BP_NUMBER", "type": "string(10)", "nullable": False,
         "description": "Business partner number (FK)",
         "validation_rules": ["required", "fk:BusinessPartner.BP_NUMBER"]},
        {"name": "ROLE_CODE", "type": "string(6)", "nullable": False,
         "description": "Role code (FLVN01=Vendor, FLCU01=Customer)",
         "validation_rules": ["required", "allowed_values:FLVN01,FLCU01"]},
        {"name": "VALID_FROM", "type": "string(10)", "nullable": True,
         "description": "Validity start date",
         "validation_rules": []},
        {"name": "VALID_TO", "type": "string(10)", "nullable": True,
         "description": "Validity end date",
         "validation_rules": []},
    ],
    "BPBankAccount": [
        {"name": "BP_NUMBER", "type": "string(10)", "nullable": False,
         "description": "Business partner number (FK)",
         "validation_rules": ["required", "fk:BusinessPartner.BP_NUMBER"]},
        {"name": "BANK_COUNTRY", "type": "string(2)", "nullable": False,
         "description": "Bank country ISO code",
         "validation_rules": ["required", "iso_code:country"]},
        {"name": "BANK_KEY", "type": "string(15)", "nullable": False,
         "description": "Bank routing number",
         "validation_rules": ["required"]},
        {"name": "BANK_ACCOUNT", "type": "string(18)", "nullable": False,
         "description": "Bank account number",
         "validation_rules": ["required"]},
        {"name": "IBAN", "type": "string(34)", "nullable": True,
         "description": "International Bank Account Number",
         "validation_rules": []},
        {"name": "SWIFT", "type": "string(11)", "nullable": True,
         "description": "SWIFT/BIC code",
         "validation_rules": []},
    ],
    "BPAddress": [
        {"name": "BP_NUMBER", "type": "string(10)", "nullable": False,
         "description": "Business partner number (FK)",
         "validation_rules": ["required", "fk:BusinessPartner.BP_NUMBER"]},
        {"name": "STREET", "type": "string(255)", "nullable": True,
         "description": "Street address",
         "validation_rules": ["string_hygiene"]},
        {"name": "CITY", "type": "string(255)", "nullable": True,
         "description": "City",
         "validation_rules": ["string_hygiene"]},
        {"name": "POSTAL_CODE", "type": "string(10)", "nullable": True,
         "description": "Postal/ZIP code",
         "validation_rules": []},
        {"name": "COUNTRY", "type": "string(2)", "nullable": False,
         "description": "ISO country code",
         "validation_rules": ["required", "iso_code:country"]},
        {"name": "REGION", "type": "string(3)", "nullable": True,
         "description": "Region/state code",
         "validation_rules": []},
        {"name": "ADDR_TYPE", "type": "string(2)", "nullable": True,
         "description": "Address type",
         "validation_rules": []},
    ],
    "BPCompanyCode": [
        {"name": "BP_NUMBER", "type": "string(10)", "nullable": False,
         "description": "Business partner number (FK)",
         "validation_rules": ["required", "fk:BusinessPartner.BP_NUMBER"]},
        {"name": "COMPANY_CODE", "type": "string(4)", "nullable": False,
         "description": "Company code (FK)",
         "validation_rules": ["required", "fk:CompanyCode.code"]},
        {"name": "RECONCILIATION_ACCOUNT", "type": "string(10)", "nullable": True,
         "description": "Reconciliation G/L account",
         "validation_rules": []},
        {"name": "PAYMENT_TERMS", "type": "string(4)", "nullable": True,
         "description": "Payment terms key",
         "validation_rules": []},
        {"name": "CURRENCY", "type": "string(3)", "nullable": True,
         "description": "Currency code",
         "validation_rules": ["iso_code:currency"]},
    ],
    "BPPurchasingOrg": [
        {"name": "BP_NUMBER", "type": "string(10)", "nullable": False,
         "description": "Business partner number (FK)",
         "validation_rules": ["required", "fk:BusinessPartner.BP_NUMBER"]},
        {"name": "PURCH_ORG", "type": "string(4)", "nullable": False,
         "description": "Purchasing organization (FK)",
         "validation_rules": ["required", "fk:PurchasingOrganization.code"]},
        {"name": "INCOTERMS", "type": "string(3)", "nullable": True,
         "description": "Incoterms code",
         "validation_rules": []},
        {"name": "PAYMENT_TERMS", "type": "string(4)", "nullable": True,
         "description": "Payment terms key",
         "validation_rules": []},
        {"name": "CURRENCY", "type": "string(3)", "nullable": True,
         "description": "Currency code",
         "validation_rules": ["iso_code:currency"]},
    ],
    "Product": [
        {"name": "PRODUCT_NUMBER", "type": "string(10)", "nullable": False,
         "description": "Product number PK",
         "validation_rules": ["required"]},
        {"name": "PRODUCT_TYPE", "type": "string(4)", "nullable": True,
         "description": "Product type (FERT/HALB/ROH/NLAG/DIEN)",
         "validation_rules": []},
        {"name": "BASE_UNIT", "type": "string(10)", "nullable": False,
         "description": "Base unit of measure (FK)",
         "validation_rules": ["required", "fk:UnitOfMeasure.code"]},
        {"name": "WEIGHT", "type": "string(10)", "nullable": True,
         "description": "Gross weight",
         "validation_rules": []},
        {"name": "WEIGHT_UNIT", "type": "string(10)", "nullable": True,
         "description": "Weight unit",
         "validation_rules": []},
        {"name": "VOLUME", "type": "string(10)", "nullable": True,
         "description": "Volume",
         "validation_rules": []},
        {"name": "VOLUME_UNIT", "type": "string(10)", "nullable": True,
         "description": "Volume unit",
         "validation_rules": []},
        {"name": "PRODUCT_GROUP", "type": "string(9)", "nullable": True,
         "description": "Material group",
         "validation_rules": []},
        {"name": "DIVISION", "type": "string(2)", "nullable": True,
         "description": "Division",
         "validation_rules": []},
        {"name": "ERDAT", "type": "string(10)", "nullable": True,
         "description": "Creation date",
         "validation_rules": []},
    ],
    "ProductPlant": [
        {"name": "PRODUCT_NUMBER", "type": "string(10)", "nullable": False,
         "description": "Product number (FK)",
         "validation_rules": ["required", "fk:Product.PRODUCT_NUMBER"]},
        {"name": "PLANT", "type": "string(4)", "nullable": False,
         "description": "Plant code (FK)",
         "validation_rules": ["required", "fk:Plant.code"]},
        {"name": "MRP_TYPE", "type": "string(2)", "nullable": True,
         "description": "MRP type",
         "validation_rules": []},
        {"name": "SAFETY_STOCK", "type": "string(10)", "nullable": True,
         "description": "Safety stock quantity",
         "validation_rules": []},
        {"name": "REORDER_POINT", "type": "string(10)", "nullable": True,
         "description": "Reorder point",
         "validation_rules": []},
        {"name": "LOT_SIZE", "type": "string(10)", "nullable": True,
         "description": "Lot sizing key",
         "validation_rules": []},
    ],
    "ProductValuation": [
        {"name": "PRODUCT_NUMBER", "type": "string(10)", "nullable": False,
         "description": "Product number (FK)",
         "validation_rules": ["required", "fk:Product.PRODUCT_NUMBER"]},
        {"name": "VALUATION_AREA", "type": "string(4)", "nullable": False,
         "description": "Valuation area (plant-level)",
         "validation_rules": ["required"]},
        {"name": "VALUATION_CLASS", "type": "string(4)", "nullable": True,
         "description": "Valuation class",
         "validation_rules": []},
        {"name": "STANDARD_PRICE", "type": "string(15)", "nullable": True,
         "description": "Standard price",
         "validation_rules": []},
        {"name": "PRICE_UNIT", "type": "string(5)", "nullable": True,
         "description": "Price unit",
         "validation_rules": []},
        {"name": "CURRENCY", "type": "string(3)", "nullable": True,
         "description": "Currency code",
         "validation_rules": ["iso_code:currency"]},
    ],
    "GLAccount": [
        {"name": "ACCOUNT_NUMBER", "type": "string(10)", "nullable": False,
         "description": "G/L account number",
         "validation_rules": ["required"]},
        {"name": "CHART_OF_ACCOUNTS", "type": "string(4)", "nullable": False,
         "description": "Chart of accounts key",
         "validation_rules": ["required"]},
        {"name": "ACCOUNT_TYPE", "type": "string(1)", "nullable": True,
         "description": "Account type (A/D/K/M/S)",
         "validation_rules": []},
        {"name": "DESCRIPTION", "type": "string(255)", "nullable": True,
         "description": "Account description",
         "validation_rules": ["string_hygiene"]},
        {"name": "CREATED_AT", "type": "string(20)", "nullable": True,
         "description": "Creation date",
         "validation_rules": []},
    ],
    "CostCenter": [
        {"name": "COST_CENTER", "type": "string(10)", "nullable": False,
         "description": "Cost center number",
         "validation_rules": ["required"]},
        {"name": "CONTROLLING_AREA", "type": "string(4)", "nullable": False,
         "description": "Controlling area",
         "validation_rules": ["required"]},
        {"name": "COMPANY_CODE", "type": "string(4)", "nullable": True,
         "description": "Company code",
         "validation_rules": []},
        {"name": "DESCRIPTION", "type": "string(255)", "nullable": True,
         "description": "Cost center description",
         "validation_rules": []},
        {"name": "VALID_FROM", "type": "string(10)", "nullable": True,
         "description": "Validity start",
         "validation_rules": []},
        {"name": "VALID_TO", "type": "string(10)", "nullable": True,
         "description": "Validity end",
         "validation_rules": []},
    ],
    "ProfitCenter": [
        {"name": "PROFIT_CENTER", "type": "string(10)", "nullable": False,
         "description": "Profit center number",
         "validation_rules": ["required"]},
        {"name": "CONTROLLING_AREA", "type": "string(4)", "nullable": False,
         "description": "Controlling area",
         "validation_rules": ["required"]},
        {"name": "DESCRIPTION", "type": "string(255)", "nullable": True,
         "description": "Profit center description",
         "validation_rules": []},
        {"name": "SEGMENT", "type": "string(10)", "nullable": True,
         "description": "Segment",
         "validation_rules": []},
    ],
    "PurchaseOrder": [
        {"name": "PO_NUMBER", "type": "string(10)", "nullable": False,
         "description": "Purchase order number PK",
         "validation_rules": ["required"]},
        {"name": "VENDOR", "type": "string(10)", "nullable": False,
         "description": "Vendor BP number (FK)",
         "validation_rules": ["required", "fk:BusinessPartner.BP_NUMBER"]},
        {"name": "COMPANY_CODE", "type": "string(4)", "nullable": False,
         "description": "Company code",
         "validation_rules": ["required"]},
        {"name": "PURCH_ORG", "type": "string(4)", "nullable": False,
         "description": "Purchasing organization",
         "validation_rules": ["required"]},
        {"name": "CURRENCY", "type": "string(3)", "nullable": False,
         "description": "Document currency",
         "validation_rules": ["required", "iso_code:currency"]},
        {"name": "DOCUMENT_DATE", "type": "string(10)", "nullable": True,
         "description": "Document date",
         "validation_rules": []},
        {"name": "STATUS", "type": "string(10)", "nullable": True,
         "description": "Order status",
         "validation_rules": []},
    ],
    "PurchaseOrderItem": [
        {"name": "PO_NUMBER", "type": "string(10)", "nullable": False,
         "description": "Purchase order number (FK)",
         "validation_rules": ["required", "fk:PurchaseOrder.PO_NUMBER"]},
        {"name": "ITEM_NUMBER", "type": "string(6)", "nullable": False,
         "description": "Line item number",
         "validation_rules": ["required"]},
        {"name": "PRODUCT", "type": "string(10)", "nullable": True,
         "description": "Product number",
         "validation_rules": []},
        {"name": "PLANT", "type": "string(4)", "nullable": True,
         "description": "Plant",
         "validation_rules": []},
        {"name": "QUANTITY", "type": "string(10)", "nullable": True,
         "description": "Order quantity",
         "validation_rules": []},
        {"name": "UNIT", "type": "string(10)", "nullable": True,
         "description": "Unit of measure",
         "validation_rules": []},
        {"name": "NET_PRICE", "type": "string(15)", "nullable": True,
         "description": "Net price",
         "validation_rules": []},
        {"name": "CURRENCY", "type": "string(3)", "nullable": True,
         "description": "Currency",
         "validation_rules": ["iso_code:currency"]},
        {"name": "DELIVERY_DATE", "type": "string(10)", "nullable": True,
         "description": "Requested delivery date",
         "validation_rules": []},
    ],
    "Country": [
        {"name": "code", "type": "string(2)", "nullable": False,
         "description": "ISO 3166-1 alpha-2 code", "validation_rules": ["required"]},
        {"name": "name", "type": "string(255)", "nullable": False,
         "description": "Country name", "validation_rules": []},
    ],
    "Currency": [
        {"name": "code", "type": "string(3)", "nullable": False,
         "description": "ISO 4217 currency code", "validation_rules": ["required"]},
        {"name": "name", "type": "string(255)", "nullable": False,
         "description": "Currency name", "validation_rules": []},
    ],
    "UnitOfMeasure": [
        {"name": "code", "type": "string(10)", "nullable": False,
         "description": "Unit of measure code", "validation_rules": ["required"]},
        {"name": "description", "type": "string(255)", "nullable": False,
         "description": "Unit description", "validation_rules": []},
    ],
    "CompanyCode": [
        {"name": "code", "type": "string(4)", "nullable": False,
         "description": "Company code PK", "validation_rules": ["required"]},
        {"name": "name", "type": "string(255)", "nullable": False,
         "description": "Company name", "validation_rules": []},
        {"name": "country", "type": "string(2)", "nullable": False,
         "description": "Country code", "validation_rules": ["iso_code:country"]},
        {"name": "currency", "type": "string(3)", "nullable": False,
         "description": "Local currency", "validation_rules": ["iso_code:currency"]},
    ],
    "Plant": [
        {"name": "code", "type": "string(4)", "nullable": False,
         "description": "Plant code PK", "validation_rules": ["required"]},
        {"name": "name", "type": "string(255)", "nullable": False,
         "description": "Plant name", "validation_rules": []},
        {"name": "company_code", "type": "string(4)", "nullable": False,
         "description": "Assigned company code", "validation_rules": []},
        {"name": "country", "type": "string(2)", "nullable": False,
         "description": "Country", "validation_rules": ["iso_code:country"]},
    ],
    "PurchasingOrganization": [
        {"name": "code", "type": "string(4)", "nullable": False,
         "description": "Purchasing org code PK", "validation_rules": ["required"]},
        {"name": "name", "type": "string(255)", "nullable": False,
         "description": "Organization name", "validation_rules": []},
        {"name": "company_code", "type": "string(4)", "nullable": False,
         "description": "Assigned company code", "validation_rules": []},
    ],
}

# FK relationships
_RELATIONSHIP_MAP: dict[str, list[dict]] = {
    "BPRole": [
        {"from_column": "BP_NUMBER", "to_table": "BusinessPartner", "to_column": "BP_NUMBER"},
    ],
    "BPBankAccount": [
        {"from_column": "BP_NUMBER", "to_table": "BusinessPartner", "to_column": "BP_NUMBER"},
    ],
    "BPAddress": [
        {"from_column": "BP_NUMBER", "to_table": "BusinessPartner", "to_column": "BP_NUMBER"},
    ],
    "BPCompanyCode": [
        {"from_column": "BP_NUMBER", "to_table": "BusinessPartner", "to_column": "BP_NUMBER"},
        {"from_column": "COMPANY_CODE", "to_table": "CompanyCode", "to_column": "code"},
    ],
    "BPPurchasingOrg": [
        {"from_column": "BP_NUMBER", "to_table": "BusinessPartner", "to_column": "BP_NUMBER"},
        {"from_column": "PURCH_ORG", "to_table": "PurchasingOrganization", "to_column": "code"},
    ],
    "ProductPlant": [
        {"from_column": "PRODUCT_NUMBER", "to_table": "Product", "to_column": "PRODUCT_NUMBER"},
        {"from_column": "PLANT", "to_table": "Plant", "to_column": "code"},
    ],
    "ProductValuation": [
        {"from_column": "PRODUCT_NUMBER", "to_table": "Product", "to_column": "PRODUCT_NUMBER"},
    ],
    "PurchaseOrder": [
        {"from_column": "VENDOR", "to_table": "BusinessPartner", "to_column": "BP_NUMBER"},
    ],
    "PurchaseOrderItem": [
        {"from_column": "PO_NUMBER", "to_table": "PurchaseOrder", "to_column": "PO_NUMBER"},
    ],
}


def get_tables() -> list[dict]:
    """Return metadata for all tables (excluding load_history)."""
    return _TABLE_META


def get_schema(table_name: str) -> list[dict]:
    """Return column definitions for the named table."""
    return _SCHEMA_MAP.get(table_name, [])


def get_relationships(table_name: str) -> list[dict]:
    """Return FK relationships for the named table."""
    return _RELATIONSHIP_MAP.get(table_name, [])
