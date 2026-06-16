import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(__file__), "todos.json")


def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []


def save(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add(tasks, text):
    tasks.append({"id": len(tasks) + 1, "text": text, "done": False})
    save(tasks)
    print(f"Added: {text}")


def list_tasks(tasks):
    if not tasks:
        print("No tasks.")
        return
    for t in tasks:
        status = "[x]" if t["done"] else "[ ]"
        print(f"  {t['id']}. {status} {t['text']}")


def complete(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save(tasks)
            print(f"Done: {t['text']}")
            return
    print(f"No task with id {task_id}")


def delete(tasks, task_id):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            removed = tasks.pop(i)
            save(tasks)
            print(f"Deleted: {removed['text']}")
            return
    print(f"No task with id {task_id}")


def edit(tasks, task_id, new_text):
    for t in tasks:
        if t["id"] == task_id:
            old = t["text"]
            t["text"] = new_text
            save(tasks)
            print(f"Updated: '{old}' -> '{new_text}'")
            return
    print(f"No task with id {task_id}")


HELP = """
Usage:
  python todo.py add <task>               Add a new task
  python todo.py list                     List all tasks
  python todo.py done <id>               Mark task as complete
  python todo.py edit <id> <new text>    Edit a task
  python todo.py delete <id>             Delete a task
"""


def main():
    tasks = load()
    args = sys.argv[1:]

    if not args or args[0] == "help":
        print(HELP)
    elif args[0] == "add" and len(args) > 1:
        add(tasks, " ".join(args[1:]))
    elif args[0] == "list":
        list_tasks(tasks)
    elif args[0] == "done" and len(args) > 1:
        complete(tasks, int(args[1]))
    elif args[0] == "edit" and len(args) > 2:
        edit(tasks, int(args[1]), " ".join(args[2:]))
    elif args[0] == "delete" and len(args) > 1:
        delete(tasks, int(args[1]))
    else:
        print(HELP)


if __name__ == "__main__":
    main()
