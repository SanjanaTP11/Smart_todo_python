import json
import os
from datetime import datetime

FILENAME = "tasks.json"

# Create the file if it doesn't exist
if not os.path.exists(FILENAME):
    with open(FILENAME, 'w') as file:
        json.dump([], file)

def load_tasks():
    with open(FILENAME, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    with open(FILENAME, 'w') as file:
        json.dump(tasks, file, indent=4)

def show_menu():
    print("\nSmart To-Do List Manager")
    print("1. Add Task")
    print("2. Mark Task as Completed")
    print("3. Delete Task")
    print("4. View All Tasks")
    print("5. Exit")

def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            add_task()
        elif choice == "2":
            mark_completed()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            view_tasks()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def add_task():
    tasks = load_tasks()

    # Get input from the user
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    priority = input("Enter priority (High/Medium/Low): ")

    # Auto-increment ID
    task_id = 1
    if tasks:
        task_id = tasks[-1]['id'] + 1

    # Create the task dictionary
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "priority": priority,
        "status": "Pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed_at": None
    }

    # Add task to list and save
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task '{title}' added successfully!")

def mark_completed():
    tasks = load_tasks()

    try:
        task_id = int(input("Enter the ID of the task to mark as completed: "))
    except ValueError:
        print("❌ Invalid ID.")
        return

    found = False
    for task in tasks:
        if task['id'] == task_id:
            if task['status'] == "Completed":
                print("⚠ Task is already marked as completed.")
                return
            task['status'] = "Completed"
            task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            found = True
            break

    if found:
        save_tasks(tasks)
        print("✅ Task marked as completed.")
    else:
        print("❌ Task not found.")

def delete_task():
    tasks = load_tasks()

    try:
        task_id = int(input("Enter the ID of the task to delete: "))
    except ValueError:
        print("❌ Invalid ID.")
        return

    new_tasks = [task for task in tasks if task['id'] != task_id]

    if len(new_tasks) == len(tasks):
        print("❌ Task not found.")
    else:
        save_tasks(new_tasks)
        print("🗑 Task deleted successfully.")

def view_tasks():
    tasks = load_tasks()

    if not tasks:
        print("📭 No tasks found.")
        return

    # Auto update overdue status
    today = datetime.now().date()
    for task in tasks:
        if task["status"] == "Pending":
            due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            if due < today:
                task["status"] = "Overdue"
    save_tasks(tasks)

    # Sort tasks: Overdue first, then by priority
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks.sort(key=lambda t: (t["status"] != "Overdue", priority_order.get(t["priority"], 4)))

    print("\n📋 Your Tasks:")
    for task in tasks:
        print(f"\nID: {task['id']}")
        print(f"Title: {task['title']}")
        print(f"Description: {task['description']}")
        print(f"Due Date: {task['due_date']}")
        print(f"Priority: {task['priority']}")
        print(f"Status: {task['status']}")
        print(f"Created At: {task['created_at']}")
        if task['completed_at']:
            print(f"Completed At: {task['completed_at']}")

# Run the program
main()
