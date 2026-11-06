import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_progress_summary_structure():
    res = client.get("/api/progress/summary")
    assert res.status_code == 200
    data = res.json()

    # User profile & rank
    assert "user" in data
    assert "level_title" in data["user"]
    assert "rank_progress_percentage" in data["user"]
    assert "streak_days" in data["user"]

    # 10 core features verification
    assert "overall_progress_percentage" in data
    assert "level_progress" in data
    assert len(data["level_progress"]) == 6
    assert "topic_progress" in data
    assert len(data["topic_progress"]) >= 10
    assert "solved_questions_count" in data
    assert "attempted_questions_count" in data
    assert "submission_accuracy_percentage" in data
    assert "question_accuracy_percentage" in data
    assert "recent_submissions" in data
    assert "weak_topics" in data
    assert "recommended_topic" in data
    assert "weekly_activity" in data
    assert len(data["weekly_activity"]) == 7


def test_anti_exploit_xp_prevention():
    """
    Submitting an already-solved question must NOT award unlimited XP.
    First solve gives XP, subsequent solves give 0 XP.
    """
    # 1. Reset progress
    client.post("/api/progress/reset")

    # 2. Get baseline XP
    initial_user = client.get("/api/auth/me").json()
    base_xp = initial_user["xp"]

    # 3. Solve an unsolved question for the first time: q-003 (Easy, Topic 1)
    solve_payload = {
        "question_id": "q-003",
        "sql": """
        SELECT 
            branch_name AS location_name,
            total_assets AS asset_value
        FROM branches;
        """,
    }

    first_sub = client.post("/api/sql/submit", json=solve_payload).json()
    assert first_sub["status"] == "ACCEPTED"
    assert first_sub["is_first_solve"] is True
    assert first_sub["xp_awarded"] == 20
    assert "Challenge Solved" in first_sub["gamification_message"]

    # Check that user XP increased by 20
    user_after_first = client.get("/api/auth/me").json()
    assert user_after_first["xp"] == base_xp + 20

    # 4. Re-submit the EXACT same solution for q-003 (already solved)
    second_sub = client.post("/api/sql/submit", json=solve_payload).json()
    assert second_sub["status"] == "ACCEPTED"
    assert second_sub["is_first_solve"] is False
    assert second_sub["xp_awarded"] == 0  # ANTI-EXPLOIT: ZERO DUPLICATE XP
    assert "Already Solved" in second_sub["gamification_message"]

    # Check that user XP DID NOT increase again
    user_after_second = client.get("/api/auth/me").json()
    assert user_after_second["xp"] == user_after_first["xp"]


def test_weak_topics_identification():
    """
    Failing submissions on a question should trigger data-driven weak-topic identification.
    """
    # Submit incorrect queries on q-004 (Topic 1: Column Projections)
    wrong_payload = {
        "question_id": "q-004",
        "sql": "SELECT non_existent_column FROM employees;",
    }
    client.post("/api/sql/submit", json=wrong_payload)
    client.post("/api/sql/submit", json=wrong_payload)

    # Check weak topics endpoint
    res = client.get("/api/progress/weak-topics")
    assert res.status_code == 200
    weak_topics = res.json()
    assert len(weak_topics) > 0

    first_weak = weak_topics[0]
    assert first_weak["failed_attempts_count"] >= 2
    assert "reason" in first_weak
    assert "recommended_action" in first_weak
    assert "lesson_url" in first_weak


def test_recommended_next_topic():
    res = client.get("/api/progress/recommended")
    assert res.status_code == 200
    rec = res.json()
    assert rec is not None
    assert "topic_slug" in rec
    assert "title" in rec
    assert "reason" in rec
    assert "practice_url" in rec
    assert "lesson_url" in rec


def test_badges_and_milestones():
    # Get badges
    res = client.get("/api/progress/badges")
    assert res.status_code == 200
    badges = res.json()
    assert len(badges) >= 2  # Seeded initial topic badge and streak badge

    # Mark another topic complete (Topic 2: where-filtering-operators)
    comp_res = client.post("/api/curriculum/topics/where-filtering-operators/complete")
    assert comp_res.status_code == 200
    assert comp_res.json()["is_completed"] is True
    assert comp_res.json()["xp_awarded"] == 100

    # Badges should now include Filter Specialist
    badges_after = client.get("/api/progress/badges").json()
    badge_titles = [b["title"] for b in badges_after]
    assert "Filter Specialist" in badge_titles

    # Marking the same topic complete again should NOT award duplicate XP
    comp_repeat = client.post("/api/curriculum/topics/where-filtering-operators/complete")
    assert comp_repeat.status_code == 200
    assert comp_repeat.json()["xp_awarded"] == 0


def test_level_and_topic_progress_endpoints():
    levels_res = client.get("/api/progress/levels")
    assert levels_res.status_code == 200
    levels = levels_res.json()
    assert len(levels) == 6

    topics_res = client.get("/api/progress/topics")
    assert topics_res.status_code == 200
    topics = topics_res.json()
    assert len(topics) >= 10
