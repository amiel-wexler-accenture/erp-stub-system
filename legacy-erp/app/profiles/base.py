from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncEngine


class BaseProfile(ABC):
    """
    Abstract base class for ERP system profiles.

    All profiles (SAP ECC, Oracle EBS, Dynamics AX, Generic) must implement this interface
    to support schema creation, data seeding, and metadata queries.
    """

    @property
    @abstractmethod
    def profile_id(self) -> str:
        """
        Unique profile identifier.

        Examples: 'sap_ecc', 'oracle_ebs', 'dynamics_ax', 'generic'
        """
        ...

    @property
    @abstractmethod
    def system_name(self) -> str:
        """
        System name for API responses.

        Must match registered identifiers in FloX Foundry source registry.
        Examples: 'ECC-1', 'ORACLE-EBS-1', 'DYNAMICS-AX-1', 'GENERIC-1'
        """
        ...

    @property
    @abstractmethod
    def system_type(self) -> str:
        """
        Human-readable system type.

        Examples: 'SAP ECC', 'Oracle E-Business Suite', 'Microsoft Dynamics AX', 'Generic Legacy'
        """
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """
        System version string.

        Examples: '6.0 EHP8', '12.2', '2012 R3', '1.0'
        """
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Human-readable profile description for UI display.

        Should explain the persona and use case.
        """
        ...

    @abstractmethod
    async def create_tables(self, engine: AsyncEngine) -> None:
        """
        Create all tables for this profile.

        Must be idempotent when called with fresh database.
        Uses SQLAlchemy async API via engine.
        """
        ...

    @abstractmethod
    async def drop_tables(self, engine: AsyncEngine) -> None:
        """
        Drop all tables for this profile.

        Used during profile switching to reset database.
        Must handle tables in correct dependency order (FKs first).
        """
        ...

    @abstractmethod
    async def seed_data(self, engine: AsyncEngine) -> None:
        """
        Seed initial data into all tables.

        Must be deterministic (Faker.seed(42), random.seed(42)).
        Injects data quality issues as per CLAUDE.md for legacy systems.
        Uses bulk INSERT operations for performance.
        """
        ...

    @abstractmethod
    def get_tables(self) -> list[dict]:
        """
        Return metadata for all tables in this profile.

        Returns:
            list[dict] with keys: {name, domain, record_count, primary_keys}

        Example:
            [
                {
                    "name": "LFA1",
                    "domain": "Vendor Master",
                    "record_count": 1000,
                    "primary_keys": ["MANDT", "LIFNR"]
                },
                ...
            ]
        """
        ...

    @abstractmethod
    def get_schema(self, table_name: str) -> dict:
        """
        Return column-level schema definition for a table.

        Args:
            table_name: Table name to retrieve schema for.

        Returns:
            dict with keys:
                - table_name: str
                - columns: list[dict] with keys {name, type, nullable, description, sample_values}

        Example:
            {
                "table_name": "LFA1",
                "columns": [
                    {
                        "name": "MANDT",
                        "type": "char(3)",
                        "nullable": False,
                        "description": "Client ID",
                        "sample_values": ["100", "200"]
                    },
                    {
                        "name": "LIFNR",
                        "type": "char(10)",
                        "nullable": False,
                        "description": "Vendor ID",
                        "sample_values": ["0000001234", "0000005678"]
                    },
                    ...
                ]
            }
        """
        ...

    @abstractmethod
    def get_relationships(self, table_name: str) -> list[dict]:
        """
        Return foreign key relationships for a table.

        Args:
            table_name: Table name to retrieve relationships for.

        Returns:
            list[dict] with keys {from_table, from_column, to_table, to_column}

        Example:
            [
                {
                    "from_table": "LFB1",
                    "from_column": "LIFNR",
                    "to_table": "LFA1",
                    "to_column": "LIFNR"
                },
                ...
            ]
        """
        ...

    def get_table_names(self) -> list[str]:
        """
        Convenience method: return list of table names.

        Returns:
            List of table name strings from get_tables().
        """
        return [t["name"] for t in self.get_tables()]
