import uuid
from faker import Faker
import random
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.ext.asyncio import AsyncEngine
from .base import BaseProfile

metadata = MetaData()

vend_table = Table("VendTable", metadata,
    Column("RecId", String(255)),
    Column("AccountNum", String(255)),
    Column("VendGroup", String(255)),
    Column("Name", String(255)),
    Column("CurrencyCode", String(255)),
    Column("PaymTermId", String(255)),
    Column("DataAreaId", String(255)),
    Column("Blocked", String(255)),
    Column("PrimaryContactPhone", String(255)),
    Column("PrimaryContactEmail", String(255)),
    Column("Address", String(255)),
    Column("City", String(255)),
    Column("State", String(255)),
    Column("ZipCode", String(255)),
    Column("CountryRegionId", String(255)),
    Column("TaxGroup", String(255)),
    Column("VATNum", String(255)),
    Column("CreatedDateTime", String(255)),
    Column("ModifiedDateTime", String(255)),
)

cust_table = Table("CustTable", metadata,
    Column("RecId", String(255)),
    Column("AccountNum", String(255)),
    Column("CustGroup", String(255)),
    Column("Name", String(255)),
    Column("CurrencyCode", String(255)),
    Column("PaymTermId", String(255)),
    Column("DataAreaId", String(255)),
    Column("Blocked", String(255)),
    Column("Phone", String(255)),
    Column("Email", String(255)),
    Column("Address", String(255)),
    Column("City", String(255)),
    Column("State", String(255)),
    Column("ZipCode", String(255)),
    Column("CountryRegionId", String(255)),
    Column("TaxGroup", String(255)),
    Column("CreatedDateTime", String(255)),
    Column("ModifiedDateTime", String(255)),
)

invent_table = Table("InventTable", metadata,
    Column("RecId", String(255)),
    Column("ItemId", String(255)),
    Column("ItemName", String(255)),
    Column("ItemGroupId", String(255)),
    Column("UnitId", String(255)),
    Column("PurchPrice", String(255)),
    Column("SalesPrice", String(255)),
    Column("NetWeight", String(255)),
    Column("GrossWeight", String(255)),
    Column("DataAreaId", String(255)),
    Column("Blocked", String(255)),
    Column("CreatedDateTime", String(255)),
    Column("ModifiedDateTime", String(255)),
)

purch_table = Table("PurchTable", metadata,
    Column("RecId", String(255)),
    Column("PurchId", String(255)),
    Column("PurchStatus", String(255)),
    Column("VendAccount", String(255)),
    Column("DeliveryName", String(255)),
    Column("DeliveryDate", String(255)),
    Column("CurrencyCode", String(255)),
    Column("InvoiceAccount", String(255)),
    Column("DataAreaId", String(255)),
    Column("CreatedDateTime", String(255)),
    Column("ModifiedDateTime", String(255)),
)

ledger_table = Table("LedgerTable", metadata,
    Column("RecId", String(255)),
    Column("LedgerDimension", String(255)),
    Column("AccountType", String(255)),
    Column("Name", String(255)),
    Column("Active", String(255)),
    Column("DataAreaId", String(255)),
    Column("CreatedDateTime", String(255)),
    Column("ModifiedDateTime", String(255)),
)

_VALID_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD"]
_VALID_COUNTRIES = ["US", "GB", "DE", "FR", "JP", "CA", "AU", "NL", "SE", "CH"]
_INVALID_COUNTRIES = ["XX", "ZZ", "99"]
_UNICODE_NAMES = ["Müller GmbH", "Société Générale", "日本電気株式会社", "شركة أرامكو السعودية"]
_DATA_AREAS = ["DAT", "USMF", "GBSI", "DEMF"]


class DynamicsAxProfile(BaseProfile):
    @property
    def profile_id(self) -> str:
        return "dynamics_ax"

    @property
    def system_name(self) -> str:
        return "DYNAMICS-AX-1"

    @property
    def system_type(self) -> str:
        return "Microsoft Dynamics AX"

    @property
    def version(self) -> str:
        return "2012 R3"

    @property
    def description(self) -> str:
        return "Microsoft Dynamics AX 2012 R3 — Finance and Operations"

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

        def dt():
            d = fake.date_time_between(start_date="-10y", end_date="now")
            if random.random() < 0.5:
                return d.strftime("%Y-%m-%dT%H:%M:%S")
            return d.strftime("%d/%m/%Y %H:%M")

        def country():
            if random.random() < 0.03:
                return random.choice(_INVALID_COUNTRIES)
            return random.choice(_VALID_COUNTRIES)

        # VendTable
        vend_accounts = []
        rows = []
        for i in range(1, 1501):
            acct = f"V{i:06d}"
            vend_accounts.append(acct)

            if random.random() < 0.03:
                name = random.choice(_UNICODE_NAMES)
            else:
                name = fake.company()
            name = ts(name)

            blocked = "Yes" if random.random() < 0.05 else ""

            row = {
                "RecId": str(uuid.uuid4()),
                "AccountNum": acct,
                "VendGroup": random.choice(["DOM", "FOR", "IC", "MISC"]),
                "Name": name,
                "CurrencyCode": random.choice(_VALID_CURRENCIES),
                "PaymTermId": random.choice(["Net30", "Net60", "Net90", "2/10Net30"]),
                "DataAreaId": random.choice(_DATA_AREAS),
                "Blocked": blocked,
                "PrimaryContactPhone": null_val() if random.random() < 0.2 else ts(fake.phone_number()),
                "PrimaryContactEmail": null_val() if random.random() < 0.2 else fake.company_email(),
                "Address": ts(fake.street_address()),
                "City": ts(fake.city()),
                "State": null_val() if random.random() < 0.3 else fake.state_abbr(),
                "ZipCode": fake.postcode(),
                "CountryRegionId": country(),
                "TaxGroup": random.choice(["DOMESTIC", "FOREIGN", "EXEMPT"]),
                "VATNum": null_val() if random.random() < 0.3 else fake.bothify("??##########"),
                "CreatedDateTime": dt(),
                "ModifiedDateTime": dt(),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(vend_table.insert(), rows[i:i+500])

        # CustTable
        rows = []
        for i in range(1, 1001):
            if random.random() < 0.03:
                name = random.choice(_UNICODE_NAMES)
            else:
                name = fake.company()
            name = ts(name)

            row = {
                "RecId": str(uuid.uuid4()),
                "AccountNum": f"C{i:06d}",
                "CustGroup": random.choice(["DOM", "FOR", "IC", "RETAIL"]),
                "Name": name,
                "CurrencyCode": random.choice(_VALID_CURRENCIES),
                "PaymTermId": random.choice(["Net30", "Net60", "Net90"]),
                "DataAreaId": random.choice(_DATA_AREAS),
                "Blocked": "Yes" if random.random() < 0.03 else "",
                "Phone": null_val() if random.random() < 0.2 else ts(fake.phone_number()),
                "Email": null_val() if random.random() < 0.2 else fake.company_email(),
                "Address": ts(fake.street_address()),
                "City": ts(fake.city()),
                "State": null_val() if random.random() < 0.3 else fake.state_abbr(),
                "ZipCode": fake.postcode(),
                "CountryRegionId": country(),
                "TaxGroup": random.choice(["DOMESTIC", "FOREIGN", "EXEMPT"]),
                "CreatedDateTime": dt(),
                "ModifiedDateTime": dt(),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(cust_table.insert(), rows[i:i+500])

        # InventTable
        rows = []
        for i in range(1, 2001):
            row = {
                "RecId": str(uuid.uuid4()),
                "ItemId": f"ITEM{i:06d}",
                "ItemName": ts(fake.catch_phrase()),
                "ItemGroupId": random.choice(["RAW", "WIP", "FIN", "MRO", "SERVICE"]),
                "UnitId": random.choice(["EA", "KG", "LB", "M", "L", "CS"]),
                "PurchPrice": null_val() if random.random() < 0.1 else str(round(random.uniform(0.5, 9999.99), 2)),
                "SalesPrice": null_val() if random.random() < 0.1 else str(round(random.uniform(1.0, 14999.99), 2)),
                "NetWeight": null_val() if random.random() < 0.3 else str(round(random.uniform(0.01, 500.0), 3)),
                "GrossWeight": null_val() if random.random() < 0.3 else str(round(random.uniform(0.01, 550.0), 3)),
                "DataAreaId": random.choice(_DATA_AREAS),
                "Blocked": "Yes" if random.random() < 0.02 else "",
                "CreatedDateTime": dt(),
                "ModifiedDateTime": dt(),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(invent_table.insert(), rows[i:i+500])

        # PurchTable
        rows = []
        for i in range(1, 2001):
            # DQ #4 orphan FK: 1%
            if random.random() < 0.01:
                vend_acct = "V999999"
            else:
                vend_acct = random.choice(vend_accounts)

            row = {
                "RecId": str(uuid.uuid4()),
                "PurchId": f"PO-{i:08d}",
                "PurchStatus": random.choice(["Open order", "Received", "Invoiced", "Canceled"]),
                "VendAccount": vend_acct,
                "DeliveryName": ts(fake.company()),
                "DeliveryDate": fake.date_between(start_date="-2y", end_date="+6m").strftime("%Y-%m-%d"),
                "CurrencyCode": random.choice(_VALID_CURRENCIES),
                "InvoiceAccount": vend_acct,
                "DataAreaId": random.choice(_DATA_AREAS),
                "CreatedDateTime": dt(),
                "ModifiedDateTime": dt(),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(purch_table.insert(), rows[i:i+500])

        # LedgerTable
        acct_types = ["Balance sheet", "Profit and loss", "Reporting", "Total", "Header"]
        rows = []
        for i in range(1, 301):
            row = {
                "RecId": str(uuid.uuid4()),
                "LedgerDimension": f"{random.randint(1000,9999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
                "AccountType": random.choice(acct_types),
                "Name": ts(fake.catch_phrase()),
                "Active": random.choice(["Yes", "No"]),
                "DataAreaId": random.choice(_DATA_AREAS),
                "CreatedDateTime": dt(),
                "ModifiedDateTime": dt(),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(ledger_table.insert(), rows[i:i+500])

    def get_tables(self) -> list[dict]:
        return [
            {"name": "VendTable", "domain": "Vendors", "record_count": 1500, "primary_keys": ["RecId"]},
            {"name": "CustTable", "domain": "Customers", "record_count": 1000, "primary_keys": ["RecId"]},
            {"name": "InventTable", "domain": "Inventory", "record_count": 2000, "primary_keys": ["RecId"]},
            {"name": "PurchTable", "domain": "Purchasing", "record_count": 2000, "primary_keys": ["RecId"]},
            {"name": "LedgerTable", "domain": "Ledger", "record_count": 300, "primary_keys": ["RecId"]},
        ]

    def get_schema(self, table_name: str) -> dict:
        _descriptions = {
            "RecId": "Unique record identifier (UUID)",
            "AccountNum": "Account number",
            "VendGroup": "Vendor group code",
            "Name": "Name",
            "CurrencyCode": "Currency code",
            "DataAreaId": "Data area (company) identifier",
            "Blocked": "Blocking status",
            "CreatedDateTime": "Record creation timestamp",
            "ModifiedDateTime": "Last modification timestamp",
        }
        tbl_map = {
            "VendTable": vend_table,
            "CustTable": cust_table,
            "InventTable": invent_table,
            "PurchTable": purch_table,
            "LedgerTable": ledger_table,
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
            "PurchTable": [
                {"from_table": "PurchTable", "from_column": "VendAccount", "to_table": "VendTable", "to_column": "AccountNum"},
            ],
        }
        return _rels.get(table_name, [])
