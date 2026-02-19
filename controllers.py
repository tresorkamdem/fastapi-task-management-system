import json
import os

TASKS_FILE = "tasks.txt"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []

    tasks = []
    with open(TASKS_FILE, "r") as file:
        for line in file:
            tasks.append(json.loads(line))

    return tasks


def save_tasks(tasks):
    # Create backup before overwriting
    if os.path.exists(TASKS_FILE):
        os.replace(TASKS_FILE, "tasks_backup.txt")

    with open(TASKS_FILE, "w") as file:
        for task in tasks:
            file.write(json.dumps(task) + "\n")

def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1
