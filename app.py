from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json, os

app = Flask(__name__)
DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    status = request.args.get("status")
    priority = request.args.get("priority")
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or not data.get("title", "").strip():
        return jsonify({"error": "Title is required"}), 400
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "title": data["title"].strip(),
        "description": data.get("description", ""),
        "priority": data.get("priority", "medium"),
        "status": "todo",
        "due_date": data.get("due_date", ""),
        "created_at": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    return jsonify(task), 201

@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json()
    allowed = ["title", "description", "priority", "status", "due_date"]
    for key in allowed:
        if key in data:
            task[key] = data[key]
    task["updated_at"] = datetime.now().isoformat()
    save_tasks(tasks)
    return jsonify(task)

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        return jsonify({"error": "Task not found"}), 404
    save_tasks(new_tasks)
    return jsonify({"message": "Task deleted"}), 200

@app.route("/api/stats", methods=["GET"])
def get_stats():
    tasks = load_tasks()
    return jsonify({
        "total": len(tasks),
        "todo": sum(1 for t in tasks if t["status"] == "todo"),
        "in_progress": sum(1 for t in tasks if t["status"] == "in_progress"),
        "done": sum(1 for t in tasks if t["status"] == "done"),
        "high": sum(1 for t in tasks if t["priority"] == "high"),
        "medium": sum(1 for t in tasks if t["priority"] == "medium"),
        "low": sum(1 for t in tasks if t["priority"] == "low"),
    })

if __name__ == "__main__":
    app.run(debug=True)
