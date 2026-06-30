import re
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ..seed import s4hana

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

_PK_MAP: dict[str, list[str]] = {t["name"]: t["primary_keys"] for t in s4hana.get_tables()}

_COMPILED_PATTERNS: dict[str, re.Pattern] = {}


def _get_pattern(regex: str) -> re.Pattern:
    if regex not in _COMPILED_PATTERNS:
        _COMPILED_PATTERNS[regex] = re.compile(regex)
    return _COMPILED_PATTERNS[regex]


class ValidationEngine:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def validate_batch(self, table_name: str, records: list[dict]) -> dict:
        schema_cols = s4hana.get_schema(table_name)
        pk_cols = _PK_MAP.get(table_name, [])
        results = []

        for idx, record in enumerate(records):
            errors, warnings = await self._validate_from_schema(
                record, idx, records[:idx], schema_cols, pk_cols
            )
            status = "FAIL" if errors else "PASS"
            results.append({"index": idx, "status": status, "errors": errors, "warnings": warnings})

        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = len(results) - passed

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

    async def _validate_from_schema(
        self,
        record: dict,
        idx: int,
        prior_records: list[dict],
        schema_cols: list[dict],
        pk_cols: list[str],
    ) -> tuple[list, list]:
        errors: list = []
        warnings: list = []

        for col_def in schema_cols:
            field = col_def["name"]
            val = record.get(field)
            rules = col_def.get("validation_rules", [])

            for rule in rules:
                if rule == "required":
                    if val is None or val == "":
                        errors.append({"rule": "required", "field": field, "message": f"{field} is required"})

                elif rule.startswith("pattern:"):
                    regex = rule[len("pattern:"):]
                    if val is not None and val != "" and not _get_pattern(regex).match(str(val)):
                        errors.append({"rule": "pattern", "field": field, "message": f"{field} must match {regex}"})

                elif rule.startswith("allowed_values:"):
                    allowed = set(rule[len("allowed_values:"):].split(","))
                    if val is not None and val != "" and val not in allowed:
                        errors.append({
                            "rule": "allowed_values",
                            "field": field,
                            "message": f"{field} must be one of {sorted(allowed)}",
                        })

                elif rule == "iso_code:country":
                    if val and val not in VALID_COUNTRIES:
                        errors.append({"rule": "iso_code", "field": field, "message": f"Unknown country code: {val}"})

                elif rule == "iso_code:currency":
                    if val and val not in VALID_CURRENCIES:
                        errors.append({"rule": "iso_code", "field": field, "message": f"Unknown currency code: {val}"})

                elif rule.startswith("fk:"):
                    ref = rule[len("fk:"):]
                    ref_table, ref_col = ref.split(".")
                    if val:
                        try:
                            result = await self.session.execute(
                                text(f'SELECT 1 FROM "{ref_table}" WHERE "{ref_col}" = :v LIMIT 1'),
                                {"v": val},
                            )
                            if not result.fetchone():
                                warnings.append({
                                    "rule": "fk_integrity",
                                    "field": field,
                                    "message": f"{field}={val} not found in {ref_table}.{ref_col}",
                                })
                        except Exception:
                            pass

                elif rule == "string_hygiene":
                    if val and isinstance(val, str):
                        if val != val.rstrip() or any(c in val for c in ["\x00", "\r", "\n", "\t"]):
                            warnings.append({
                                "rule": "string_hygiene",
                                "field": field,
                                "message": f"{field} has trailing spaces or control characters",
                            })

                elif rule == "date_reasonableness":
                    if val:
                        try:
                            d = date.fromisoformat(str(val)[:10])
                            if d > date.today() + timedelta(days=365):
                                warnings.append({
                                    "rule": "date_reasonableness",
                                    "field": field,
                                    "message": f"{field} is more than 1 year in the future",
                                })
                        except (ValueError, TypeError):
                            pass

        # Within-batch duplicate PK check
        if pk_cols and prior_records:
            current_pk = tuple(record.get(c) for c in pk_cols)
            for prior in prior_records:
                if tuple(prior.get(c) for c in pk_cols) == current_pk:
                    pk_desc = ", ".join(f"{c}={record.get(c)}" for c in pk_cols)
                    errors.append({
                        "rule": "unique",
                        "field": pk_cols[0],
                        "message": f"Duplicate PK in batch: {pk_desc}",
                    })
                    break

        return errors, warnings
