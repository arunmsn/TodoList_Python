# Baseline code for the term project
"""
  File: todo.py
  Description: Creates a todo list that is editable by users 
               and can be viewed in different methods.

  Student Name: Arun Mahadevan Sathia Narayanan
  Student UT EID: as235872

  Course Name: CS 313E
  Unique Number: 50184
"""

import os
from typing import List
from datetime import datetime, date, timedelta

def initialize_todo_file():
    """Creates the todo list file with headers if it doesn't exist"""
    if not os.path.exists("todo_list.txt"):
        with open("todo_list.txt", "w", encoding="utf-8") as file:
            file.write("Task, Description, Priority, Status, Due Date\n")

class Node:
    """Defines a node"""
    def __init__(self, task):
        self.task = task
        self.next = None

class LinkedList:
    """Defines a LinkedList"""
    def __init__(self):
        self.head = None
        self.length = 0

    def insert(self, task):
        """Inserts a new node at the end of the list"""
        new_node = Node(task)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.length += 1

    def remove(self, index):
        """Removes a specified node at the index"""
        if self.head is None:
            return None
        if index == 0:
            removed = self.head
            self.head = self.head.next
            self.length -= 1
            return removed.task
        current = self.head
        for _ in range(index - 1):
            if current.next is None:
                return None
            current = current.next
        if current.next is None:
            return None
        removed = current.next
        current.next = current.next.next
        self.length -= 1
        return removed.task

    def get(self, index):
        """Gets the specific node at the index"""
        if self.head is None:
            return None
        current = self.head
        for _ in range(index):
            if current.next is None:
                return None
            current = current.next
        return current.task

    def __len__(self):
        return self.length

class Task:
    """Defines a Task with priority and due date validation"""
    def __init__(self, title, description, priority, due_date=None, allow_past_dates=False):
        self.title = title
        self.description = description
        self.status = "To Do"

        # Ensure priority is a positive integer
        if not isinstance(priority, int) or priority < 1:
            raise ValueError("Priority must be a positive integer (1 is highest)")
        self.priority = priority

        # Due date validation
        if due_date:
            # Convert string to date if needed
            if isinstance(due_date, str):
                try:
                    due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                except ValueError as e:
                    raise ValueError("Invalid date format. Use YYYY-MM-DD") from e

            # Ensure due date is a date object
            if not isinstance(due_date, date):
                raise ValueError("Due date must be a valid date")

            # Validate that due date is not in the past unless explicitly allowed
            if not allow_past_dates and due_date < date.today():
                raise ValueError("Due date cannot be in the past")

        self.due_date = due_date

    # Add comparison methods for priority-based comparison
    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def __str__(self):
        return f"Task(title={self.title}, priority={self.priority}, status={self.status})"

def heap_push(heap, item):
    """Adds an item to the heap and then maintains the heap property"""
    heap.append(item)
    _heap_up(heap, len(heap) - 1)

def heap_pop(heap):
    """Removes an item from the heap and then maintains the heap property"""
    if not heap:
        return None

    if len(heap) == 1:
        return heap.pop()

    result = heap[0]
    heap[0] = heap.pop()  # Move last element to root
    if heap:  # Only heapify if there are elements remaining
        _heap_down(heap, 0)
    return result

def _heap_up(heap, index):
    """Maintains the heap property of the heap, bubbles up items"""
    while index > 0:
        parent = (index - 1) // 2
        if heap[parent] > heap[index]:
            heap[parent], heap[index] = heap[index], heap[parent]
            index = parent
        else:
            break

def _heap_down(heap, index):
    """Maintains the heap property of the heap, bubbles down items"""
    if not heap:  # Safety check
        return

    while True:
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(heap) and heap[left] < heap[smallest]:
            smallest = left
        if right < len(heap) and heap[right] < heap[smallest]:
            smallest = right

        if smallest == index:
            break

        heap[index], heap[smallest] = heap[smallest], heap[index]
        index = smallest

def get_user_input() -> List[str]:
    """Gets the user input with priority and due date validation"""
    title = input("Enter the task title: ")
    description = input("Enter the task description: ")

    while True:
        try:
            priority = int(input("Enter the task priority (1 is highest): "))
            if priority < 1:
                print("Priority must be a positive integer (1 is highest)")
                continue
            break
        except ValueError:
            print("Please enter a valid number")

    # Optional due date input
    due_date_input = input("Enter due date (YYYY-MM-DD, press Enter to skip): ")
    due_date = None
    if due_date_input:
        try:
            due_date = datetime.strptime(due_date_input, "%Y-%m-%d").date()
            if due_date < date.today():
                print("Due date cannot be in the past")
                due_date = None
        except ValueError:
            print("Invalid date format. Skipping due date.")

    return [title, description, priority, due_date]

tasks = LinkedList()
priority_queue = []

def load_tasks():
    """Loads tasks from the file with due date support"""
    if os.path.exists("todo_list.txt"):
        with open("todo_list.txt", "r", encoding="utf-8") as file:
            # Skip the header line
            next(file)  # This skips the "Task,Description,Priority,Status,Due Date" line

            for line in file:
                parts = line.strip().split(", ")
                if len(parts) == 5:
                    title, description, priority, status, due_date_str = parts
                    task = Task(title, description, int(priority),
                                due_date_str if due_date_str else None,
                                allow_past_dates=True)  # Allow past dates when loading from file
                    task.status = status
                    tasks.insert(task)
                    heap_push(priority_queue, task)
                elif len(parts) == 4:  # Backwards compatibility
                    title, description, priority, status = parts
                    task = Task(title, description, int(priority), allow_past_dates=True)
                    task.status = status
                    tasks.insert(task)
                    heap_push(priority_queue, task)

def save_tasks():
    """Saves tasks to the file with due date, preserving the header"""
    with open("todo_list.txt", "w", encoding="utf-8") as file:
        # Write the header line first
        file.write("Task, Description, Priority, Status, Due Date\n")
        # Write all tasks
        for i in range(len(tasks)):
            task = tasks.get(i)
            # Include due date in save format
            due_date_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else ""
            file.write(\
            f"{task.title}, {task.description}, {task.priority}, {task.status}, {due_date_str}\n")

def add_task():
    """Adds a Task with a Title, Description, and Priority"""
    title, description, priority, due_date = get_user_input()
    task = Task(title, description, priority, due_date)
    tasks.insert(task)
    heap_push(priority_queue, task)
    save_tasks()
    print(f"Added task: {title}")

def update_task():
    """Updates a Task's Status, Priority, or Due Date"""
    # Get the task index
    try:
        index = int(input("Enter the index of the task to update: "))
    except ValueError:
        print("Please enter a valid number")
        return

    # Verify task exists
    task = tasks.get(index-1)
    if not task:
        print("Invalid task index.")
        return

    # Show update options
    print("\nWhat would you like to update?")
    print("1. Status")
    print("2. Priority")
    print("3. Due Date")
    update_choice = input("Enter your choice (1-3): ")

    if update_choice == "1":
        # Update status
        status = input("Enter the new status: ")
        task.status = status
        print(f"Updated task: {task.title} - Status: {status}")

    elif update_choice == "2":
        # Update priority
        try:
            new_priority = int(input("Enter the new priority (1 is highest): "))
            # Remove and re-add to priority queue to maintain heap property
            priority_queue.remove(task)
            task.priority = new_priority
            heap_push(priority_queue, task)
            print(f"Updated task: {task.title} - Priority: {new_priority}")
        except ValueError:
            print("Invalid priority value. Please enter a number.")
            return

    elif update_choice == "3":
        # Update due date
        due_date_inpt = input("Enter new due date (YYYY-MM-DD) or press Enter to remove due date: ")

        if due_date_inpt:
            try:
                new_due_date = datetime.strptime(due_date_inpt, "%Y-%m-%d").date()
                if new_due_date < date.today():
                    print("Due date cannot be in the past")
                    return
                task.due_date = new_due_date
                print(f"Updated task: {task.title} - Due Date: {new_due_date}")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                return
        else:
            # Remove due date
            task.due_date = None
            print(f"Removed due date for task: {task.title}")

    else:
        print("Invalid choice.")
        return

    save_tasks()

def delete_task():
    """Removes a Task at a specific index"""
    index = int(input("Enter the index of the task to delete: "))
    if tasks.get(index-1):
        task = tasks.remove(index-1)
    else:
        print("Invalid action.")
        return
    priority_queue.remove(task)
    save_tasks()
    print(f"Deleted task: {task.title}")

def get_time_frame_tasks(task_list, time_frame):
    """
    Filters tasks based on specified time frame
    Returns tasks that fall within the time frame and overdue tasks
    """
    today = date.today()

    # Calculate end dates for different time frames
    time_frames = {
        "today": today,
        "tomorrow": today + timedelta(days=1),
        "week": today + timedelta(weeks=1),
        "month": today + timedelta(days=30),
        "overdue": today
    }

    if time_frame not in time_frames:
        return [], []

    end_date = time_frames[time_frame]

    # Filter tasks based on time frame
    filtered_tasks = []
    overdue_tasks = []

    for task in task_list:
        if task.due_date:
            if time_frame == "overdue":
                if task.due_date < today and task.status.lower() != "done":
                    overdue_tasks.append(task)
            elif time_frame == "today":
                if task.due_date == today:
                    filtered_tasks.append(task)
            elif time_frame == "tomorrow":
                if task.due_date == end_date:
                    filtered_tasks.append(task)
            else:  # week or month
                if today <= task.due_date <= end_date:
                    filtered_tasks.append(task)

    return filtered_tasks, overdue_tasks

def print_task_list(tasks_to_print, header):
    """Helper function to print tasks in a consistent format"""
    if tasks_to_print:
        print(f"\n{header}:")
        for i, task in enumerate(tasks_to_print, 1):
            if task.due_date:
                due_date_str = task.due_date.strftime("%Y-%m-%d")
            else:
                due_date_str = "No due date"
            print(f"{i}. {task.title} - Status: {task.status} - "
                  f"Priority: {task.priority} - Due: {due_date_str}")
    else:
        print(f"\nNo tasks found for {header.lower()}")

def list_tasks():
    """Prints out the Tasks with enhanced viewing options"""
    if len(tasks) == 0:
        print("ToDo list is empty.")
    else:
        print("\nTodo List Menu:")
        print("1. View by Index")
        print("2. View by Priority")
        print("3. Filter by Status")
        print("4. View by Due Date")
        print("5. View by Time Frame")
        choice = input("Enter your choice (1-5): ")

        # Create a list of all tasks in their current order
        task_list = []
        current = tasks.head
        while current is not None:
            task_list.append(current.task)
            current = current.next

        if choice == "1":
            print("Todo List:")
            for i, task in enumerate(task_list, 1):
                due_date_str = task.due_date.strftime("%Y-%m-%d") \
                    if task.due_date else "No due date"
                print(f"{i}. {task.title} - Status: {task.status} - "
                      f"Priority: {task.priority} - Due: {due_date_str}")

        elif choice == "2":
            print("Todo List (by Priority):")
            priority_tasks = sorted(priority_queue)
            for task in priority_tasks:
                x = priority_queue.index(task)
                due_date_str = task.due_date.strftime("%Y-%m-%d") \
                    if task.due_date else "No due date"
                print(f"{x+1}. {task.title} - Status: {task.status} - "
                      f"Priority: {task.priority} - Due: {due_date_str}")

        elif choice == "3":
            # Get unique statuses from existing tasks
            statuses = set(task.status for task in task_list)
            print("\nAvailable statuses:")
            for status in sorted(statuses):
                print(f"- {status}")

            # Get status to filter by
            filter_status = input("\nEnter status to filter by: ")

            # Filter and display tasks
            filtered_tasks = [task for task in task_list
                              if task.status.lower() == filter_status.lower()]
            print_task_list(filtered_tasks, f"Tasks with status '{filter_status}'")

        elif choice == "4":
            print("Tasks sorted by Due Date:")
            # Sort tasks by due date, with tasks without due dates at the end
            sorted_tasks = sorted(task_list, key=lambda x: (x.due_date is None,
                                                            x.due_date or date.max))
            print_task_list(sorted_tasks, "Tasks by due date")

        elif choice == "5":
            print("\nTime Frame Options:")
            print("1. View Overdue Tasks")
            print("2. View Tasks Due Today")
            print("3. View Tasks Due Tomorrow")
            print("4. View Tasks Due in a Week")
            print("5. View Tasks Due in a Month")
            print("6. View All Time Frames")

            time_choice = input("Enter your choice (1-6): ")

            time_frames = {
                "1": "overdue",
                "2": "today",
                "3": "tomorrow",
                "4": "week",
                "5": "month"
            }

            if time_choice in time_frames:
                time_frame = time_frames[time_choice]
                filtered_tasks, overdue_tasks = get_time_frame_tasks(task_list, time_frame)

                if time_frame == "overdue":
                    print_task_list(overdue_tasks, "Overdue Tasks")
                else:
                    print_task_list(filtered_tasks, f"Tasks due {time_frame}")

            elif time_choice == "6":
                # Show all time frames
                for label in ["Overdue Tasks", "Due Today", "Due Tomorrow",
                            "Due This Week", "Due This Month"]:
                    time_frame = label.split()[1].lower()
                    filtered_tasks, overdue_tasks = \
                        get_time_frame_tasks(task_list, time_frame)

                    if time_frame == "overdue":
                        print_task_list(overdue_tasks, label)
                    else:
                        print_task_list(filtered_tasks, label)

            else:
                print("Invalid choice. Please try again.")

        else:
            print("Invalid choice. Please try again.")

def main():
    """Main method"""
    load_tasks()

    while True:
        print("\nTodo List Menu:")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Delete Task")
        print("4. List Tasks")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add_task()
        elif choice == "2":
            update_task()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            list_tasks()
        elif choice == "5":
            save_tasks()
            print("ToDo List has been saved. Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
