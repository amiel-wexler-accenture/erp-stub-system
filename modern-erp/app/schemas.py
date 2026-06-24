from pydantic import BaseModel
from typing import Any, Optional


class ModernSystemInfo(BaseModel):
    system_name: str
    api_version: str
    supports_validation: bool
    max_batch_size: int


class TableMeta(BaseModel):
    name: str
    domain: str
    record_count: int
    primary_keys: list[str]
    load_supported: bool = True
    validate_supported: bool = True


class ValidationRule(BaseModel):
    rule_type: str
    field: str
    constraint: str
    severity: str  # "ERROR" or "WARNING"


class ModernColumnDef(BaseModel):
    name: str
    type: str
    nullable: bool
    description: str
    sample_values: list[Any] = []
    validation_rules: list[ValidationRule] = []


class TableSchema(BaseModel):
    table_name: str
    columns: list[ModernColumnDef]


class Relationship(BaseModel):
    from_table: str
    from_column: str
    to_table: str
    to_column: str


class DataResponse(BaseModel):
    records: list[dict[str, Any]]
    total: int
    has_more: bool


class ValidationRecord(BaseModel):
    index: int
    status: str  # "PASS" or "FAIL"
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []


class ValidationSummary(BaseModel):
    by_rule: dict[str, int] = {}
    by_column: dict[str, int] = {}


class ValidationResponse(BaseModel):
    batch_size: int
    passed: int
    failed: int
    records: list[ValidationRecord]
    summary: ValidationSummary


class LoadRequest(BaseModel):
    records: list[dict[str, Any]]
    mode: str = "upsert"  # insert | upsert | update_only
    on_error: str = "reject_record"  # reject_record | reject_batch | log_and_continue


class LoadResponse(BaseModel):
    batch_id: str
    inserted: int
    updated: int
    rejected: int
    errors: list[dict[str, Any]] = []


class LoadStatus(BaseModel):
    batch_id: str
    table_name: str
    status: str
    inserted: int
    updated: int
    rejected: int
    created_at: str


class Profile(BaseModel):
    id: str
    name: str
    description: str
    active: bool
