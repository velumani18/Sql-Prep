from typing import Dict, List, Optional
from pydantic import BaseModel

class ColumnInfo(BaseModel):
    name: str
    type: str
    is_primary_key: bool = False
    is_foreign_key: bool = False
    references: Optional[str] = None
    nullable: bool = True

class TableInfo(BaseModel):
    name: str
    description: str
    columns: List[ColumnInfo]
    row_count: int

class SyntheticDatabaseBlueprint(BaseModel):
    id: str
    name: str
    display_name: str
    description: str
    init_ddl: str
    seed_dml: str
    tables: List[TableInfo]

def load_seed_databases() -> Dict[str, SyntheticDatabaseBlueprint]:
    from app.data.company_db import COMPANY_DATABASE
    from app.data.ecommerce_db import ECOMMERCE_DATABASE
    from app.data.university_db import UNIVERSITY_DATABASE
    from app.data.banking_db import BANKING_DATABASE

    return {
        "db-company": COMPANY_DATABASE,
        "db-ecommerce": ECOMMERCE_DATABASE,
        "db-university": UNIVERSITY_DATABASE,
        "db-banking": BANKING_DATABASE,
    }

SEED_DATABASES: Dict[str, SyntheticDatabaseBlueprint] = load_seed_databases()
