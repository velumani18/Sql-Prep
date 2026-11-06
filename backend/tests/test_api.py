from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_databases():
    response = client.get("/api/databases")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 4
    ids = [d["id"] for d in data]
    assert "db-company" in ids
    assert "db-ecommerce" in ids
    assert "db-university" in ids
    assert "db-banking" in ids

def test_get_database_schema():
    response = client.get("/api/databases/db-ecommerce/schema")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ecommerce_db"
    assert len(data["tables"]) >= 5
    table_names = [t["name"] for t in data["tables"]]
    assert "customers" in table_names
    assert "orders" in table_names
    assert "products" in table_names

def test_get_table_details():
    response = client.get("/api/databases/db-ecommerce/tables/customers")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "customers"
    assert len(data["sample_rows"]) == 10
    assert "id" in data["columns_list"]
    assert "email" in data["columns_list"]

def test_get_question():
    response = client.get("/api/questions/q-101")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "q-101"
    assert data["title"] == "Customers with Zero Purchases"
    assert len(data["test_cases"]) == 3
    # Check that custom_seed_dml was not leaked
    for tc in data["test_cases"]:
        assert "custom_seed_dml" not in tc

def test_sql_execute_endpoint():
    payload = {
        "database_id": "db-ecommerce",
        "sql": "SELECT id, name FROM customers WHERE country = 'Germany';",
    }
    response = client.post("/api/sql/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["columns"] == ["id", "name"]
    assert len(data["rows"]) == 2
    assert data["rows"][0] == [103, "Elena Rostova"]

def test_sql_execute_restricted_blocked():
    payload = {
        "database_id": "db-ecommerce",
        "sql": "DROP TABLE customers;",
    }
    response = client.post("/api/sql/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error_type"] == "RESTRICTED_OPERATION"

def test_sql_submit_accepted():
    # Valid solution for q-101
    payload = {
        "question_id": "q-101",
        "sql": """
        SELECT 
            c.id AS customer_id,
            c.name AS customer_name,
            c.email
        FROM customers c
        LEFT JOIN orders o ON c.id = o.customer_id
        WHERE o.id IS NULL
        ORDER BY c.name ASC;
        """,
    }
    response = client.post("/api/sql/submit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ACCEPTED"
    assert data["all_passed"] is True
    assert data["passed_test_cases"] == 3
    assert data["total_test_cases"] == 3

def test_sql_submit_wrong_answer():
    # Incomplete solution (misses the Anti-join WHERE o.id IS NULL check)
    payload = {
        "question_id": "q-101",
        "sql": """
        SELECT 
            c.id AS customer_id,
            c.name AS customer_name,
            c.email
        FROM customers c
        ORDER BY c.name ASC;
        """,
    }
    response = client.post("/api/sql/submit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "WRONG_ANSWER"
    assert data["all_passed"] is False
    assert data["passed_test_cases"] < data["total_test_cases"]
