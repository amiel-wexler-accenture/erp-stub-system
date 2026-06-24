import re
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Known valid country codes (subset matching what's seeded in the Country table)
VALID_COUNTRIES = {
    "US", "GB", "DE", "FR", "JP", "BR", "CN", "IN", "CA", "AU", "MX", "IT", "ES", "NL",
    "SE", "NO", "DK", "FI", "CH", "AT", "BE", "PL", "CZ", "PT", "RU", "ZA", "KR", "SG",
    "HK", "TW", "AR", "CL", "CO", "PE", "VE", "EG", "NG", "KE", "SA", "AE", "IL", "TR",
    "TH", "MY", "ID", "PH", "VN", "PK", "BD", "NZ",
}

VALID_CURRENCIES = {
    "USD", "EUR", "GBP", "JPY", "BRL", "CNY", "INR", "CAD", "AUD", "MXN", "CHF", "SEK",
    "NOK", "DKK", "PLN", "CZK", "HUF", "RUB", "ZAR", "KRW", "SGD", "HKD", "TWD", "ARS",
    "CLP", "COP", "SAR", "AED", "TRY", "THB",
}

VALID_BP_TYPES = {"VEND", "CUST", "BOTH"}

BP_NUMBER_PATTERN = re.compile(r"^[0-9]{10}$")


class ValidationEngine:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def validate_batch(self, table_name: str, records: list[dict]) -> dict:
        """
        Validate a batch of records for the given table.
        Returns a dict matching the ValidationResponse schema.
        Does NOT insert data.
        """
        results = []

        for idx, record in enumerate(records):
            errors = []
            warnings = []

            if table_name == "BusinessPartner":
                errors, warnings = await self._validate_business_partner(record, idx, records[:idx])
            else:
                # Generic validation for other tables: check string hygiene on all fields
                errors, warnings = self._validate_generic(record)

            status = "FAIL" if errors else "PASS"
            results.append({
                "index": idx,
                "status": status,
                "errors": errors,
                "warnings": warnings,
            })

        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = len(results) - passed

        # Build summary aggregated across all errors and warnings
        by_rule: dict[str, int] = {}
        by_column: dict[str, int] = {}
        for r in results:
            for e in r["errors"] + r["warnings"]:
                rule = e.get("rule", "unknown")
                field = e.get("field", "unknown")
                by_rule[rule] = by_rule.get(rule, 0) + 1
                by_column[field] = by_column.get(field, 0) + 1

        return {
            "batch_size": len(records),
            "passed": passed,
            "failed": failed,
            "records": results,
            "summary": {"by_rule": by_rule, "by_column": by_column},
        }

    async def _validate_business_partner(
        self, record: dict, idx: int, prior_records: list[dict]
    ) -> tuple[list, list]:
        errors = []
        warnings = []

        # 1. required — BP_NUMBER, bp_type, and NAME1 are required
        for field in ["BP_NUMBER", "bp_type", "NAME1"]:
            val = record.get(field)
            if val is None or val == "":
                errors.append({
                    "rule": "required",
                    "field": field,
                    "message": f"{field} is required",
                })

        if errors:
            # Short-circuit: further rules depend on these fields being present
            return errors, warnings

        bp_number = record.get("BP_NUMBER", "")
        bp_type = record.get("bp_type", "")

        # 2. pattern — BP_NUMBER must be exactly 10 digits
        if not BP_NUMBER_PATTERN.match(bp_number):
            errors.append({
                "rule": "pattern",
                "field": "BP_NUMBER",
                "message": "BP_NUMBER must be exactly 10 digits",
            })

        # 3. allowed_values — bp_type must be VEND, CUST, or BOTH
        if bp_type not in VALID_BP_TYPES:
            errors.append({
                "rule": "allowed_values",
                "field": "bp_type",
                "message": f"bp_type must be one of {sorted(VALID_BP_TYPES)}",
            })

        # 4. iso_code — COUNTRY and CURRENCY validated against known sets
        country = record.get("COUNTRY")
        if country and country not in VALID_COUNTRIES:
            errors.append({
                "rule": "iso_code",
                "field": "COUNTRY",
                "message": f"Unknown country code: {country}",
            })

        currency = record.get("CURRENCY")
        if currency and currency not in VALID_CURRENCIES:
            errors.append({
                "rule": "iso_code",
                "field": "CURRENCY",
                "message": f"Unknown currency code: {currency}",
            })

        # 5. fk_integrity — check if BP_NUMBER already exists in the DB
        #    (report as warning; load engine decides based on mode whether to upsert or reject)
        bp_number_has_error = any(e["field"] == "BP_NUMBER" for e in errors)
        if not bp_number_has_error:
            try:
                result = await self.session.execute(
                    text('SELECT 1 FROM "BusinessPartner" WHERE "BP_NUMBER" = :bp LIMIT 1'),
                    {"bp": bp_number},
                )
                existing = result.fetchone()
                if existing:
                    warnings.append({
                        "rule": "fk_integrity",
                        "field": "BP_NUMBER",
                        "message": f"BP_NUMBER {bp_number} already exists (will upsert if mode=upsert)",
                    })
            except Exception:
                # Table may not yet exist during testing; skip silently
                pass

        # 6. unique within batch — duplicate BP_NUMBER in the same submitted batch
        for prior in prior_records:
            if prior.get("BP_NUMBER") == bp_number:
                errors.append({
                    "rule": "unique",
                    "field": "BP_NUMBER",
                    "message": f"Duplicate BP_NUMBER in batch: {bp_number}",
                })
                break

        # 7. string_hygiene — trailing spaces or control characters in name fields
        for field in ["NAME1", "NAME2"]:
            val = record.get(field)
            if val and isinstance(val, str):
                has_trailing = val != val.rstrip()
                has_control = any(c in val for c in ["\x00", "\r", "\n", "\t"])
                if has_trailing or has_control:
                    warnings.append({
                        "rule": "string_hygiene",
                        "field": field,
                        "message": f"{field} has trailing spaces or control characters",
                    })

        # 8. date_reasonableness — created_at must not be more than 1 year in the future
        created_at = record.get("created_at")
        if created_at:
            try:
                d = date.fromisoformat(str(created_at)[:10])
                if d > date.today() + timedelta(days=365):
                    warnings.append({
                        "rule": "date_reasonableness",
                        "field": "created_at",
                        "message": "created_at is more than 1 year in the future",
                    })
            except (ValueError, TypeError):
                pass

        # 9. cross_field — bp_type=VEND should supply purchasing org data
        if bp_type == "VEND" and not record.get("PURCH_ORG"):
            warnings.append({
                "rule": "cross_field",
                "field": "PURCH_ORG",
                "message": "bp_type=VEND but no PURCH_ORG provided",
            })

        return errors, warnings

    def _validate_generic(self, record: dict) -> tuple[list, list]:
        """Minimal validation for non-BusinessPartner tables: string hygiene only."""
        errors: list = []
        warnings: list = []
        for field, val in record.items():
            if val and isinstance(val, str) and val != val.rstrip():
                warnings.append({
                    "rule": "string_hygiene",
                    "field": field,
                    "message": f"{field} has trailing spaces",
                })
        return errors, warnings
