from faker import Faker
import random
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.ext.asyncio import AsyncEngine
from .base import BaseProfile

metadata = MetaData()

ap_suppliers = Table("AP_SUPPLIERS", metadata,
    Column("VENDOR_ID", String(255)),
    Column("VENDOR_NAME", String(255)),
    Column("VENDOR_TYPE_LOOKUP_CODE", String(255)),
    Column("ENABLED_FLAG", String(255)),
    Column("VENDOR_NAME_ALT", String(255)),
    Column("SEGMENT1", String(255)),
    Column("SUMMARY_FLAG", String(255)),
    Column("SET_OF_BOOKS_ID", String(255)),
    Column("EMPLOYEE_ID", String(255)),
    Column("PAY_GROUP_LOOKUP_CODE", String(255)),
    Column("PAYMENT_PRIORITY", String(255)),
    Column("TERMS_ID", String(255)),
    Column("INVOICE_CURRENCY_CODE", String(255)),
    Column("PAYMENT_CURRENCY_CODE", String(255)),
    Column("AMOUNT_LIMIT", String(255)),
    Column("NUM_1099", String(255)),
    Column("TYPE_1099", String(255)),
    Column("VAT_REGISTRATION_NUM", String(255)),
    Column("CHECK_DIGITS", String(255)),
    Column("BANK_CHARGE_BEARER", String(255)),
    Column("MATCH_OPTION", String(255)),
    Column("VENDOR_COUNT", String(255)),
    Column("CREATION_DATE", String(255)),
    Column("CREATED_BY", String(255)),
    Column("LAST_UPDATE_DATE", String(255)),
    Column("LAST_UPDATED_BY", String(255)),
    Column("ORG_ID", String(255)),
)

ar_customers = Table("AR_CUSTOMERS", metadata,
    Column("CUSTOMER_ID", String(255)),
    Column("CUSTOMER_NAME", String(255)),
    Column("CUSTOMER_NUMBER", String(255)),
    Column("CUSTOMER_TYPE", String(255)),
    Column("ACCOUNT_NUMBER", String(255)),
    Column("STATUS", String(255)),
    Column("CREATION_DATE", String(255)),
    Column("CREATED_BY", String(255)),
    Column("LAST_UPDATE_DATE", String(255)),
    Column("LAST_UPDATED_BY", String(255)),
    Column("ORG_ID", String(255)),
    Column("TAX_REFERENCE", String(255)),
    Column("URL", String(255)),
    Column("EMAIL_ADDRESS", String(255)),
    Column("PHONE", String(255)),
    Column("CITY", String(255)),
    Column("STATE", String(255)),
    Column("POSTAL_CODE", String(255)),
    Column("COUNTRY", String(255)),
)

mtl_system_items_b = Table("MTL_SYSTEM_ITEMS_B", metadata,
    Column("INVENTORY_ITEM_ID", String(255)),
    Column("ORGANIZATION_ID", String(255)),
    Column("SEGMENT1", String(255)),
    Column("DESCRIPTION", String(255)),
    Column("ITEM_TYPE", String(255)),
    Column("PRIMARY_UOM_CODE", String(255)),
    Column("ENABLED_FLAG", String(255)),
    Column("INVENTORY_ITEM_FLAG", String(255)),
    Column("PURCHASABLE_FLAG", String(255)),
    Column("CREATION_DATE", String(255)),
    Column("CREATED_BY", String(255)),
    Column("LAST_UPDATE_DATE", String(255)),
    Column("LAST_UPDATED_BY", String(255)),
)

po_headers_all = Table("PO_HEADERS_ALL", metadata,
    Column("PO_HEADER_ID", String(255)),
    Column("SEGMENT1", String(255)),
    Column("TYPE_LOOKUP_CODE", String(255)),
    Column("STATUS_LOOKUP_CODE", String(255)),
    Column("VENDOR_ID", String(255)),
    Column("ORG_ID", String(255)),
    Column("CURRENCY_CODE", String(255)),
    Column("RATE_TYPE", String(255)),
    Column("RATE", String(255)),
    Column("SHIP_TO_LOCATION_ID", String(255)),
    Column("BILL_TO_LOCATION_ID", String(255)),
    Column("TERMS_ID", String(255)),
    Column("CREATION_DATE", String(255)),
    Column("CREATED_BY", String(255)),
    Column("LAST_UPDATE_DATE", String(255)),
    Column("LAST_UPDATED_BY", String(255)),
    Column("AUTHORIZATION_STATUS", String(255)),
    Column("NOTE_TO_VENDOR", String(255)),
    Column("CLOSED_CODE", String(255)),
)

gl_code_combinations = Table("GL_CODE_COMBINATIONS", metadata,
    Column("CODE_COMBINATION_ID", String(255)),
    Column("CHART_OF_ACCOUNTS_ID", String(255)),
    Column("SEGMENT1", String(255)),
    Column("SEGMENT2", String(255)),
    Column("SEGMENT3", String(255)),
    Column("ENABLED_FLAG", String(255)),
    Column("SUMMARY_FLAG", String(255)),
    Column("START_DATE_ACTIVE", String(255)),
    Column("END_DATE_ACTIVE", String(255)),
    Column("CREATION_DATE", String(255)),
    Column("CREATED_BY", String(255)),
    Column("LAST_UPDATE_DATE", String(255)),
    Column("LAST_UPDATED_BY", String(255)),
)

_VALID_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "SEK"]
_INVALID_CURRENCIES = ["XXX", "ZZZ", "999"]
_UNICODE_NAMES = ["Müller GmbH", "Société Générale", "日本電気株式会社", "شركة أرامكو السعودية"]


class OracleEbsProfile(BaseProfile):
    @property
    def profile_id(self) -> str:
        return "oracle_ebs"

    @property
    def system_name(self) -> str:
        return "ORACLE-EBS-1"

    @property
    def system_type(self) -> str:
        return "Oracle E-Business Suite"

    @property
    def version(self) -> str:
        return "12.2.10"

    @property
    def description(self) -> str:
        return "Oracle E-Business Suite 12.2.10 — AP/AR/GL modules"

    async def create_tables(self, engine: AsyncEngine) -> None:
        async with engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

    async def drop_tables(self, engine: AsyncEngine) -> None:
        async with engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)

    async def seed_data(self, engine: AsyncEngine) -> None:
        fake = Faker(["en_US", "en_GB", "de_DE", "fr_FR", "ja_JP", "pt_BR"])
        Faker.seed(42)
        random.seed(42)

        def ts(val):
            if val and random.random() < 0.20:
                return val + "   "
            return val

        def null_val():
            return random.choice([None, "", "N/A"])

        def erdate():
            d = fake.date_between(start_date="-10y", end_date="today")
            if random.random() < 0.5:
                return d.strftime("%Y-%m-%d %H:%M:%S")
            return d.strftime("%d-%b-%Y")

        # AP_SUPPLIERS
        n_suppliers = 1500
        supplier_ids = []
        near_dupe_names = {}
        rows = []
        for i in range(1, n_suppliers + 1):
            sid = str(i)
            supplier_ids.append(sid)

            # DQ #7 unicode
            if random.random() < 0.03:
                name = random.choice(_UNICODE_NAMES)
            else:
                name = fake.company()

            # DQ #3 near-dupes: 2%
            if random.random() < 0.02 and near_dupe_names:
                name = random.choice(list(near_dupe_names.keys()))
            else:
                near_dupe_names[name] = sid

            # DQ #1 trailing spaces
            name = ts(name)

            # DQ #8 blocked: 5%
            enabled = "N" if random.random() < 0.05 else "Y"

            # DQ #5 invalid currency code: 3%
            if random.random() < 0.03:
                inv_curr = random.choice(_INVALID_CURRENCIES)
            else:
                inv_curr = random.choice(_VALID_CURRENCIES)

            # DQ #2 inconsistent nulls: 30%
            vendor_name_alt = null_val() if random.random() < 0.30 else fake.company()
            employee_id = null_val() if random.random() < 0.30 else str(random.randint(10000, 99999))

            row = {
                "VENDOR_ID": sid,
                "VENDOR_NAME": name,
                "VENDOR_TYPE_LOOKUP_CODE": random.choice(["STANDARD", "EMPLOYEE", "FOREIGN"]),
                "ENABLED_FLAG": enabled,
                "VENDOR_NAME_ALT": vendor_name_alt,
                "SEGMENT1": ts(f"V{i:06d}"),
                "SUMMARY_FLAG": "N",
                "SET_OF_BOOKS_ID": "1",
                "EMPLOYEE_ID": employee_id,
                "PAY_GROUP_LOOKUP_CODE": random.choice(["STANDARD", "EMPLOYEE"]),
                "PAYMENT_PRIORITY": str(random.randint(1, 99)),
                "TERMS_ID": str(random.randint(1, 20)),
                "INVOICE_CURRENCY_CODE": inv_curr,
                "PAYMENT_CURRENCY_CODE": random.choice(_VALID_CURRENCIES),
                "AMOUNT_LIMIT": null_val() if random.random() < 0.4 else str(random.randint(10000, 1000000)),
                "NUM_1099": null_val() if random.random() < 0.5 else fake.ssn(),
                "TYPE_1099": null_val() if random.random() < 0.5 else random.choice(["MISC", "NEC"]),
                "VAT_REGISTRATION_NUM": null_val() if random.random() < 0.3 else fake.bothify("??##########"),
                "CHECK_DIGITS": null_val() if random.random() < 0.5 else str(random.randint(10, 99)),
                "BANK_CHARGE_BEARER": random.choice(["I", "S", "B"]),
                "MATCH_OPTION": random.choice(["P", "R"]),
                "VENDOR_COUNT": str(random.randint(1, 500)),
                "CREATION_DATE": erdate(),
                "CREATED_BY": str(random.randint(1, 100)),
                "LAST_UPDATE_DATE": erdate(),
                "LAST_UPDATED_BY": str(random.randint(1, 100)),
                "ORG_ID": random.choice(["101", "102", "201"]),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(ap_suppliers.insert(), rows[i:i+500])

        # AR_CUSTOMERS
        rows = []
        for i in range(1, 1001):
            if random.random() < 0.03:
                name = random.choice(_UNICODE_NAMES)
            else:
                name = fake.company()
            name = ts(name)
            row = {
                "CUSTOMER_ID": str(i),
                "CUSTOMER_NAME": name,
                "CUSTOMER_NUMBER": f"C{i:07d}",
                "CUSTOMER_TYPE": random.choice(["ORGANIZATION", "PERSON"]),
                "ACCOUNT_NUMBER": fake.bothify("ACC-#######"),
                "STATUS": "A" if random.random() > 0.05 else "I",
                "CREATION_DATE": erdate(),
                "CREATED_BY": str(random.randint(1, 100)),
                "LAST_UPDATE_DATE": erdate(),
                "LAST_UPDATED_BY": str(random.randint(1, 100)),
                "ORG_ID": random.choice(["101", "102", "201"]),
                "TAX_REFERENCE": null_val() if random.random() < 0.3 else fake.bothify("TAX-########"),
                "URL": null_val() if random.random() < 0.4 else fake.url(),
                "EMAIL_ADDRESS": null_val() if random.random() < 0.2 else fake.company_email(),
                "PHONE": ts(fake.phone_number()),
                "CITY": ts(fake.city()),
                "STATE": fake.state_abbr() if hasattr(fake, "state_abbr") else fake.state(),
                "POSTAL_CODE": fake.postcode(),
                "COUNTRY": random.choice(["US", "GB", "DE", "FR", "JP", "CA", "XX" if random.random() < 0.03 else "AU"]),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(ar_customers.insert(), rows[i:i+500])

        # MTL_SYSTEM_ITEMS_B
        item_types = ["PURCHASED", "MANUFACTURED", "PHANTOM", "KIT", "STANDARD"]
        uom_codes = ["EA", "KG", "LB", "M", "L", "CS", "BX"]
        org_ids = ["101", "102", "201", "301"]
        rows = []
        for i in range(1, 2001):
            row = {
                "INVENTORY_ITEM_ID": str(i),
                "ORGANIZATION_ID": random.choice(org_ids),
                "SEGMENT1": f"ITEM{i:06d}",
                "DESCRIPTION": ts(fake.catch_phrase()),
                "ITEM_TYPE": random.choice(item_types),
                "PRIMARY_UOM_CODE": random.choice(uom_codes),
                "ENABLED_FLAG": "N" if random.random() < 0.03 else "Y",
                "INVENTORY_ITEM_FLAG": random.choice(["Y", "N"]),
                "PURCHASABLE_FLAG": random.choice(["Y", "N"]),
                "CREATION_DATE": erdate(),
                "CREATED_BY": str(random.randint(1, 100)),
                "LAST_UPDATE_DATE": erdate(),
                "LAST_UPDATED_BY": str(random.randint(1, 100)),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(mtl_system_items_b.insert(), rows[i:i+500])

        # PO_HEADERS_ALL
        rows = []
        for i in range(1, 2001):
            # DQ #4 orphan FK: 1%
            if random.random() < 0.01:
                vendor_id = "9999999"
            else:
                vendor_id = str(random.randint(1, n_suppliers))

            row = {
                "PO_HEADER_ID": str(i),
                "SEGMENT1": f"PO{i:08d}",
                "TYPE_LOOKUP_CODE": random.choice(["STANDARD", "BLANKET", "PLANNED"]),
                "STATUS_LOOKUP_CODE": random.choice(["APPROVED", "IN PROCESS", "INCOMPLETE"]),
                "VENDOR_ID": vendor_id,
                "ORG_ID": random.choice(["101", "102", "201"]),
                "CURRENCY_CODE": random.choice(_VALID_CURRENCIES),
                "RATE_TYPE": random.choice(["Corporate", "Spot", "User"]),
                "RATE": null_val() if random.random() < 0.3 else str(round(random.uniform(0.8, 1.5), 4)),
                "SHIP_TO_LOCATION_ID": str(random.randint(1, 50)),
                "BILL_TO_LOCATION_ID": str(random.randint(1, 50)),
                "TERMS_ID": str(random.randint(1, 20)),
                "CREATION_DATE": erdate(),
                "CREATED_BY": str(random.randint(1, 100)),
                "LAST_UPDATE_DATE": erdate(),
                "LAST_UPDATED_BY": str(random.randint(1, 100)),
                "AUTHORIZATION_STATUS": random.choice(["APPROVED", "REQUIRES REAPPROVAL", "IN PROCESS"]),
                "NOTE_TO_VENDOR": null_val() if random.random() < 0.6 else ts(fake.sentence()),
                "CLOSED_CODE": random.choice(["OPEN", "CLOSED", "FINALLY CLOSED"]),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(po_headers_all.insert(), rows[i:i+500])

        # GL_CODE_COMBINATIONS
        rows = []
        for i in range(1, 301):
            row = {
                "CODE_COMBINATION_ID": str(i),
                "CHART_OF_ACCOUNTS_ID": "1",
                "SEGMENT1": f"{random.randint(1000,9999)}",
                "SEGMENT2": f"{random.randint(100,999)}",
                "SEGMENT3": f"{random.randint(1000,9999)}",
                "ENABLED_FLAG": "N" if random.random() < 0.03 else "Y",
                "SUMMARY_FLAG": "N",
                "START_DATE_ACTIVE": fake.date_between(start_date="-15y", end_date="-1y").strftime("%Y-%m-%d"),
                "END_DATE_ACTIVE": null_val() if random.random() < 0.7 else fake.date_between(start_date="today", end_date="+5y").strftime("%Y-%m-%d"),
                "CREATION_DATE": erdate(),
                "CREATED_BY": str(random.randint(1, 100)),
                "LAST_UPDATE_DATE": erdate(),
                "LAST_UPDATED_BY": str(random.randint(1, 100)),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(gl_code_combinations.insert(), rows[i:i+500])

    def get_tables(self) -> list[dict]:
        return [
            {"name": "AP_SUPPLIERS", "domain": "Accounts Payable", "record_count": 1500, "primary_keys": ["VENDOR_ID"]},
            {"name": "AR_CUSTOMERS", "domain": "Accounts Receivable", "record_count": 1000, "primary_keys": ["CUSTOMER_ID"]},
            {"name": "MTL_SYSTEM_ITEMS_B", "domain": "Inventory", "record_count": 2000, "primary_keys": ["INVENTORY_ITEM_ID", "ORGANIZATION_ID"]},
            {"name": "PO_HEADERS_ALL", "domain": "Purchasing", "record_count": 2000, "primary_keys": ["PO_HEADER_ID"]},
            {"name": "GL_CODE_COMBINATIONS", "domain": "General Ledger", "record_count": 300, "primary_keys": ["CODE_COMBINATION_ID"]},
        ]

    def get_schema(self, table_name: str) -> dict:
        _descriptions = {
            "VENDOR_ID": "Vendor unique identifier",
            "VENDOR_NAME": "Vendor name",
            "ENABLED_FLAG": "Y=enabled, N=disabled",
            "CREATION_DATE": "Record creation date",
            "ORG_ID": "Operating unit identifier",
            "CUSTOMER_ID": "Customer unique identifier",
            "CUSTOMER_NAME": "Customer name",
            "INVENTORY_ITEM_ID": "Inventory item identifier",
            "ORGANIZATION_ID": "Organization identifier",
            "PO_HEADER_ID": "Purchase order header identifier",
            "CODE_COMBINATION_ID": "Account code combination identifier",
        }
        tbl_map = {
            "AP_SUPPLIERS": ap_suppliers,
            "AR_CUSTOMERS": ar_customers,
            "MTL_SYSTEM_ITEMS_B": mtl_system_items_b,
            "PO_HEADERS_ALL": po_headers_all,
            "GL_CODE_COMBINATIONS": gl_code_combinations,
        }
        tbl = tbl_map.get(table_name)
        if tbl is None:
            return {"table_name": table_name, "columns": []}
        columns = []
        for col in tbl.columns:
            columns.append({
                "name": col.name,
                "type": "String(255)",
                "nullable": True,
                "description": _descriptions.get(col.name, col.name),
                "sample_values": [],
            })
        return {"table_name": table_name, "columns": columns}

    def get_relationships(self, table_name: str) -> list[dict]:
        _rels = {
            "PO_HEADERS_ALL": [
                {"from_table": "PO_HEADERS_ALL", "from_column": "VENDOR_ID", "to_table": "AP_SUPPLIERS", "to_column": "VENDOR_ID"},
            ],
        }
        return _rels.get(table_name, [])
