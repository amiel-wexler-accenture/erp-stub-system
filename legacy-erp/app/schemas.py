from pydantic import BaseModel
from typing import Any, Optional


class SystemInfo(BaseModel):
    system_name: str
    system_type: str
    version: str
    table_count: int
    record_count: int


class TableMeta(BaseModel):
    name: str
    domain: str
    record_count: int
    primary_keys: list[str]


class ColumnDef(BaseModel):
    name: str
    type: str
    nullable: bool
    description: str
    sample_values: list[Any] = []


class TableSchema(BaseModel):
    table_name: str
    columns: list[ColumnDef]


class Relationship(BaseModel):
    from_table: str
    from_column: str
    to_table: str
    to_column: str


class DataResponse(BaseModel):
    records: list[dict[str, Any]]
    total: int
    has_more: bool


class Profile(BaseModel):
    id: str
    name: str
    description: str
    active: bool
