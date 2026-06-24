from faker import Faker
import random
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.ext.asyncio import AsyncEngine
from .base import BaseProfile

metadata = MetaData()

vendors = Table("vendors", metadata,
    Column("id", String(255)),
    Column("name", String(255)),
    Column("address", String(255)),
    Column("city", String(255)),
    Column("state", String(255)),
    Column("zip_code", String(255)),
    Column("country", String(255)),
    Column("phone", String(255)),
    Column("email", String(255)),
    Column("tax_id", String(255)),
    Column("status", String(255)),
    Column("currency", String(255)),
    Column("payment_terms", String(255)),
    Column("created_at", String(255)),
    Column("updated_at", String(255)),
)

customers = Table("customers", metadata,
    Column("id", String(255)),
    Column("name", String(255)),
    Column("address", String(255)),
    Column("city", String(255)),
    Column("state", String(255)),
    Column("zip_code", String(255)),
    Column("country", String(255)),
    Column("phone", String(255)),
    Column("email", String(255)),
    Column("tax_id", String(255)),
    Column("status", String(255)),
    Column("credit_limit", String(255)),
    Column("currency", String(255)),
    Column("created_at", String(255)),
    Column("updated_at", String(255)),
)

materials = Table("materials", metadata,
    Column("id", String(255)),
    Column("code", String(255)),
    Column("description", String(255)),
    Column("unit_of_measure", String(255)),
    Column("weight", String(255)),
    Column("category", String(255)),
    Column("subcategory", String(255)),
    Column("status", String(255)),
    Column("list_price", String(255)),
    Column("currency", String(255)),
    Column("created_at", String(255)),
    Column("updated_at", String(255)),
)

purchase_orders = Table("purchase_orders", metadata,
    Column("id", String(255)),
    Column("po_number", String(255)),
    Column("vendor_id", String(255)),
    Column("status", String(255)),
    Column("currency", String(255)),
    Column("total_amount", String(255)),
    Column("order_date", String(255)),
    Column("delivery_date", String(255)),
    Column("created_at", String(255)),
    Column("updated_at", String(255)),
)

_VALID_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD"]
_VALID_COUNTRIES = ["US", "GB", "DE", "FR", "JP", "CA", "AU"]
_INVALID_COUNTRIES = ["XX", "ZZ"]
_UNICODE_NAMES = ["Müller GmbH", "Société Générale", "日本電気株式会社", "شركة أرامكو السعودية"]


class GenericProfile(BaseProfile):
    @property
    def profile_id(self) -> str:
        return "generic"

    @property
    def system_name(self) -> str:
        return "GENERIC-1"

    @property
    def system_type(self) -> str:
        return "Generic Legacy ERP"

    @property
    def version(self) -> str:
        return "3.4.1"

    @property
    def description(self) -> str:
        return "Generic legacy ERP system — simplified flat schema"

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

        def iso_dt():
            d = fake.date_time_between(start_date="-10y", end_date="now")
            if random.random() < 0.5:
                return d.strftime("%Y-%m-%dT%H:%M:%SZ")
            return d.strftime("%Y-%m-%d %H:%M:%S")

        def country():
            if random.random() < 0.03:
                return random.choice(_INVALID_COUNTRIES)
            return random.choice(_VALID_COUNTRIES)

        # vendors
        vendor_ids = []
        rows = []
        for i in range(1, 1001):
            vid = str(i)
            vendor_ids.append(vid)

            if random.random() < 0.03:
                name = random.choice(_UNICODE_NAMES)
            else:
                name = fake.company()
            name = ts(name)

            # DQ #8 blocked: 5%
            status = "inactive" if random.random() < 0.05 else "active"

            row = {
                "id": vid,
                "name": name,
                "address": ts(fake.street_address()),
                "city": ts(fake.city()),
                "state": null_val() if random.random() < 0.2 else fake.state_abbr(),
                "zip_code": fake.postcode(),
                "country": country(),
                "phone": null_val() if random.random() < 0.1 else ts(fake.phone_number()),
                "email": null_val() if random.random() < 0.1 else fake.company_email(),
                "tax_id": null_val() if random.random() < 0.2 else fake.bothify("??-#######"),
                "status": status,
                "currency": random.choice(_VALID_CURRENCIES),
                "payment_terms": random.choice(["net30", "net60", "net90", "immediate"]),
                "created_at": iso_dt(),
                "updated_at": iso_dt(),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(vendors.insert(), rows[i:i+500])

        # customers
        rows = []
        for i in range(1, 501):
            if random.random() < 0.03:
                name = random.choice(_UNICODE_NAMES)
            else:
                name = fake.company()
            name = ts(name)

            row = {
                "id": str(i),
                "name": name,
                "address": ts(fake.street_address()),
                "city": ts(fake.city()),
                "state": null_val() if random.random() < 0.2 else fake.state_abbr(),
                "zip_code": fake.postcode(),
                "country": country(),
                "phone": null_val() if random.random() < 0.1 else ts(fake.phone_number()),
                "email": null_val() if random.random() < 0.1 else fake.company_email(),
                "tax_id": null_val() if random.random() < 0.2 else fake.bothify("??-#######"),
                "status": "inactive" if random.random() < 0.05 else "active",
                "credit_limit": null_val() if random.random() < 0.3 else str(random.randint(5000, 500000)),
                "currency": random.choice(_VALID_CURRENCIES),
                "created_at": iso_dt(),
                "updated_at": iso_dt(),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(customers.insert(), rows[i:i+500])

        # materials
        categories = ["Electronics", "Chemicals", "Raw Materials", "Packaging", "MRO", "Services"]
        uoms = ["EA", "KG", "LB", "M", "L", "CS", "BX"]
        rows = []
        for i in range(1, 1001):
            cat = random.choice(categories)
            row = {
                "id": str(i),
                "code": f"MAT{i:07d}",
                "description": ts(fake.catch_phrase()),
                "unit_of_measure": random.choice(uoms),
                "weight": null_val() if random.random() < 0.2 else str(round(random.uniform(0.01, 500.0), 3)),
                "category": cat,
                "subcategory": null_val() if random.random() < 0.3 else fake.word().capitalize(),
                "status": "discontinued" if random.random() < 0.05 else "active",
                "list_price": null_val() if random.random() < 0.1 else str(round(random.uniform(0.5, 9999.99), 2)),
                "currency": random.choice(_VALID_CURRENCIES),
                "created_at": iso_dt(),
                "updated_at": iso_dt(),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(materials.insert(), rows[i:i+500])

        # purchase_orders
        statuses = ["open", "approved", "received", "closed", "cancelled"]
        rows = []
        for i in range(1, 2001):
            # DQ #4 orphan FK: 1%
            if random.random() < 0.01:
                vendor_id = "99999"
            else:
                vendor_id = random.choice(vendor_ids)

            order_date = fake.date_between(start_date="-3y", end_date="today")
            row = {
                "id": str(i),
                "po_number": f"PO-{i:08d}",
                "vendor_id": vendor_id,
                "status": random.choice(statuses),
                "currency": random.choice(_VALID_CURRENCIES),
                "total_amount": str(round(random.uniform(100.0, 999999.99), 2)),
                "order_date": order_date.strftime("%Y-%m-%d"),
                "delivery_date": null_val() if random.random() < 0.1 else fake.date_between(start_date=order_date, end_date="+6m").strftime("%Y-%m-%d"),
                "created_at": iso_dt(),
                "updated_at": iso_dt(),
            }
            rows.append(row)

        async with engine.begin() as conn:
            for i in range(0, len(rows), 500):
                await conn.execute(purchase_orders.insert(), rows[i:i+500])

    def get_tables(self) -> list[dict]:
        return [
            {"name": "vendors", "domain": "Vendors", "record_count": 1000, "primary_keys": ["id"]},
            {"name": "customers", "domain": "Customers", "record_count": 500, "primary_keys": ["id"]},
            {"name": "materials", "domain": "Materials", "record_count": 1000, "primary_keys": ["id"]},
            {"name": "purchase_orders", "domain": "Purchasing", "record_count": 2000, "primary_keys": ["id"]},
        ]

    def get_schema(self, table_name: str) -> dict:
        _descriptions = {
            "id": "Primary key",
            "name": "Name",
            "address": "Street address",
            "city": "City",
            "state": "State or province",
            "zip_code": "Postal / ZIP code",
            "country": "Country code",
            "phone": "Phone number",
            "email": "Email address",
            "tax_id": "Tax identifier",
            "status": "Record status",
            "currency": "Currency code",
            "payment_terms": "Payment terms",
            "created_at": "Creation timestamp",
            "updated_at": "Last update timestamp",
            "vendor_id": "Reference to vendors.id",
            "po_number": "Purchase order number",
            "total_amount": "Total order amount",
            "order_date": "Date order was placed",
            "delivery_date": "Expected delivery date",
        }
        tbl_map = {
            "vendors": vendors,
            "customers": customers,
            "materials": materials,
            "purchase_orders": purchase_orders,
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
            "purchase_orders": [
                {"from_table": "purchase_orders", "from_column": "vendor_id", "to_table": "vendors", "to_column": "id"},
            ],
        }
        return _rels.get(table_name, [])
