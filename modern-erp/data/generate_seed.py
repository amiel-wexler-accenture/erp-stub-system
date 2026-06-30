#!/usr/bin/env python3
"""
Transform legacy ECC seed CSVs → S/4HANA format CSVs for the modern ERP.

Run from modern-erp/data/:
    python3 generate_seed.py
Requires: pip install pandas
"""

import csv
import sys
from pathlib import Path

import pandas as pd

LEGACY_SEED = Path(__file__).parent.parent.parent / "legacy-erp" / "data" / "seed"
OUTPUT_DIR = Path(__file__).parent / "seed"

# Valid reference codes (must match s4hana.py constants)
VALID_COUNTRIES = {
    "US", "GB", "DE", "FR", "JP", "BR", "CN", "IN", "CA", "AU", "MX",
    "IT", "ES", "NL", "SE", "NO", "DK", "FI", "CH", "AT", "BE", "PL",
    "CZ", "PT", "RU", "ZA", "KR", "SG", "HK", "TW", "AR", "CL", "CO",
    "PE", "VE", "EG", "NG", "KE", "SA", "AE", "IL", "TR", "TH", "MY",
    "ID", "PH", "VN", "PK", "BD", "NZ",
}
VALID_CURRENCIES = {
    "USD", "EUR", "GBP", "JPY", "BRL", "CNY", "INR", "CAD", "AUD", "MXN",
    "CHF", "SEK", "NOK", "DKK", "PLN", "CZK", "HUF", "RUB", "ZAR", "KRW",
    "SGD", "HKD", "TWD", "ARS", "CLP", "COP", "SAR", "AED", "TRY", "THB",
}
VALID_UOMS = {
    "EA", "KG", "G", "LB", "OZ", "L", "ML", "M", "CM", "MM",
    "M2", "M3", "PC", "BOX", "PAL", "ROL", "SET", "PR", "DZ", "HR",
}
VALID_PRODUCT_TYPES = {"FERT", "HALB", "ROH", "NLAG", "DIEN"}
VALID_COMPANY_CODES = {"1000", "2000", "3000", "4000", "5000"}
VALID_MRP_TYPES = {"PD", "VB", "ND", "MK", "VV"}
VALUATION_CLASS_BY_TYPE = {
    "FERT": "7920", "HALB": "7921", "ROH": "3000", "NLAG": "3001", "DIEN": "3002",
}

CUSTOMER_BP_OFFSET = 3000  # KUNNR numeric + this = BP_NUMBER to avoid collision with LIFNR


# ---------------------------------------------------------------------------
# Cleaning helpers
# ---------------------------------------------------------------------------

def clean(v) -> str:
    """Strip whitespace."""
    if v is None:
        return ""
    return str(v).strip()


def denull(v: str) -> str:
    """Normalize 'N/A' string to empty (= SQL NULL in loader convention)."""
    return "" if clean(v) in ("N/A", "n/a") else v


def normalize_date(v) -> str:
    """Convert YYYYMMDD or DD.MM.YYYY to YYYY-MM-DD. Returns '' on failure."""
    v = clean(v)
    if not v or v in ("N/A", "00000000", "0"):
        return ""
    if len(v) == 8 and v.isdigit():
        return f"{v[:4]}-{v[4:6]}-{v[6:]}"
    if len(v) == 10 and v[2] == "." and v[5] == ".":
        return f"{v[6:]}-{v[3:5]}-{v[:2]}"
    if len(v) == 10 and v[4] == "-":
        return v  # already ISO
    return ""


def fix_country(v) -> str:
    """Replace invalid country codes with DE fallback."""
    v = clean(v).upper()
    return v if v in VALID_COUNTRIES else ("DE" if v else "")


def fix_currency(v, default="EUR") -> str:
    """Replace invalid currency codes with default."""
    v = clean(v).upper()
    return v if v in VALID_CURRENCIES else default


def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(LEGACY_SEED / f"{name}.csv", dtype=str, keep_default_na=False)


def write_csv(name: str, rows: list[dict], fields: list[str]) -> None:
    out = OUTPUT_DIR / f"{name}.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  {name}.csv  →  {len(rows):,} rows")


# ---------------------------------------------------------------------------
# Code mapping builders
# ---------------------------------------------------------------------------

def build_ekorg_map(ekorg_values: set) -> dict:
    """Map legacy EKORG codes (1000, 3000 …) to S/4 PO01-PO05."""
    codes = sorted(ekorg_values - {""})
    targets = [f"PO{i:02d}" for i in range(1, 6)]
    return {k: targets[i % len(targets)] for i, k in enumerate(codes)}


def build_werks_map(werks_values: set) -> dict:
    """Map legacy WERKS codes to S/4 P001-P010."""
    codes = sorted(werks_values - {""})
    targets = [f"P{i:03d}" for i in range(1, 11)]
    return {k: targets[i % len(targets)] for i, k in enumerate(codes)}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading legacy CSVs...")
    lfa1 = read_csv("LFA1")
    lfb1 = read_csv("LFB1")
    lfbk = read_csv("LFBK")
    lfm1 = read_csv("LFM1")
    kna1 = read_csv("KNA1")
    knb1 = read_csv("KNB1")
    knbk = read_csv("KNBK")
    mara = read_csv("MARA")
    marc = read_csv("MARC")
    ska1 = read_csv("SKA1")
    skat = read_csv("SKAT")
    csks = read_csv("CSKS")
    ekko = read_csv("EKKO")
    ekpo = read_csv("EKPO")

    # Build code maps from actual data in the CSVs
    unique_ekorg = (
        set(lfm1["EKORG"].str.strip()) | set(ekko["EKORG"].str.strip())
    ) - {""}
    unique_werks = (
        set(marc["WERKS"].str.strip()) | set(ekpo["WERKS"].str.strip())
    ) - {""}
    ekorg_map = build_ekorg_map(unique_ekorg)
    werks_map = build_werks_map(unique_werks)

    print(f"  EKORG codes: {sorted(ekorg_map)} → {sorted(set(ekorg_map.values()))}")
    print(f"  WERKS codes: {sorted(werks_map)} → {sorted(set(werks_map.values()))}")

    # Filter to valid client rows
    def mandt_ok(df: pd.DataFrame) -> pd.DataFrame:
        return df[df["MANDT"].str.strip() == "100"]

    lfa1 = mandt_ok(lfa1)
    lfb1 = mandt_ok(lfb1)
    lfbk = mandt_ok(lfbk)
    lfm1 = mandt_ok(lfm1)
    kna1 = mandt_ok(kna1)
    knb1 = mandt_ok(knb1)
    knbk = mandt_ok(knbk)
    mara = mandt_ok(mara)
    marc = mandt_ok(marc)
    ska1 = mandt_ok(ska1)
    skat = mandt_ok(skat)
    csks = mandt_ok(csks)
    ekko = mandt_ok(ekko)
    ekpo = mandt_ok(ekpo)

    # Remove soft-deleted vendors/customers
    vendors = lfa1[lfa1["LOEVM"].str.strip() != "X"].copy()
    customers = kna1[kna1["LOEVM"].str.strip() != "X"].copy()

    valid_vendor_lifnr = set(vendors["LIFNR"].str.strip())

    # Lookup helpers
    lfb1_by_lifnr = lfb1.groupby(lfb1["LIFNR"].str.strip())
    knb1_by_kunnr = knb1.groupby(knb1["KUNNR"].str.strip())

    print(f"\n  Vendors: {len(vendors):,}  |  Customers: {len(customers):,}")
    print("\nGenerating S/4HANA CSVs...")

    # ── BusinessPartner ──────────────────────────────────────────────────────
    bp_rows = []
    bp_type_map: dict[str, str] = {}

    for _, v in vendors.iterrows():
        bp_num = clean(v["LIFNR"])
        name1 = clean(denull(v["NAME1"]))
        if not name1 or not bp_num:
            continue
        country = fix_country(v.get("LAND1", "")) or "DE"
        grp = lfb1_by_lifnr.get_group(bp_num) if bp_num in lfb1_by_lifnr.groups else None
        currency = fix_currency(grp["WAERS"].iloc[0] if grp is not None else "EUR")
        bp_type_map[bp_num] = "VEND"
        bp_rows.append({
            "BP_NUMBER": bp_num,
            "bp_type": "VEND",
            "NAME1": name1[:255],
            "NAME2": clean(denull(v.get("NAME2", "")))[:255],
            "COUNTRY": country,
            "CURRENCY": currency,
            "TAX_NUMBER": clean(denull(v.get("STCD1", "")))[:20],
            "LANGUAGE": clean(v.get("SPRAS", ""))[:2],
            "created_at": normalize_date(v.get("ERDAT", "")),
        })

    for _, c in customers.iterrows():
        kunnr_raw = clean(c["KUNNR"])
        try:
            bp_num = f"{int(kunnr_raw) + CUSTOMER_BP_OFFSET:010d}"
        except ValueError:
            continue
        name1 = clean(denull(c["NAME1"]))
        if not name1:
            continue
        country = fix_country(c.get("LAND1", "")) or "DE"
        grp = knb1_by_kunnr.get_group(kunnr_raw) if kunnr_raw in knb1_by_kunnr.groups else None
        currency = fix_currency(grp["WAERS"].iloc[0] if grp is not None else "EUR")
        bp_type_map[bp_num] = "CUST"
        bp_rows.append({
            "BP_NUMBER": bp_num,
            "bp_type": "CUST",
            "NAME1": name1[:255],
            "NAME2": clean(denull(c.get("NAME2", "")))[:255],
            "COUNTRY": country,
            "CURRENCY": currency,
            "TAX_NUMBER": clean(denull(c.get("STCD1", "")))[:20],
            "LANGUAGE": clean(c.get("SPRAS", ""))[:2],
            "created_at": normalize_date(c.get("ERDAT", "")),
        })

    write_csv("BusinessPartner", bp_rows,
        ["BP_NUMBER", "bp_type", "NAME1", "NAME2", "COUNTRY", "CURRENCY",
         "TAX_NUMBER", "LANGUAGE", "created_at"])
    valid_bp_numbers = {r["BP_NUMBER"] for r in bp_rows}

    # ── BPRole ───────────────────────────────────────────────────────────────
    role_map = {"VEND": ["FLVN01"], "CUST": ["FLCU01"], "BOTH": ["FLVN01", "FLCU01"]}
    role_rows = [
        {"BP_NUMBER": bp_num, "ROLE_CODE": rc,
         "VALID_FROM": "2000-01-01", "VALID_TO": "9999-12-31"}
        for bp_num, bp_type in bp_type_map.items()
        for rc in role_map.get(bp_type, ["FLVN01"])
    ]
    write_csv("BPRole", role_rows, ["BP_NUMBER", "ROLE_CODE", "VALID_FROM", "VALID_TO"])

    # ── BPBankAccount ─────────────────────────────────────────────────────────
    bank_rows = []
    seen_bank = set()

    def add_bank(bp_num, row):
        if bp_num not in valid_bp_numbers:
            return
        bank_country = fix_country(row.get("BANKS", "")) or "DE"
        bank_key = clean(row.get("BANKL", ""))[:15]
        bank_acct = clean(row.get("BANKN", ""))[:18]
        if not bank_key or not bank_acct:
            return
        pk = (bp_num, bank_country, bank_key, bank_acct)
        if pk in seen_bank:
            return
        seen_bank.add(pk)
        bank_rows.append({
            "BP_NUMBER": bp_num,
            "BANK_COUNTRY": bank_country,
            "BANK_KEY": bank_key,
            "BANK_ACCOUNT": bank_acct,
            "IBAN": clean(row.get("IBAN", ""))[:34],
            "SWIFT": clean(row.get("SWIFT", ""))[:11],
        })

    for _, row in lfbk.iterrows():
        add_bank(clean(row["LIFNR"]), row)

    for _, row in knbk.iterrows():
        kunnr_raw = clean(row["KUNNR"])
        try:
            bp_num = f"{int(kunnr_raw) + CUSTOMER_BP_OFFSET:010d}"
        except ValueError:
            continue
        add_bank(bp_num, row)

    write_csv("BPBankAccount", bank_rows,
        ["BP_NUMBER", "BANK_COUNTRY", "BANK_KEY", "BANK_ACCOUNT", "IBAN", "SWIFT"])

    # ── BPAddress ────────────────────────────────────────────────────────────
    addr_rows = []
    seen_addr = set()

    def add_address(bp_num, row, name_col_prefix=""):
        if bp_num in seen_addr or bp_num not in valid_bp_numbers:
            return
        seen_addr.add(bp_num)
        addr_rows.append({
            "BP_NUMBER": bp_num,
            "STREET": clean(denull(row.get("STRAS", "")))[:255],
            "CITY": clean(denull(row.get("ORT01", "")))[:255],
            "POSTAL_CODE": clean(row.get("PSTLZ", ""))[:10],
            "COUNTRY": fix_country(row.get("LAND1", "")) or "DE",
            "REGION": clean(row.get("REGIO", ""))[:3],
            "ADDR_TYPE": "01",
        })

    for _, v in vendors.iterrows():
        add_address(clean(v["LIFNR"]), v)

    for _, c in customers.iterrows():
        kunnr_raw = clean(c["KUNNR"])
        try:
            bp_num = f"{int(kunnr_raw) + CUSTOMER_BP_OFFSET:010d}"
        except ValueError:
            continue
        add_address(bp_num, c)

    write_csv("BPAddress", addr_rows,
        ["BP_NUMBER", "STREET", "CITY", "POSTAL_CODE", "COUNTRY", "REGION", "ADDR_TYPE"])

    # ── BPCompanyCode ─────────────────────────────────────────────────────────
    bpc_rows = []
    seen_bpc = set()

    for _, row in lfb1.iterrows():
        lifnr = clean(row["LIFNR"])
        if lifnr not in valid_bp_numbers:
            continue
        bukrs = clean(row.get("BUKRS", ""))
        if bukrs not in VALID_COMPANY_CODES:
            continue
        pk = (lifnr, bukrs)
        if pk in seen_bpc:
            continue
        seen_bpc.add(pk)
        bpc_rows.append({
            "BP_NUMBER": lifnr,
            "COMPANY_CODE": bukrs,
            "RECONCILIATION_ACCOUNT": clean(row.get("AKONT", ""))[:10],
            "PAYMENT_TERMS": clean(row.get("ZTERM", ""))[:4],
            "CURRENCY": fix_currency(row.get("WAERS", "EUR")),
        })

    for _, row in knb1.iterrows():
        kunnr_raw = clean(row["KUNNR"])
        try:
            bp_num = f"{int(kunnr_raw) + CUSTOMER_BP_OFFSET:010d}"
        except ValueError:
            continue
        if bp_num not in valid_bp_numbers:
            continue
        bukrs = clean(row.get("BUKRS", ""))
        if bukrs not in VALID_COMPANY_CODES:
            continue
        pk = (bp_num, bukrs)
        if pk in seen_bpc:
            continue
        seen_bpc.add(pk)
        bpc_rows.append({
            "BP_NUMBER": bp_num,
            "COMPANY_CODE": bukrs,
            "RECONCILIATION_ACCOUNT": clean(row.get("AKONT", ""))[:10],
            "PAYMENT_TERMS": clean(row.get("ZTERM", ""))[:4],
            "CURRENCY": fix_currency(row.get("WAERS", "EUR")),
        })

    write_csv("BPCompanyCode", bpc_rows,
        ["BP_NUMBER", "COMPANY_CODE", "RECONCILIATION_ACCOUNT", "PAYMENT_TERMS", "CURRENCY"])

    # ── BPPurchasingOrg ───────────────────────────────────────────────────────
    bpp_rows = []
    seen_bpp = set()

    for _, row in lfm1.iterrows():
        lifnr = clean(row["LIFNR"])
        if lifnr not in valid_bp_numbers:
            continue
        ekorg_raw = clean(row.get("EKORG", ""))
        purch_org = ekorg_map.get(ekorg_raw, "PO01")
        pk = (lifnr, purch_org)
        if pk in seen_bpp:
            continue
        seen_bpp.add(pk)
        bpp_rows.append({
            "BP_NUMBER": lifnr,
            "PURCH_ORG": purch_org,
            "INCOTERMS": clean(row.get("INCO1", ""))[:3],
            "PAYMENT_TERMS": "",  # LFM1 has no ZTERM; leave blank
            "CURRENCY": fix_currency(row.get("WAERS", "EUR")),
        })

    write_csv("BPPurchasingOrg", bpp_rows,
        ["BP_NUMBER", "PURCH_ORG", "INCOTERMS", "PAYMENT_TERMS", "CURRENCY"])

    # ── Product ───────────────────────────────────────────────────────────────
    matnr_map: dict[str, str] = {}
    product_rows = []
    product_idx = 0

    # First WERKS per MATNR from MARC for valuation
    marc_stripped = marc.copy()
    marc_stripped["_matnr"] = marc_stripped["MATNR"].str.strip()
    marc_stripped["_werks"] = marc_stripped["WERKS"].str.strip()
    first_werks = marc_stripped.drop_duplicates("_matnr").set_index("_matnr")["_werks"].to_dict()

    for _, row in mara.iterrows():
        matnr = clean(row["MATNR"])
        if not matnr or matnr in matnr_map:
            continue
        product_idx += 1
        prod_num = f"P{product_idx:09d}"
        matnr_map[matnr] = prod_num

        mtart = clean(row.get("MTART", ""))
        prod_type = mtart if mtart in VALID_PRODUCT_TYPES else "ROH"
        meins = clean(row.get("MEINS", "EA"))
        base_unit = meins if meins in VALID_UOMS else "EA"
        spart = clean(row.get("SPART", ""))
        division = spart if spart in {"01", "02", "03", "04", "05"} else "01"

        product_rows.append({
            "PRODUCT_NUMBER": prod_num,
            "PRODUCT_TYPE": prod_type,
            "BASE_UNIT": base_unit,
            "WEIGHT": clean(row.get("BRGEW", ""))[:10],
            "WEIGHT_UNIT": (clean(row.get("GEWEI", "KG")) or "KG")[:10],
            "VOLUME": clean(row.get("VOLUM", ""))[:10],
            "VOLUME_UNIT": clean(row.get("VOLEH", ""))[:10],
            "PRODUCT_GROUP": "MECH",
            "DIVISION": division,
            "ERDAT": normalize_date(row.get("ERSDA", "") or row.get("ERDAT", "")),
        })

    write_csv("Product", product_rows,
        ["PRODUCT_NUMBER", "PRODUCT_TYPE", "BASE_UNIT", "WEIGHT", "WEIGHT_UNIT",
         "VOLUME", "VOLUME_UNIT", "PRODUCT_GROUP", "DIVISION", "ERDAT"])

    # ── ProductPlant ─────────────────────────────────────────────────────────
    pp_rows = []
    seen_pp = set()

    for _, row in marc.iterrows():
        matnr = clean(row["MATNR"])
        prod_num = matnr_map.get(matnr)
        if not prod_num:
            continue
        werks_raw = clean(row.get("WERKS", ""))
        plant = werks_map.get(werks_raw, "P001")
        pk = (prod_num, plant)
        if pk in seen_pp:
            continue
        seen_pp.add(pk)
        mrp = clean(row.get("DISMM", ""))[:2]
        pp_rows.append({
            "PRODUCT_NUMBER": prod_num,
            "PLANT": plant,
            "MRP_TYPE": mrp if mrp in VALID_MRP_TYPES else "PD",
            "SAFETY_STOCK": (clean(row.get("EISBE", "")) or "0")[:10],
            "REORDER_POINT": (clean(row.get("MINBE", "")) or "0")[:10],
            "LOT_SIZE": (clean(row.get("DISLS", "")) or "EX")[:10],
        })

    write_csv("ProductPlant", pp_rows,
        ["PRODUCT_NUMBER", "PLANT", "MRP_TYPE", "SAFETY_STOCK", "REORDER_POINT", "LOT_SIZE"])

    # ── ProductValuation ─────────────────────────────────────────────────────
    pv_rows = []

    for _, row in mara.iterrows():
        matnr = clean(row["MATNR"])
        prod_num = matnr_map.get(matnr)
        if not prod_num:
            continue
        werks_raw = first_werks.get(matnr, "")
        val_area = werks_map.get(werks_raw, "P001")
        mtart = clean(row.get("MTART", ""))
        prod_type = mtart if mtart in VALID_PRODUCT_TYPES else "ROH"
        pv_rows.append({
            "PRODUCT_NUMBER": prod_num,
            "VALUATION_AREA": val_area,
            "VALUATION_CLASS": VALUATION_CLASS_BY_TYPE.get(prod_type, "3000"),
            "STANDARD_PRICE": "0.00",
            "PRICE_UNIT": "1",
            "CURRENCY": "EUR",
        })

    write_csv("ProductValuation", pv_rows,
        ["PRODUCT_NUMBER", "VALUATION_AREA", "VALUATION_CLASS",
         "STANDARD_PRICE", "PRICE_UNIT", "CURRENCY"])

    # ── GLAccount ─────────────────────────────────────────────────────────────
    # Build description map from SKAT (prefer SPRAS=E for English)
    desc_map: dict[str, str] = {}
    for _, row in skat.iterrows():
        saknr = clean(row["SAKNR"])
        spras = clean(row.get("SPRAS", ""))
        desc = (clean(row.get("TXT20", "")) or clean(row.get("TXT50", "")))[:255]
        if saknr not in desc_map or spras in ("E", "EN"):
            desc_map[saknr] = desc

    gl_rows = []
    seen_gl: set = set()
    for _, row in ska1.iterrows():
        saknr = clean(row["SAKNR"])
        if saknr in seen_gl:
            continue
        seen_gl.add(saknr)
        try:
            acct_num = f"{int(saknr):010d}"
        except ValueError:
            acct_num = saknr[:10].zfill(10)
        gl_rows.append({
            "ACCOUNT_NUMBER": acct_num,
            "CHART_OF_ACCOUNTS": (clean(row.get("KTOPL", "INT")) or "INT")[:4],
            "ACCOUNT_TYPE": "S",
            "DESCRIPTION": desc_map.get(saknr, "")[:255],
            "CREATED_AT": normalize_date(row.get("ERDAT", "")),
        })

    write_csv("GLAccount", gl_rows,
        ["ACCOUNT_NUMBER", "CHART_OF_ACCOUNTS", "ACCOUNT_TYPE", "DESCRIPTION", "CREATED_AT"])

    # ── CostCenter ───────────────────────────────────────────────────────────
    cc_rows = []
    seen_cc: set = set()
    for _, row in csks.iterrows():
        kostl = clean(row["KOSTL"])
        kokrs = (clean(row.get("KOKRS", "")) or "CO01")[:4]
        pk = (kostl, kokrs)
        if pk in seen_cc:
            continue
        seen_cc.add(pk)
        bukrs = clean(row.get("BUKRS", ""))
        cc_rows.append({
            "COST_CENTER": kostl[:10],
            "CONTROLLING_AREA": kokrs,
            "COMPANY_CODE": bukrs if bukrs in VALID_COMPANY_CODES else "1000",
            "DESCRIPTION": clean(row.get("KTEXT", ""))[:255],
            "VALID_FROM": normalize_date(row.get("DATAB", "")) or "2000-01-01",
            "VALID_TO": normalize_date(row.get("DATBI", "")) or "9999-12-31",
        })

    write_csv("CostCenter", cc_rows,
        ["COST_CENTER", "CONTROLLING_AREA", "COMPANY_CODE",
         "DESCRIPTION", "VALID_FROM", "VALID_TO"])

    # ── ProfitCenter (synthetic — no direct ECC source) ───────────────────────
    segments = ["MFCT", "SERV", "DIST", "RETL", "CORP"]
    pc_rows = [
        {
            "PROFIT_CENTER": f"PC{n + 1:08d}",
            "CONTROLLING_AREA": "CO01",
            "DESCRIPTION": f"Profit Center {n + 1:03d} ({segments[n % len(segments)]})",
            "SEGMENT": segments[n % len(segments)],
        }
        for n in range(40)
    ]
    write_csv("ProfitCenter", pc_rows,
        ["PROFIT_CENTER", "CONTROLLING_AREA", "DESCRIPTION", "SEGMENT"])

    # ── PurchaseOrder ─────────────────────────────────────────────────────────
    po_rows = []
    seen_po: set = set()
    for _, row in ekko.iterrows():
        ebeln = clean(row["EBELN"])
        if ebeln in seen_po:
            continue
        lifnr = clean(row.get("LIFNR", ""))
        # Filter orphan FK and vendors not in our BP set
        if lifnr not in valid_vendor_lifnr or lifnr not in valid_bp_numbers:
            continue
        ekorg_raw = clean(row.get("EKORG", ""))
        bukrs = clean(row.get("BUKRS", ""))
        seen_po.add(ebeln)
        po_rows.append({
            "PO_NUMBER": ebeln,
            "VENDOR": lifnr,
            "COMPANY_CODE": bukrs if bukrs in VALID_COMPANY_CODES else "1000",
            "PURCH_ORG": ekorg_map.get(ekorg_raw, "PO01"),
            "CURRENCY": fix_currency(row.get("WAERS", "USD"), default="USD"),
            "DOCUMENT_DATE": normalize_date(row.get("BEDAT", "")),
            "STATUS": "OPEN",
        })

    write_csv("PurchaseOrder", po_rows,
        ["PO_NUMBER", "VENDOR", "COMPANY_CODE", "PURCH_ORG",
         "CURRENCY", "DOCUMENT_DATE", "STATUS"])
    valid_po_numbers = {r["PO_NUMBER"] for r in po_rows}

    # ── PurchaseOrderItem ─────────────────────────────────────────────────────
    ekko_waers = ekko.set_index(ekko["EBELN"].str.strip())["WAERS"].to_dict()

    poi_rows = []
    seen_poi: set = set()
    for _, row in ekpo.iterrows():
        ebeln = clean(row["EBELN"])
        if ebeln not in valid_po_numbers:
            continue
        ebelp = clean(row.get("EBELP", ""))
        pk = (ebeln, ebelp)
        if pk in seen_poi:
            continue
        seen_poi.add(pk)
        matnr = clean(row.get("MATNR", ""))
        werks_raw = clean(row.get("WERKS", ""))
        poi_rows.append({
            "PO_NUMBER": ebeln,
            "ITEM_NUMBER": ebelp[:6],
            "PRODUCT": matnr_map.get(matnr, "")[:10],
            "PLANT": werks_map.get(werks_raw, "P001") if werks_raw else "",
            "QUANTITY": clean(row.get("MENGE", ""))[:10],
            "UNIT": (clean(row.get("MEINS", "")) or "EA")[:10],
            "NET_PRICE": clean(row.get("NETPR", ""))[:15],
            "CURRENCY": fix_currency(ekko_waers.get(ebeln, "USD"), default="USD"),
            "DELIVERY_DATE": "",
        })

    write_csv("PurchaseOrderItem", poi_rows,
        ["PO_NUMBER", "ITEM_NUMBER", "PRODUCT", "PLANT",
         "QUANTITY", "UNIT", "NET_PRICE", "CURRENCY", "DELIVERY_DATE"])

    total = sum(1 for _ in OUTPUT_DIR.glob("*.csv"))
    print(f"\nDone! {total} CSV files written to {OUTPUT_DIR}")


if __name__ == "__main__":
    if not LEGACY_SEED.exists():
        print(f"ERROR: Legacy seed dir not found: {LEGACY_SEED}", file=sys.stderr)
        sys.exit(1)
    main()
