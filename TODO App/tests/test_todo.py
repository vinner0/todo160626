# tests/test_todo.py
import json
import os
import pytest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import todo


@pytest.fixture
def tasks():
    return [
        {"id": 1, "text": "Buy groceries", "done": False},
        {"id": 2, "text": "Write report", "done": False},
    ]


def test_edit_updates_task_text(tasks, tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DATA_FILE", str(tmp_path / "todos.json"))
    todo.edit(tasks, 1, "Buy vegetables")
    assert tasks[0]["text"] == "Buy vegetables"


def test_edit_saves_to_file(tasks, tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DATA_FILE", str(tmp_path / "todos.json"))
    todo.edit(tasks, 1, "Buy vegetables")
    with open(tmp_path / "todos.json") as f:
        saved = json.load(f)
    assert saved[0]["text"] == "Buy vegetables"


def test_edit_nonexistent_id_prints_message(tasks, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(todo, "DATA_FILE", str(tmp_path / "todos.json"))
    todo.edit(tasks, 99, "Ghost task")
    out = capsys.readouterr().out
    assert "No task with id 99" in out


def test_edit_does_not_change_done_status(tasks, tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DATA_FILE", str(tmp_path / "todos.json"))
    tasks[0]["done"] = True
    todo.edit(tasks, 1, "Buy vegetables")
    assert tasks[0]["done"] is True
