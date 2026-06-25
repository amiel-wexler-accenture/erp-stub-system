#!/usr/bin/env python3
"""
Generate SAP ECC seed CSVs from SAP Datasphere bike content.

Usage (from legacy-erp/data/):  python generate_seed.py
Output: seed/*.csv  (20 files, ~58,000 rows total)

Dependencies: pip install faker pandas
"""

import csv
import random
from pathlib import Path

import pandas as pd
from faker import Faker

SCRIPT_DIR = Path(__file__).parent
SOURCE_DIR = (
    SCRIPT_DIR / "source" / "datasphere-content-main" / "SAP_Sample_Content" / "CSV"
)
SEED_DIR = SCRIPT_DIR / "seed"
SEED_DIR.mkdir(exist_ok=True)

Faker.seed(42)
random.seed(42)
fake = Faker(["en_US", "en_GB", "de_DE", "fr_FR", "ja_JP", "pt_BR"])

# ── Constants ─────────────────────────────────────────────────────────────────
_UNICODE = [
    "Müller GmbH", "Société Générale", "日本電気株式会社", "شركة أرامكو السعودية",
]
_COUNTRIES = [
    "US","DE","GB","FR","JP","BR","CN","CA","AU","IT",
    "ES","NL","SE","CH","AT","BE","PL","MX","KR","IN",
]
_BAD_COUNTRIES = ["XX","ZZ","QQ"]
_BRSCH = list("ABCDEFGHIJKLMNOPQRST")
_BAD_BRSCH = ["999","000","XYZ"]
_CURRENCIES = ["USD","EUR","GBP","JPY","BRL","CHF","CAD","AUD","CNY","KRW"]
_BUKRS = ["1000","2000","3000","4000","5000"]
_EKORG = ["1000","2000","3000","4000","5000"]
_WERKS = ["1000","1001","1002","2000","2001","3000","3001","4000","5000","5001"]
_VKORG = ["1000","2000","3000"]
_VTWEG = ["10","20","30"]
_SPART = ["00","01","02","03","04"]
_LANGS = ["E","D","F","J","P"]
_MEINS = ["ST","KG","L","M","M2","M3","EA","PC"]
_INCO1 = ["EXW","FCA","CPT","CIP","DAT","DAP","DDP","FOB","CFR","CIF"]
_ZTERM = ["0001","0002","0003","NT30","NT60","NT90","2/10NET30"]
_MTART_MAP = {"FG":"FERT","CR":"ROH","MT":"ROH","RB":"HALB","RC":"HALB","TM":"DIEN"}
_SALESORG_EKORG = {"APJ":"3000","EMEA":"2000","AMER":"1000"}


# ── DQ helpers ────────────────────────────────────────────────────────────────
def ts(v):
    """DQ#1: trailing space injection ~20%."""
    return v + "   " if v and random.random() < 0.20 else v


def nv():
    """DQ#2: inconsistent null — empty cell (→ SQL NULL) or 'N/A' string."""
    return "" if random.random() < 0.5 else "N/A"


def erdat():
    """DQ#6: date as YYYYMMDD or DD.MM.YYYY format, mixed across rows."""
    d = fake.date_between(start_date="-15y", end_date="today")
    return d.strftime("%Y%m%d") if random.random() < 0.5 else d.strftime("%d.%m.%Y")


def mandt():
    """DQ#9: ~0.5% wrong client contamination."""
    return "200" if random.random() < 0.005 else "100"


def land1():
    """DQ#5: ~3% invalid country codes."""
    return (
        random.choice(_BAD_COUNTRIES) if random.random() < 0.03
        else random.choice(_COUNTRIES)
    )


def brsch():
    """DQ#5: ~3% invalid industry codes."""
    return (
        random.choice(_BAD_BRSCH) if random.random() < 0.03
        else random.choice(_BRSCH)
    )


def name1(fallback=None):
    """DQ#7: ~5% Unicode company names."""
    if random.random() < 0.05:
        return random.choice(_UNICODE)
    return fallback or fake.company()


# ── CSV writer ────────────────────────────────────────────────────────────────
def write(table_name, rows, cols):
    path = SEED_DIR / f"{table_name}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            # Ensure every column has an entry; missing → empty cell (SQL NULL)
            w.writerow({c: row.get(c, "") for c in cols})
    print(f"  {table_name:<8s}  {len(rows):>6,d} rows  →  {path.name}")


# ── Load source CSVs ──────────────────────────────────────────────────────────
print("Loading source CSVs …")
bp_df = pd.read_csv(SOURCE_DIR / "Sales/BusinessPartners.csv", sep=";")
products_df = pd.read_csv(SOURCE_DIR / "FI/Products.csv", dtype=str)
products_df = products_df[products_df["PRODUCTID"] != "#"].reset_index(drop=True)
orders_df = pd.read_csv(SOURCE_DIR / "Sales/SalesOrders.csv", sep=";", dtype=str, encoding="utf-8-sig")
items_df = pd.read_csv(SOURCE_DIR / "Sales/SalesOrderItems.csv", sep=";", dtype=str, encoding="utf-8-sig")

vendors_src = bp_df[bp_df["PARTNERROLE"].astype(str) == "1"].reset_index(drop=True)
customers_src = bp_df[bp_df["PARTNERROLE"].astype(str) == "2"].reset_index(drop=True)

print(
    f"  BusinessPartners: {len(vendors_src)} vendors, {len(customers_src)} customers\n"
    f"  Products: {len(products_df)} rows\n"
    f"  SalesOrders: {len(orders_df)} rows\n"
    f"  SalesOrderItems: {len(items_df)} rows"
)

print("\nGenerating seed tables …")

# ── LFA1 ──────────────────────────────────────────────────────────────────────
LFA1_COLS = [
    "MANDT","LIFNR","LAND1","NAME1","NAME2","NAME3","NAME4","ORT01","ORT02",
    "PFACH","PSTL2","PSTLZ","REGIO","SORTL","STRAS","ADRNR","MCOD1","MCOD2",
    "MCOD3","ANRED","BAHNS","BBBNR","BBSNR","BEGRU","BRSCH","BUBKZ","DATLT",
    "DTAMS","DTAWS","ERDAT","ERNAM","ESRNR","KONZS","KTOKK","KUNNR","LNRZA",
    "LOEVM","SPERR","SPERM","SPRAS","STCD1","STCD2","STKZA","STKZU","TELBX",
    "TELF1","TELF2","TELFX","TELTX","TELX1","XCPDK","XZEMP","VBUND","FISKN",
    "STCEG","STKZN","SPERQ","GBORT","GBDAT","SEXKZ","KRAUS","REVDB","QSSYS",
    "KTOCK","PFORT","WERKS","LTSNA","WERKR","PLKAL","DUEFL","TXJCD","SPERZ",
    "SCACD","SFRGR","LZONE","XLFZA","DLGRP","STCD3","STCD4","STCD5","PROFS",
    "EMNFR","LFURL","CONFS","UPDAT","UPTIM","NODEL","PODKZB",
]

lfa1_rows = []
lifnr_list = []
dup_names = []

for n in range(1, 2001):
    lifnr = f"{n:010d}"
    lifnr_list.append(lifnr)

    # Anchor: real bike company data for first len(vendors_src) rows
    src_idx = n - 1
    if src_idx < len(vendors_src):
        src = vendors_src.iloc[src_idx]
        cname = str(src["COMPANYNAME"]) if pd.notna(src["COMPANYNAME"]) else fake.company()
        telf1 = str(src["PHONENUMBER"]) if pd.notna(src.get("PHONENUMBER")) else fake.phone_number()[:16]
        telfx = str(src["FAXNUMBER"]) if pd.notna(src.get("FAXNUMBER")) and str(src.get("FAXNUMBER", "")).strip() else ""
        lfurl = str(src["WEBADDRESS"]) if pd.notna(src.get("WEBADDRESS")) else ""
        raw_date = str(src.get("CREATEDAT", "")).replace("-", "")
        erdat_val = raw_date[:8] if len(raw_date) >= 8 else erdat()
        ernam = str(src.get("CREATEDBY", fake.user_name()))[:12]
        land1_val = random.choice(_COUNTRIES)
    else:
        cname = fake.company()
        telf1 = fake.phone_number()[:16]
        telfx = fake.phone_number()[:16] if random.random() < 0.5 else ""
        lfurl = fake.url() if random.random() < 0.4 else ""
        erdat_val = erdat()
        ernam = fake.user_name()[:12]
        land1_val = land1()

    # DQ#3: near-duplicate record (~2%)
    n1 = name1(cname)
    if n > 50 and random.random() < 0.02 and dup_names:
        n1 = random.choice(dup_names)
    else:
        dup_names.append(n1)
        if len(dup_names) > 100:
            dup_names.pop(0)

    # DQ#8: deletion flag (~5%)
    loevm = "X" if random.random() < 0.05 else ""

    lfa1_rows.append({
        "MANDT": mandt(),
        "LIFNR": lifnr,
        "LAND1": land1_val,
        "NAME1": ts(n1),
        "NAME2": nv() if random.random() < 0.30 else fake.company_suffix(),
        "NAME3": nv() if random.random() < 0.50 else fake.bs()[:20],
        "NAME4": nv() if random.random() < 0.70 else "",
        "ORT01": ts(fake.city()),
        "ORT02": nv() if random.random() < 0.40 else fake.city(),
        "PFACH": nv() if random.random() < 0.60 else fake.postcode(),
        "PSTL2": fake.postcode(),
        "PSTLZ": fake.postcode(),
        "REGIO": fake.state_abbr(),
        "SORTL": ts(n1[:10].upper()),
        "STRAS": ts(fake.street_address()),
        "ADRNR": fake.numerify("######"),
        "MCOD1": ts(n1[:25].upper()),
        "ANRED": random.choice(["Firma","Herr","Frau","Mr.","Ms.",""]),
        "BEGRU": random.choice(["0001","0002","0003",""]),
        "BRSCH": brsch(),
        "ERDAT": erdat_val,
        "ERNAM": ernam,
        "KTOKK": random.choice(["LIEF","KRED","0001"]),
        "LOEVM": loevm,
        "SPRAS": random.choice(_LANGS),
        "STCD1": nv() if random.random() < 0.20 else fake.numerify("##########"),
        "STKZU": random.choice(["X",""]),
        "TELF1": ts(telf1),
        "TELF2": "" if random.random() < 0.60 else fake.phone_number()[:16],
        "TELFX": ts(telfx) if telfx else "",
        "STCEG": "" if random.random() < 0.30 else "DE" + fake.numerify("###########"),
        "WERKS": random.choice(_WERKS),
        "PLKAL": random.choice(["01","02","03",""]),
        "LFURL": lfurl,
        "UPDAT": fake.date_between(start_date="-2y", end_date="today").strftime("%Y%m%d"),
        "UPTIM": fake.time(pattern="%H%M%S"),
    })

write("LFA1", lfa1_rows, LFA1_COLS)

# ── LFB1 ──────────────────────────────────────────────────────────────────────
LFB1_COLS = [
    "MANDT","LIFNR","BUKRS","PERNR","ALTKN","BEGRU","ZUAWA","AKONT","ALTKT",
    "ALTKN2","ZTERM","WAERS","FDGRP","REPRF","TOGRP","LNRZE","LNRZB","ZINDT",
    "ZINRT","DATLZ","ALTKZ","MINDK","INTAD","KVERM","BUSAB","UBBZG","EXPKK",
    "ABSBE","ZFBDT","SKFOR","SKNTO","MANDT_OVERRIDE",
]
lfb1_rows = []
for _ in range(3000):
    lifnr = random.choice(lifnr_list)
    lfb1_rows.append({
        "MANDT": mandt(),
        "LIFNR": lifnr,
        "BUKRS": random.choice(_BUKRS),
        "AKONT": fake.numerify("######"),
        "ZTERM": random.choice(_ZTERM),
        "WAERS": random.choice(_CURRENCIES),
        "ZUAWA": random.choice(["001","002","003"]),
        "BEGRU": random.choice(["0001","0002","0003",""]),
        "REPRF": random.choice(["X",""]),
        "BUSAB": fake.bothify("??"),
    })
write("LFB1", lfb1_rows, LFB1_COLS)

# ── LFBK ──────────────────────────────────────────────────────────────────────
LFBK_COLS = [
    "MANDT","LIFNR","BANKS","BANKL","BANKN","BKONT","BVTYP","XEZER","BANKA",
    "PROVZ","STRAS","ORT01","SWIFT","IBAN","KOINH","KOVON","KOBIS",
]
lfbk_rows = []
for _ in range(2000):
    lifnr = random.choice(lifnr_list)
    country = random.choice(_COUNTRIES)
    lfbk_rows.append({
        "MANDT": mandt(),
        "LIFNR": lifnr,
        "BANKS": country,
        "BANKL": fake.numerify("########"),
        "BANKN": fake.numerify("##########"),
        "BANKA": ts(fake.company()),
        "STRAS": ts(fake.street_address()),
        "ORT01": ts(fake.city()),
        "SWIFT": fake.swift(),
        "IBAN": fake.iban(),
        "KOINH": "" if random.random() < 0.50 else fake.name(),
    })
write("LFBK", lfbk_rows, LFBK_COLS)

# ── LFAS ──────────────────────────────────────────────────────────────────────
LFAS_COLS = ["MANDT","LIFNR","EKORG","SPERM","LOEVM","VENSL","BSTAE"]
lfas_rows = []
for _ in range(2500):
    lfas_rows.append({
        "MANDT": mandt(),
        "LIFNR": random.choice(lifnr_list),
        "EKORG": random.choice(_EKORG),
        "LOEVM": "X" if random.random() < 0.02 else "",
        "BSTAE": random.choice(["0001","0002","0003",""]),
    })
write("LFAS", lfas_rows, LFAS_COLS)

# ── LFM1 ──────────────────────────────────────────────────────────────────────
LFM1_COLS = [
    "MANDT","LIFNR","EKORG","WAERS","LIEFR","MINBW","KZABS","KZAUT","KZBESN",
    "MEPRF","INCO1","INCO2","WEBRE","KZWBK","BOAUF","BOKRE","BOSPE","BOSTA",
    "BOSPE2","UMSAE",
]
lfm1_rows = []
for _ in range(2500):
    lfm1_rows.append({
        "MANDT": mandt(),
        "LIFNR": random.choice(lifnr_list),
        "EKORG": random.choice(_EKORG),
        "WAERS": random.choice(_CURRENCIES),
        "INCO1": random.choice(_INCO1),
        "MEPRF": random.choice(["1","2","3",""]),
        "WEBRE": random.choice(["X",""]),
    })
write("LFM1", lfm1_rows, LFM1_COLS)

# ── LFM2 ──────────────────────────────────────────────────────────────────────
LFM2_COLS = [
    "MANDT","LIFNR","EKORG","WERKS","SPERM","LOEVM","PLIFZ","MNGLG","MNGKO",
    "MNGZE","UEBTO","UNTTO","UGBTO",
]
lfm2_rows = []
for _ in range(3000):
    lfm2_rows.append({
        "MANDT": mandt(),
        "LIFNR": random.choice(lifnr_list),
        "EKORG": random.choice(_EKORG),
        "WERKS": random.choice(_WERKS),
        "PLIFZ": str(random.randint(1, 30)),
        "UEBTO": str(round(random.uniform(0, 20), 1)),
        "UNTTO": str(round(random.uniform(0, 10), 1)),
    })
write("LFM2", lfm2_rows, LFM2_COLS)

# ── LFB5 ──────────────────────────────────────────────────────────────────────
LFB5_COLS = ["MANDT","LIFNR","BUKRS","MABER","MAHNS","MANDT2"]
lfb5_rows = []
for _ in range(1500):
    lfb5_rows.append({
        "MANDT": mandt(),
        "LIFNR": random.choice(lifnr_list),
        "BUKRS": random.choice(_BUKRS),
        "MABER": fake.bothify("??"),
        "MAHNS": str(random.randint(0, 5)),
    })
write("LFB5", lfb5_rows, LFB5_COLS)

# ── LFBW ──────────────────────────────────────────────────────────────────────
LFBW_COLS = ["MANDT","LIFNR","BUKRS","WITHT","WT_WITHCD","WT_EXPT","QSREC","WITHT2"]
lfbw_rows = []
for _ in range(1000):
    lfbw_rows.append({
        "MANDT": mandt(),
        "LIFNR": random.choice(lifnr_list),
        "BUKRS": random.choice(_BUKRS),
        "WITHT": fake.bothify("??"),
        "WT_WITHCD": fake.bothify("##"),
        "QSREC": random.choice(["G","N",""]),
    })
write("LFBW", lfbw_rows, LFBW_COLS)

# ── KNA1 ──────────────────────────────────────────────────────────────────────
KNA1_COLS = [
    "MANDT","KUNNR","LAND1","NAME1","NAME2","NAME3","NAME4","ORT01","ORT02",
    "PSTLZ","REGIO","SORTL","STRAS","TELF1","TELF2","TELFX","TELTX","XCPDK",
    "STCD1","STCD2","STKZU","ERDAT","ERNAM","KTOKD","SPRAS","ANRED","MCOD1",
    "MCOD2","MCOD3","LOEVM","SPERR",
]
kna1_rows = []
kunnr_list = []
dup_cnames = []

for n in range(1, 2001):
    kunnr = f"{n:010d}"
    kunnr_list.append(kunnr)

    src_idx = n - 1
    if src_idx < len(customers_src):
        src = customers_src.iloc[src_idx]
        cname = str(src["COMPANYNAME"]) if pd.notna(src["COMPANYNAME"]) else fake.company()
        telf1 = str(src["PHONENUMBER"]) if pd.notna(src.get("PHONENUMBER")) else fake.phone_number()[:16]
        raw_date = str(src.get("CREATEDAT", "")).replace("-", "")
        erdat_val = raw_date[:8] if len(raw_date) >= 8 else erdat()
        ernam = str(src.get("CREATEDBY", fake.user_name()))[:12]
        land1_val = random.choice(_COUNTRIES)
    else:
        cname = fake.company()
        telf1 = fake.phone_number()[:16]
        erdat_val = erdat()
        ernam = fake.user_name()[:12]
        land1_val = land1()

    n1 = name1(cname)
    if n > 50 and random.random() < 0.02 and dup_cnames:
        n1 = random.choice(dup_cnames)
    else:
        dup_cnames.append(n1)
        if len(dup_cnames) > 100:
            dup_cnames.pop(0)

    kna1_rows.append({
        "MANDT": mandt(),
        "KUNNR": kunnr,
        "LAND1": land1_val,
        "NAME1": ts(n1),
        "NAME2": nv() if random.random() < 0.30 else fake.company_suffix(),
        "NAME3": nv() if random.random() < 0.50 else "",
        "NAME4": "",
        "ORT01": ts(fake.city()),
        "ORT02": nv() if random.random() < 0.40 else fake.city(),
        "PSTLZ": fake.postcode(),
        "REGIO": fake.state_abbr(),
        "SORTL": ts(n1[:10].upper()),
        "STRAS": ts(fake.street_address()),
        "TELF1": ts(telf1),
        "TELF2": "" if random.random() < 0.70 else fake.phone_number()[:16],
        "TELFX": "" if random.random() < 0.60 else fake.phone_number()[:16],
        "STCD1": nv() if random.random() < 0.20 else fake.numerify("##########"),
        "STKZU": random.choice(["X",""]),
        "ERDAT": erdat_val,
        "ERNAM": ernam,
        "KTOKD": random.choice(["DEBI","0001","D001"]),
        "SPRAS": random.choice(_LANGS),
        "ANRED": random.choice(["Firma","Herr","Frau","Mr.","Ms.",""]),
        "MCOD1": ts(n1[:25].upper()),
        "LOEVM": "X" if random.random() < 0.03 else "",
    })

write("KNA1", kna1_rows, KNA1_COLS)

# ── KNB1 ──────────────────────────────────────────────────────────────────────
KNB1_COLS = ["MANDT","KUNNR","BUKRS","AKONT","ZTERM","WAERS","ZUAWA","BEGRU","ALTKN","REPRF"]
knb1_rows = []
for _ in range(2500):
    knb1_rows.append({
        "MANDT": mandt(),
        "KUNNR": random.choice(kunnr_list),
        "BUKRS": random.choice(_BUKRS),
        "AKONT": fake.numerify("######"),
        "ZTERM": random.choice(_ZTERM),
        "WAERS": random.choice(_CURRENCIES),
        "ZUAWA": random.choice(["001","002","003"]),
        "BEGRU": random.choice(["0001","0002","0003",""]),
        "REPRF": random.choice(["X",""]),
    })
write("KNB1", knb1_rows, KNB1_COLS)

# ── KNVV ──────────────────────────────────────────────────────────────────────
KNVV_COLS = [
    "MANDT","KUNNR","VKORG","VTWEG","SPART","BZIRK","VKBUR","KDGRP","WAERS",
    "ZTERM","INCO1","INCO2","KVGR1","KVGR2","KVGR3","KVGR4","KVGR5",
]
knvv_rows = []
for _ in range(3000):
    knvv_rows.append({
        "MANDT": mandt(),
        "KUNNR": random.choice(kunnr_list),
        "VKORG": random.choice(_VKORG),
        "VTWEG": random.choice(_VTWEG),
        "SPART": random.choice(_SPART),
        "WAERS": random.choice(_CURRENCIES),
        "ZTERM": random.choice(_ZTERM),
        "INCO1": random.choice(_INCO1),
        "KDGRP": fake.bothify("??"),
        "VKBUR": fake.numerify("####"),
    })
write("KNVV", knvv_rows, KNVV_COLS)

# ── KNBK ──────────────────────────────────────────────────────────────────────
KNBK_COLS = [
    "MANDT","KUNNR","BANKS","BANKL","BANKN","BKONT","BVTYP","XEZER",
    "BANKA","SWIFT","IBAN",
]
knbk_rows = []
for _ in range(2000):
    knbk_rows.append({
        "MANDT": mandt(),
        "KUNNR": random.choice(kunnr_list),
        "BANKS": random.choice(_COUNTRIES),
        "BANKL": fake.numerify("########"),
        "BANKN": fake.numerify("##########"),
        "BANKA": ts(fake.company()),
        "SWIFT": fake.swift(),
        "IBAN": fake.iban(),
    })
write("KNBK", knbk_rows, KNBK_COLS)

# ── MARA ──────────────────────────────────────────────────────────────────────
MARA_COLS = [
    "MANDT","MATNR","ERSDA","ERNAM","LAEDA","AENAM","MTART","MBRSH","MATKL",
    "MEINS","BSTME","ZEINR","ZEIVR","ZEIFO","AESZN","BLANZ","FERTH","FORMT",
    "NORMT","LABOR","EKWSL","BRGEW","GEWEI","NTGEW","VOLUM","VOLEH","BEHVO",
    "RAUBE","TEMPB","DISST","TRAGR","STOFF","SPART","VHART","FUELG","IPRKZ",
    "RDPRF","MHDRZ","MHDLP","MHDLF","BWVOR","BWSCL","SAISO","ETIAR","ETIFO",
    "ENTAR","EAN11","NUMTP","LAENG","BREIT","HOEHE","MEABM","PRDHA","CADKZ",
    "ERGEW","ERVOLM","WERKS","LMEINS","BRGEW2","GEWEI2",
]
mara_rows = []
matnr_list = []

# Anchor: real bike products first
products_index = products_df.set_index("PRODUCTID")

for n in range(1, 2001):
    src_idx = n - 1
    if src_idx < len(products_df):
        src = products_df.iloc[src_idx]
        matnr = str(src["PRODUCTID"])
        mtart = _MTART_MAP.get(str(src.get("PRODUCTCATEGORYID","")), "FERT")
        raw_weight = src.get("WEIGHTMEASURE","")
        brgew = str(round(float(raw_weight) / 1000.0, 3)) if str(raw_weight).replace(".","").isdigit() else str(round(random.uniform(0.5, 30.0), 3))
        gewei = str(src.get("WEIGHTUNIT","KG"))
        meins = str(src.get("QUANTITYUNIT","EA"))
        raw_date = str(src.get("CREATEDAT","")).replace("-","")
        ersda = raw_date[:8] if len(raw_date) >= 8 else erdat()
        ernam = str(src.get("CREATEDBY", fake.user_name()))[:12]
        raw_laeda = str(src.get("CHANGEDAT","")).replace("-","")
        laeda = raw_laeda[:8] if len(raw_laeda) >= 8 else fake.date_between(start_date="-2y", end_date="today").strftime("%Y%m%d")
        aenam = str(src.get("CHANGEDBY", fake.user_name()))[:12]
        width = str(src.get("WIDTH","")) or ""
        depth = str(src.get("DEPTH","")) or ""
        height = str(src.get("HEIGHT","")) or ""
        meabm = str(src.get("DIMENSIONUNIT","")) or ""
    else:
        seq = n - len(products_df)
        matnr = f"MAT{seq:07d}"
        mtart = random.choice(["ROH","HALB","FERT","HIBE","VERP","DIEN","NLAG","ERSA"])
        brgew = str(round(random.uniform(0.1, 1000.0), 3))
        gewei = "KG"
        meins = random.choice(_MEINS)
        ersda = erdat()
        ernam = fake.user_name()[:12]
        laeda = fake.date_between(start_date="-2y", end_date="today").strftime("%Y%m%d")
        aenam = fake.user_name()[:12]
        width = str(round(random.uniform(1, 200), 1))
        depth = str(round(random.uniform(1, 200), 1))
        height = str(round(random.uniform(1, 200), 1))
        meabm = random.choice(["CM","M","IN"])

    matnr_list.append(matnr)
    mara_rows.append({
        "MANDT": mandt(),
        "MATNR": matnr,
        "ERSDA": ersda,
        "ERNAM": ernam,
        "LAEDA": laeda,
        "AENAM": aenam,
        "MTART": mtart,
        "MBRSH": random.choice(["A","C","E","F","M","R"]),
        "MATKL": fake.numerify("######"),
        "MEINS": meins,
        "BSTME": meins,
        "BRGEW": brgew,
        "GEWEI": gewei,
        "NTGEW": str(round(float(brgew) * 0.9, 3)) if brgew else "",
        "VOLUM": str(round(random.uniform(0.001, 100), 3)),
        "VOLEH": random.choice(["L","M3","CM3"]),
        "SPART": random.choice(_SPART),
        "EAN11": fake.ean(length=13),
        "LAENG": width,
        "BREIT": depth,
        "HOEHE": height,
        "MEABM": meabm,
        "WERKS": random.choice(_WERKS),
    })

write("MARA", mara_rows, MARA_COLS)

# ── MARC ──────────────────────────────────────────────────────────────────────
MARC_COLS = [
    "MANDT","MATNR","WERKS","PSTAT","LVORM","BWTTY","XCHAR","MMSTA","MMSTD",
    "MAABC","KZKRI","EKGRP","DISMM","DISPO","DISLS","BERID","BSTMI","MINBE",
    "EISBE","MABST","STRGR","LGPRO","LGFSB","HERKL","INSMK","SSQSS","MTVFP",
    "KZAUS","AUSDT","NFMAT","MFLHN","KZBED","LGPBE","LGOBE","INSMK2",
]
marc_rows = []
for _ in range(5000):
    marc_rows.append({
        "MANDT": mandt(),
        "MATNR": random.choice(matnr_list),
        "WERKS": random.choice(_WERKS),
        "MAABC": random.choice(["A","B","C",""]),
        "EKGRP": fake.numerify("###"),
        "DISMM": random.choice(["PD","MRP","","VB"]),
        "DISPO": fake.bothify("???"),
        "INSMK": random.choice(["X",""]),
    })
write("MARC", marc_rows, MARC_COLS)

# ── MAKT ──────────────────────────────────────────────────────────────────────
MAKT_COLS = ["MANDT","MATNR","SPRAS","MAKTX","MAKTG"]
makt_rows = []
for _ in range(3000):
    maktx = ts(fake.catch_phrase()[:40])
    makt_rows.append({
        "MANDT": mandt(),
        "MATNR": random.choice(matnr_list),
        "SPRAS": random.choice(_LANGS),
        "MAKTX": maktx,
        "MAKTG": maktx.strip().upper()[:40],
    })
write("MAKT", makt_rows, MAKT_COLS)

# ── SKA1 ──────────────────────────────────────────────────────────────────────
SKA1_COLS = [
    "MANDT","KTOPL","SAKNR","BILKT","ERDAT","ERNAM","GVTYP","KTOKS","MUSTR",
    "VBUND","XBILK","XLOEV","XSPEA","XSPEB","XUMSA",
]
# Account ranges: 1xxxxx=Assets, 2xxxxx=Liabilities, 3-4xxxxx=Revenue/COGS, 5-8xxxxx=Expenses
_GL_RANGES = [
    ("S", "1"), ("S", "2"), ("X", "3"), ("X", "4"),
    ("E", "5"), ("E", "6"), ("E", "7"), ("E", "8"),
]
ska1_rows = []
saknr_list = []
for n in range(400):
    range_info = _GL_RANGES[n % len(_GL_RANGES)]
    saknr = range_info[1] + fake.numerify("#####")
    saknr_list.append(saknr)
    ska1_rows.append({
        "MANDT": "100",
        "KTOPL": "INT",
        "SAKNR": saknr,
        "ERDAT": erdat(),
        "ERNAM": fake.user_name()[:12],
        "GVTYP": range_info[0],
        "KTOKS": fake.bothify("????"),
        "XBILK": random.choice(["X",""]),
    })
write("SKA1", ska1_rows, SKA1_COLS)

# ── SKAT ──────────────────────────────────────────────────────────────────────
SKAT_COLS = ["MANDT","SPRAS","KTOPL","SAKNR","TXT20","TXT50"]
skat_rows = []
for _ in range(500):
    skat_rows.append({
        "MANDT": "100",
        "SPRAS": random.choice(_LANGS),
        "KTOPL": "INT",
        "SAKNR": random.choice(saknr_list),
        "TXT20": fake.bs()[:20],
        "TXT50": ts(fake.catch_phrase()[:50]),
    })
write("SKAT", skat_rows, SKAT_COLS)

# ── CSKS ──────────────────────────────────────────────────────────────────────
CSKS_COLS = [
    "MANDT","KOSTL","DATBI","DATAB","BKLAS","BUKRS","GSBER","KOKRS","KOSTLV",
    "KHINR","KOSAR","VERAK","VERAK2","KTEXT","LTEXT","FUNC_AREA",
]
csks_rows = []
for _ in range(300):
    csks_rows.append({
        "MANDT": "100",
        "KOSTL": fake.numerify("##########"),
        "DATBI": "99991231",
        "DATAB": fake.date_between(start_date="-10y", end_date="-1y").strftime("%Y%m%d"),
        "BUKRS": random.choice(_BUKRS),
        "GSBER": fake.bothify("????"),
        "KOKRS": "1000",
        "KOSAR": random.choice(["A","B","C","D"]),
        "VERAK": fake.user_name()[:12],
        "KTEXT": ts(fake.job()[:20]),
        "LTEXT": fake.bs()[:40],
    })
write("CSKS", csks_rows, CSKS_COLS)

# ── EKKO ──────────────────────────────────────────────────────────────────────
EKKO_COLS = [
    "MANDT","EBELN","BUKRS","BSART","LIFNR","EKORG","EKGRP","WAERS","WKURS",
    "KUFIX","BEDAT","KDATB","KDATE","KDATV","ABGRU","AUTLF","WEAKT","MEMORY",
    "KZABS","RLWRT","ZTERM","ZBD1T","ZBD2T","ZBD3T","ZBD1P","ZBD2P","MWSKZ",
    "IHREZ","VERKF","EXNUM","UNSEZ","INCO1","INCO2","KONNR","KTPNR","ABTYP",
    "WGLIF","KNUMV",
]
ekko_rows = []
ebeln_set = set()

# Take first 5,000 rows from SalesOrders as PO headers
src_orders = orders_df.head(5000)

for _, order in src_orders.iterrows():
    salesorderid = str(order["SALESORDERID"]).strip()
    # Zero-pad to 10 chars
    ebeln = salesorderid.zfill(10)
    ebeln_set.add(ebeln)

    # Map SALESORG → EKORG
    ekorg = _SALESORG_EKORG.get(str(order.get("SALESORG","")), random.choice(_EKORG))

    # DQ#4: orphan FK (~1%): LIFNR not in LFA1
    if random.random() < 0.01:
        lifnr_fk = "9999999999"
    else:
        lifnr_fk = random.choice(lifnr_list)

    bedat = str(order.get("CREATEDAT","")).strip()
    waers = str(order.get("CURRENCY","USD")).strip()

    ekko_rows.append({
        "MANDT": mandt(),
        "EBELN": ebeln,
        "BUKRS": random.choice(_BUKRS),
        "BSART": random.choice(["NB","ZB","UB","FO"]),
        "LIFNR": lifnr_fk,
        "EKORG": ekorg,
        "EKGRP": fake.numerify("###"),
        "WAERS": waers if waers else random.choice(_CURRENCIES),
        "WKURS": str(round(random.uniform(0.5, 2.0), 5)),
        "BEDAT": bedat,
        "KDATE": fake.date_between(start_date="-5y", end_date="today").strftime("%Y%m%d"),
        "AUTLF": random.choice(["X",""]),
        "WEAKT": random.choice(["X",""]),
        "ZTERM": random.choice(_ZTERM),
        "ZBD1T": str(random.randint(0, 30)),
        "ZBD2T": str(random.randint(0, 60)),
        "ZBD3T": str(random.randint(0, 90)),
        "ZBD1P": str(round(random.uniform(0, 3), 1)),
        "ZBD2P": str(round(random.uniform(0, 2), 1)),
        "MWSKZ": random.choice(["V1","V2","V3",""]),
        "INCO1": random.choice(_INCO1),
        "KNUMV": fake.numerify("##########"),
    })

write("EKKO", ekko_rows, EKKO_COLS)

# ── EKPO ──────────────────────────────────────────────────────────────────────
EKPO_COLS = [
    "MANDT","EBELN","EBELP","MATNR","WERKS","LGORT","MATKL","INFNR","IDNLF",
    "KTMNG","MENGE","MEINS","BPRME","BPUMZ","BPUMN","NETPR","PEINH","NETWR",
    "BRTWR","BUGSZ","RETPO","WEPOS","WEUNB","REPOS","MWSKZ","ADRNR","PACKNO",
    "FPLNR","BELNR","LOEKZ","BANFN","BNFPO","EBELN2","EBELP2",
]
ekpo_rows = []

# Filter items to only those whose order ID maps to an EKKO EBELN
# (ensures FK integrity between EKPO and EKKO)
matnr_set = set(matnr_list)

for _, item in items_df.iterrows():
    if len(ekpo_rows) >= 15000:
        break
    salesorderid = str(item["SALESORDERID"]).strip()
    ebeln = salesorderid.zfill(10)
    if ebeln not in ebeln_set:
        continue

    item_no = str(item["SALESORDERITEM"]).strip()
    ebelp = item_no.zfill(5)

    productid = str(item.get("PRODUCTID","")).strip()
    # Use product ID if it's in MARA; otherwise fall back to random MATNR
    matnr = productid if productid in matnr_set else random.choice(matnr_list)

    qty = str(item.get("QUANTITY","")).strip()
    meins = str(item.get("QUANTITYUNIT","EA")).strip() or "EA"
    netwr = str(item.get("NETAMOUNT","")).strip()
    brtwr = str(item.get("GROSSAMOUNT","")).strip()

    # Derive unit price: NETAMOUNT / QUANTITY
    try:
        netpr = str(round(float(netwr) / float(qty), 2)) if float(qty) != 0 else "0.00"
    except (ValueError, ZeroDivisionError):
        netpr = str(round(random.uniform(1, 10000), 2))

    ekpo_rows.append({
        "MANDT": mandt(),
        "EBELN": ebeln,
        "EBELP": ebelp,
        "MATNR": matnr,
        "WERKS": random.choice(_WERKS),
        "LGORT": fake.numerify("####"),
        "MATKL": fake.numerify("######"),
        "MENGE": qty or str(round(random.uniform(1, 1000), 3)),
        "MEINS": meins,
        "BPRME": meins,
        "NETPR": netpr,
        "PEINH": "1",
        "NETWR": netwr or str(round(random.uniform(100, 1000000), 2)),
        "BRTWR": brtwr or str(round(random.uniform(100, 1000000), 2)),
        "WEPOS": random.choice(["X",""]),
        "MWSKZ": random.choice(["V1","V2","V3",""]),
    })

write("EKPO", ekpo_rows, EKPO_COLS)

print(f"\nDone. {len(list(SEED_DIR.glob('*.csv')))} CSVs written to {SEED_DIR}")
