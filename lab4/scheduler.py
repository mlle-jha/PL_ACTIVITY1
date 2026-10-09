import random
import time
from datetime import date

tasks = []
task_id = 1

def add_task(title, priority, due_date):
    global task_id
    task = {
        "id": task_id,
        "title": title,
        "priority": priority,
        "due_date": date.fromisoformat(due_date),
        "done": False
    }
    tasks.append(task)
    task_id += 1

def complete_task(id):
    for task in tasks:
        if task["id"] == id:
            task["done"] = True

def sort_tasks():
    return sorted(tasks, key=lambda task: (task["priority"], task["due_date"]))

def show_tasks():
    for task in sort_tasks():
        status = "Done" if task["done"] else "Not Done"
        print(
            f"ID: {task['id']} | "
            f"Task: {task['title']} | "
            f"Priority: {task['priority']} | "
            f"Due: {task['due_date']} | "
            f"Status: {status}"
        )
print("Python:")
add_task("Deadline OS Project", 2, "2026-10-12")
add_task("Pass PL Activity 4 & 5", 1, "2026-10-09")
add_task("Remedial Quiz 5", 3, "2026-10-13")

complete_task(2)

print("\n-- Task List --")
show_tasks()

print("\n-- Type Tests --")
add_task("Bad Task", "1", "2026-10-20")

print("Invalid priority was accepted when adding the task.")

try:
    show_tasks()
except TypeError as error:
    print("Sorting Error:", error)

tasks.pop()

try:
    result = "5" + 3
    print(result)
except TypeError as error:
    print("'5' + 3 Error:", error)

print("2 ** 63 + 1 =", 2 ** 63 + 1)

print("\n-- Benchmark --")
tasks.clear()
task_id = 1
random.seed(42)
number_of_tasks = 200000
start_time = time.perf_counter()

for i in range(number_of_tasks):
    priority = random.randrange(5)
    day = 10 + random.randrange(18)
    add_task(
        f"Task {i}",
        priority,
        f"2026-10-{day}"
    )
sort_tasks()
end_time = time.perf_counter()
total_time = (end_time - start_time) * 1000

print(number_of_tasks, "tasks added and sorted in",
      round(total_time, 1), "ms")