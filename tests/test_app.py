import pytest
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

DATA_FILE = "tasks.json"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    with app.test_client() as c:
        yield c
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


# ─── GET /api/tasks ───────────────────────────────────────────────────────────

def test_get_tasks_empty(client):
    """TC-01: Get all tasks when none exist returns empty list."""
    res = client.get("/api/tasks")
    assert res.status_code == 200
    assert res.get_json() == []


def test_get_tasks_returns_list(client):
    """TC-02: Get all tasks returns a list with created tasks."""
    client.post("/api/tasks", json={"title": "Task A"})
    client.post("/api/tasks", json={"title": "Task B"})
    res = client.get("/api/tasks")
    assert res.status_code == 200
    assert len(res.get_json()) == 2


def test_get_tasks_filter_by_status(client):
    """TC-03: Filtering by status returns only matching tasks."""
    client.post("/api/tasks", json={"title": "Todo Task"})
    task = client.post("/api/tasks", json={"title": "Progress Task"}).get_json()
    client.put(f"/api/tasks/{task['id']}", json={"status": "in_progress"})
    res = client.get("/api/tasks?status=in_progress")
    data = res.get_json()
    assert all(t["status"] == "in_progress" for t in data)


def test_get_tasks_filter_by_priority(client):
    """TC-04: Filtering by priority returns only matching tasks."""
    client.post("/api/tasks", json={"title": "High Task", "priority": "high"})
    client.post("/api/tasks", json={"title": "Low Task", "priority": "low"})
    res = client.get("/api/tasks?priority=high")
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["priority"] == "high"


# ─── POST /api/tasks ──────────────────────────────────────────────────────────

def test_create_task_minimal(client):
    """TC-05: Creating a task with only title succeeds."""
    res = client.post("/api/tasks", json={"title": "Simple Task"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Simple Task"
    assert data["status"] == "todo"
    assert data["priority"] == "medium"


def test_create_task_full(client):
    """TC-06: Creating a task with all fields stores all values."""
    payload = {
        "title": "Full Task",
        "description": "Details here",
        "priority": "high",
        "due_date": "2025-12-31"
    }
    res = client.post("/api/tasks", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["description"] == "Details here"
    assert data["priority"] == "high"
    assert data["due_date"] == "2025-12-31"


def test_create_task_no_title(client):
    """TC-07: Creating a task without a title returns 400."""
    res = client.post("/api/tasks", json={"description": "No title"})
    assert res.status_code == 400


def test_create_task_empty_title(client):
    """TC-08: Creating a task with an empty title returns 400."""
    res = client.post("/api/tasks", json={"title": "   "})
    assert res.status_code == 400


def test_create_task_assigns_unique_ids(client):
    """TC-09: Each created task receives a unique ID."""
    t1 = client.post("/api/tasks", json={"title": "T1"}).get_json()
    t2 = client.post("/api/tasks", json={"title": "T2"}).get_json()
    assert t1["id"] != t2["id"]


# ─── GET /api/tasks/<id> ──────────────────────────────────────────────────────

def test_get_single_task(client):
    """TC-10: Getting a task by ID returns the correct task."""
    created = client.post("/api/tasks", json={"title": "Find Me"}).get_json()
    res = client.get(f"/api/tasks/{created['id']}")
    assert res.status_code == 200
    assert res.get_json()["title"] == "Find Me"


def test_get_nonexistent_task(client):
    """TC-11: Getting a task with non-existent ID returns 404."""
    res = client.get("/api/tasks/9999")
    assert res.status_code == 404


# ─── PUT /api/tasks/<id> ──────────────────────────────────────────────────────

def test_update_task_title(client):
    """TC-12: Updating the title of a task changes it correctly."""
    task = client.post("/api/tasks", json={"title": "Old Title"}).get_json()
    res = client.put(f"/api/tasks/{task['id']}", json={"title": "New Title"})
    assert res.status_code == 200
    assert res.get_json()["title"] == "New Title"


def test_update_task_status(client):
    """TC-13: Updating task status reflects correctly."""
    task = client.post("/api/tasks", json={"title": "Status Test"}).get_json()
    res = client.put(f"/api/tasks/{task['id']}", json={"status": "done"})
    assert res.get_json()["status"] == "done"


def test_update_task_priority(client):
    """TC-14: Updating task priority reflects correctly."""
    task = client.post("/api/tasks", json={"title": "Priority Test"}).get_json()
    res = client.put(f"/api/tasks/{task['id']}", json={"priority": "high"})
    assert res.get_json()["priority"] == "high"


def test_update_nonexistent_task(client):
    """TC-15: Updating a non-existent task returns 404."""
    res = client.put("/api/tasks/9999", json={"title": "Ghost"})
    assert res.status_code == 404


# ─── DELETE /api/tasks/<id> ───────────────────────────────────────────────────

def test_delete_task(client):
    """TC-16: Deleting a task removes it from the list."""
    task = client.post("/api/tasks", json={"title": "Delete Me"}).get_json()
    res = client.delete(f"/api/tasks/{task['id']}")
    assert res.status_code == 200
    tasks = client.get("/api/tasks").get_json()
    assert not any(t["id"] == task["id"] for t in tasks)


def test_delete_nonexistent_task(client):
    """TC-17: Deleting a non-existent task returns 404."""
    res = client.delete("/api/tasks/9999")
    assert res.status_code == 404


# ─── GET /api/stats ───────────────────────────────────────────────────────────

def test_stats_empty(client):
    """TC-18: Stats with no tasks shows all zeros."""
    res = client.get("/api/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total"] == 0


def test_stats_counts(client):
    """TC-19: Stats correctly count tasks by status and priority."""
    client.post("/api/tasks", json={"title": "T1", "priority": "high"})
    t2 = client.post("/api/tasks", json={"title": "T2", "priority": "low"}).get_json()
    client.put(f"/api/tasks/{t2['id']}", json={"status": "done"})
    data = client.get("/api/stats").get_json()
    assert data["total"] == 2
    assert data["todo"] == 1
    assert data["done"] == 1
    assert data["high"] == 1


# ─── Homepage ─────────────────────────────────────────────────────────────────

def test_homepage_loads(client):
    """TC-20: Homepage returns 200 with HTML content."""
    res = client.get("/")
    assert res.status_code == 200
    assert b"TaskFlow" in res.data
