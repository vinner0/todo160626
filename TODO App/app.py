import json
import os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "todos.json")


def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []


def save(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/todos", methods=["GET"])
def list_todos():
    return jsonify(load())


@app.route("/api/todos", methods=["POST"])
def add_todo():
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "text required"}), 400
    tasks = load()
    task = {"id": next_id(tasks), "text": text, "done": False}
    tasks.append(task)
    save(tasks)
    return jsonify(task), 201


@app.route("/api/todos/<int:task_id>/done", methods=["PATCH"])
def complete_todo(task_id):
    tasks = load()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            save(tasks)
            return jsonify(t)
    return jsonify({"error": "not found"}), 404


@app.route("/api/todos/<int:task_id>", methods=["PUT"])
def edit_todo(task_id):
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "text required"}), 400
    tasks = load()
    for t in tasks:
        if t["id"] == task_id:
            t["text"] = text
            save(tasks)
            return jsonify(t)
    return jsonify({"error": "not found"}), 404


@app.route("/api/todos/<int:task_id>", methods=["DELETE"])
def delete_todo(task_id):
    tasks = load()
    tasks = [t for t in tasks if t["id"] != task_id]
    save(tasks)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
