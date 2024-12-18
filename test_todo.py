"""
  File: test_todo.py
  Description: Test suite for todo.py
               Tests core functionality, due dates, and time frames

  Student Name: Arun Mahadevan Sathia Narayanan
  Student UT EID: as235872
  
  Course Name: CS 313E
  Unique Number: 50184
"""

import unittest
from datetime import date, timedelta
import os
from todo import Task, LinkedList, heap_push, heap_pop
from todo import get_time_frame_tasks, initialize_todo_file

class TestTodoList(unittest.TestCase):
    """TestTodoList"""
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Clear any existing todo_list.txt
        if os.path.exists("todo_list.txt"):
            os.remove("todo_list.txt")

        # Initialize empty data structures
        self.tasks = LinkedList()
        self.priority_queue = []

        # Create some test dates
        self.today = date.today()
        self.tomorrow = self.today + timedelta(days=1)
        self.next_week = self.today + timedelta(weeks=1)
        self.last_week = self.today - timedelta(weeks=1)

    def test_task_creation(self):
        """Test basic task creation and validation"""
        # Test valid task creation
        task = Task("Test Task", "Description", 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Description")
        self.assertEqual(task.priority, 1)
        self.assertEqual(task.status, "To Do")

        # Test invalid priority
        with self.assertRaises(ValueError):
            Task("Test", "Description", 0)

        with self.assertRaises(ValueError):
            Task("Test", "Description", -1)

    def test_task_with_due_date(self):
        """Test task creation with due dates"""
        # Test valid future due date
        future_date = self.today + timedelta(days=5)
        task = Task("Future Task", "Description", 1, future_date)
        self.assertEqual(task.due_date, future_date)

        # Test past due date
        past_date = self.today - timedelta(days=5)
        with self.assertRaises(ValueError):
            Task("Past Task", "Description", 1, past_date)

        # Test invalid date format
        with self.assertRaises(ValueError):
            Task("Invalid Date", "Description", 1, "invalid-date")

    def test_linked_list_operations(self):
        """Test LinkedList operations"""
        # Test insert
        self.tasks.insert(Task("Task 1", "Description 1", 1))
        self.assertEqual(len(self.tasks), 1)
        self.assertEqual(self.tasks.get(0).title, "Task 1")

        # Test multiple inserts
        self.tasks.insert(Task("Task 2", "Description 2", 2))
        self.assertEqual(len(self.tasks), 2)

        # Test remove
        removed_task = self.tasks.remove(0)
        self.assertEqual(removed_task.title, "Task 1")
        self.assertEqual(len(self.tasks), 1)

        # Test get
        self.assertEqual(self.tasks.get(0).title, "Task 2")
        self.assertIsNone(self.tasks.get(5))  # Invalid index

    def test_priority_queue(self):
        """Test priority queue operations"""
        # Create tasks with different priorities
        task1 = Task("High Priority", "Description", 1)
        task2 = Task("Medium Priority", "Description", 2)
        task3 = Task("Low Priority", "Description", 3)

        # Test heap push
        heap_push(self.priority_queue, task3)
        heap_push(self.priority_queue, task1)
        heap_push(self.priority_queue, task2)

        # Test heap pop (should come out in priority order)
        self.assertEqual(heap_pop(self.priority_queue).priority, 1)
        self.assertEqual(heap_pop(self.priority_queue).priority, 2)
        self.assertEqual(heap_pop(self.priority_queue).priority, 3)

    def test_time_frame_filtering(self):
        """Test time frame filtering functionality"""
        # Create tasks with different due dates
        task_list = [
            Task("Today Task", "Description", 1, self.today),
            Task("Tomorrow Task", "Description", 2, self.tomorrow),
            Task("Week Task", "Description", 3, self.next_week),
            Task("Overdue Task", "Description", 4, self.last_week, allow_past_dates=True)
        ]
        task_list[3].status = "To Do"  # Ensure overdue task is not marked as done

        # Test today's tasks
        today_tasks, _ = get_time_frame_tasks(task_list, "today")
        self.assertEqual(len(today_tasks), 1)
        self.assertEqual(today_tasks[0].title, "Today Task")

        # Test tomorrow's tasks
        tomorrow_tasks, _ = get_time_frame_tasks(task_list, "tomorrow")
        self.assertEqual(len(tomorrow_tasks), 1)
        self.assertEqual(tomorrow_tasks[0].title, "Tomorrow Task")

        # Test week's tasks
        week_tasks, _ = get_time_frame_tasks(task_list, "week")
        self.assertEqual(len(week_tasks), 3)  # Today, Tomorrow, and Week tasks

        # Test overdue tasks
        _, overdue_tasks = get_time_frame_tasks(task_list, "overdue")
        self.assertEqual(len(overdue_tasks), 1)
        self.assertEqual(overdue_tasks[0].title, "Overdue Task")

    def test_file_operations(self):
        """Test file operations and header line"""
        # Test file initialization
        initialize_todo_file()
        self.assertTrue(os.path.exists("todo_list.txt"))

        # Check header line
        with open("todo_list.txt", "r", encoding="utf-8") as file:
            first_line = file.readline().strip()
            self.assertEqual(first_line, "Task, Description, Priority, Status, Due Date")

        # Clean up
        os.remove("todo_list.txt")

    def test_task_comparison(self):
        """Test task comparison operators"""
        task1 = Task("Task 1", "Description", 1)
        task2 = Task("Task 2", "Description", 2)
        task3 = Task("Task 3", "Description", 1)

        self.assertTrue(task1 < task2)
        self.assertFalse(task1 > task2)
        self.assertTrue(task1 == task3)
        self.assertFalse(task1 == task2)

    def tearDown(self):
        """Clean up after each test method"""
        if os.path.exists("todo_list.txt"):
            os.remove("todo_list.txt")

if __name__ == "__main__":
    unittest.main()
