import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_auth_endpoints():
    # Login
    res = client.post("/api/auth/login", json={"email": "tester@sqlforge.dev"})
    assert res.status_code == 200
    data = res.json()
    assert "token" in data
    assert data["user"]["email"] == "tester@sqlforge.dev"

    # Current user
    me_res = client.get("/api/auth/me")
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "tester@sqlforge.dev"

def test_curriculum_endpoints():
    # List all 6 levels
    levels_res = client.get("/api/curriculum/levels")
    assert levels_res.status_code == 200
    levels = levels_res.json()
    assert len(levels) == 6
    assert levels[0]["level_number"] == 1
    assert len(levels[0]["topics"]) > 0

    # Get single topic
    topic_slug = levels[0]["topics"][0]["slug"]
    topic_res = client.get(f"/api/curriculum/topics/{topic_slug}")
    assert topic_res.status_code == 200
    topic_data = topic_res.json()
    assert topic_data["slug"] == topic_slug
    assert "syntax_reference" in topic_data
    assert len(topic_data["worked_examples"]) >= 3
    assert len(topic_data["practice_questions"]) >= 5

    # Mark topic completed
    comp_res = client.post(f"/api/curriculum/topics/{topic_slug}/complete")
    assert comp_res.status_code == 200
    assert comp_res.json()["is_completed"] is True

def test_questions_list_and_details():
    # List questions
    q_res = client.get("/api/questions?limit=10")
    assert q_res.status_code == 200
    q_data = q_res.json()
    assert q_data["total"] >= 70
    assert len(q_data["questions"]) == 10

    # Get single question from bank (e.g. q-001)
    q1_res = client.get("/api/questions/q-001")
    assert q1_res.status_code == 200
    q1 = q1_res.json()
    assert q1["id"] == "q-001"
    assert q1["database_id"] == "db-company"
    assert len(q1["test_cases"]) >= 2
    # Hidden seed DML should not be leaked
    for tc in q1["test_cases"]:
        assert "custom_seed_dml" not in tc

    # Solution view
    sol_res = client.get("/api/questions/q-001/solution")
    assert sol_res.status_code == 200
    sol = sol_res.json()
    assert "SELECT first_name, last_name, email" in sol["solution_sql"]

def test_question_submission_and_progress_tracking():
    # Submit solution for q-001
    submit_res = client.post("/api/sql/submit", json={
        "question_id": "q-001",
        "sql": "SELECT first_name, last_name, email FROM employees;"
    })
    assert submit_res.status_code == 200
    sub_data = submit_res.json()
    assert sub_data["status"] == "ACCEPTED"
    assert sub_data["all_passed"] is True

    # Check progress summary
    prog_res = client.get("/api/progress/summary")
    assert prog_res.status_code == 200
    prog = prog_res.json()
    assert prog["solved_questions_count"] >= 3
    assert len(prog["recent_submissions"]) > 0
    assert prog["recent_submissions"][0]["question_id"] == "q-001"

