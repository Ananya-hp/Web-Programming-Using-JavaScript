# Student Name:
# Roll No:
# Assignment 4 - Flask Powered Dynamic To-Do List Application
# Date:

from flask import Flask, render_template, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)

tasks = []
next_id = 1


def find_task(task_id):
    """Find a task by ID."""
    return next((task for task in tasks if task["id"] == task_id), None)


@app.route("/")
def home():
    """Render the main To-Do page."""
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks with optional filtering."""
    status = request.args.get("status")
    filtered = tasks

    if status == "active":
        filtered = [task for task in tasks if not task["completed"]]
    elif status == "completed":
        filtered = [task for task in tasks if task["completed"]]

    return jsonify(filtered), 200


@app.route("/api/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    global next_id

    data = request.get_json()

    if not data or not data.get("title", "").strip():
        return jsonify({"error": "Title is required"}), 400

    priority = data.get("priority", "medium").lower()
    if priority not in ["low", "medium", "high"]:
        priority = "medium"

    task = {
        "id": next_id,
        "title": data["title"].strip(),
        "description": data.get("description", "").strip(),
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update an existing task."""
    task = find_task(task_id)
    if not task:
        abort(404)

    data = request.get_json()

    if "title" in data:
        if not data["title"].strip():
            return jsonify({"error": "Title cannot be empty"}), 400
        task["title"] = data["title"].strip()

    if "description" in data:
        task["description"] = data["description"].strip()

    if "priority" in data:
        priority = data["priority"].lower()
        task["priority"] = priority if priority in ["low", "medium", "high"] else "medium"

    if "completed" in data:
        task["completed"] = bool(data["completed"])

    return jsonify(task), 200


@app.route("/api/tasks/<int:task_id>/toggle", methods=["PATCH"])
def toggle_task(task_id):
    """Toggle task completion status."""
    task = find_task(task_id)
    if not task:
        abort(404)

    task["completed"] = not task["completed"]
    return jsonify(task), 200


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task."""
    task = find_task(task_id)
    if not task:
        abort(404)

    tasks.remove(task)
    return "", 204


@app.route("/api/tasks", methods=["DELETE"])
def clear_all_tasks():
    """Delete all tasks."""
    global tasks
    tasks = []
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)