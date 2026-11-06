from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, Query, status
from app.engine.db_manager import db_manager

router = APIRouter(prefix="/api/databases", tags=["Synthetic Databases"])

@router.get("", response_model=List[Dict[str, Any]])
def list_databases() -> List[Dict[str, Any]]:
    """Returns a list of all available synthetic relational databases."""
    databases = db_manager.get_all()
    return [
        {
            "id": db.id,
            "name": db.name,
            "display_name": db.display_name,
            "description": db.description,
            "tables_count": len(db.tables),
        }
        for db in databases
    ]

@router.get("/{database_id}/schema", response_model=Dict[str, Any])
def get_database_schema(database_id: str) -> Dict[str, Any]:
    """Returns the complete relational schema metadata and column definitions."""
    db = db_manager.get_by_id(database_id)
    if not db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Database '{database_id}' not found.",
        )

    return {
        "id": db.id,
        "name": db.name,
        "display_name": db.display_name,
        "description": db.description,
        "tables": [table.model_dump() for table in db.tables],
    }

@router.get("/{database_id}/tables/{table_name}", response_model=Dict[str, Any])
def get_table_details(
    database_id: str,
    table_name: str,
    limit: int = Query(default=10, ge=1, le=100),
) -> Dict[str, Any]:
    """Returns column metadata and sample rows for a specific table."""
    db = db_manager.get_by_id(database_id)
    if not db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Database '{database_id}' not found.",
        )

    table = next((t for t in db.tables if t.name.lower() == table_name.lower()), None)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table '{table_name}' does not exist in database '{db.name}'.",
        )

    preview_res = db_manager.preview_table_data(database_id, table.name, limit=limit)

    return {
        "table_name": table.name,
        "description": table.description,
        "columns": [col.model_dump() for col in table.columns],
        "row_count": table.row_count,
        "sample_rows": preview_res.rows,
        "columns_list": preview_res.columns,
    }

