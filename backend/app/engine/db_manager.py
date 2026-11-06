from typing import Any, Dict, List, Optional
from app.data.seed_databases import SEED_DATABASES, SyntheticDatabaseBlueprint
from app.engine.sqlite_executor import SQLiteExecutor
from app.engine.types import QueryResult

class DatabaseManager:
    """
    Central registry for synthetic exercise databases.
    Responsible for looking up database schemas, introspecting tables,
    and creating isolated SQLite execution environments.
    """

    def __init__(self):
        self._databases: Dict[str, SyntheticDatabaseBlueprint] = dict(SEED_DATABASES)

    def get_all(self) -> List[SyntheticDatabaseBlueprint]:
        """Returns all registered synthetic databases."""
        return list(self._databases.values())

    def get_by_id(self, db_id: str) -> Optional[SyntheticDatabaseBlueprint]:
        """Finds database by unique ID or by name."""
        if db_id in self._databases:
            return self._databases[db_id]
        for db in self._databases.values():
            if db.name == db_id:
                return db
        return None

    def get_executor(self, db_id: str) -> SQLiteExecutor:
        """Creates an executor pre-configured with the database initialization DDL/DML."""
        db = self.get_by_id(db_id)
        if not db:
            raise ValueError(f"Synthetic database '{db_id}' not found.")
        return SQLiteExecutor(init_ddl=db.init_ddl, seed_dml=db.seed_dml)

    def preview_table_data(self, db_id: str, table_name: str, limit: int = 10) -> QueryResult:
        """Safely previews sample records for a table in the database."""
        db = self.get_by_id(db_id)
        if not db:
            raise ValueError(f"Synthetic database '{db_id}' not found.")

        # Sanitize table_name against registered tables to prevent injection
        valid_table = next((t.name for t in db.tables if t.name.lower() == table_name.lower()), None)
        if not valid_table:
            raise ValueError(f"Table '{table_name}' does not exist in database '{db.name}'.")

        executor = self.get_executor(db_id)
        return executor.execute_query(f"SELECT * FROM {valid_table} LIMIT {limit};")

db_manager = DatabaseManager()

