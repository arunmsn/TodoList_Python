# TodoList_Python

## About  
This is a ToDo List application that allows users to manage tasks with the following features:  
- Add tasks with title, description, and priority levels  
- Update task status and priority  
- Delete tasks  
- List tasks in different views (by index, priority, filtered by status, due date, or by time frame)  
- Persistent storage using a text file  
- Priority-based task organization

## Main Classes and Methods:  
Node: Basic node structure for linked list  
Attributes: task, next  

LinkedList: Main data structure for storing tasks  
Methods: insert(), remove(), get(), len()  

Task: Represents a single task  
Attributes: title, description, status, priority  
Methods: lt() for priority comparison

## Heap Functions:  
heap_push(): Adds items to priority queue  
heap_pop(): Removes items from priority queue  
_heap_up(): Maintains heap property upward  
_heap_down(): Maintains heap property downward

## Main Program Functions:  
load_tasks(): Loads tasks from file  
save_tasks(): Saves tasks to file  
add_task(): Creates new tasks  
update_task(): Modifies existing tasks  
delete_task(): Removes tasks  
list_tasks(): Displays tasks in various formats  
get_user_input(): Handles user input for task creation  
get_time_frame_tasks(): Shows the tasks within a specified time frame  
print_task_list(): Helper function to print tasks (using a consistent format)

## Libraries:     
os: For file operations (checking file existence, file input/output)  
typing: For type hints (List)  
datetime: For measuring with dates and time frames

## Data Structures:    
Linked List: Main storage structure for tasks  
Implementation: Custom LinkedList class with Node class  
Used for: Sequential storage and access of tasks  

Min Heap (Priority Queue): Secondary structure for priority-based access  
Implementation: List-based binary heap with helper functions  
Used for: Priority-based task organization and viewing

## Test Cases:    
Test cases as seen in "test_todo.py".

## Strengths/Weaknesses:    
Strengths:  
- Solid basic task management functionality
- Efficient priority-based task organization
- Persistent storage
- Multiple viewing options

Expected Weaknesses:  
- No support for task categories or tags (only status of task)
- Basic text-based interface - only Command-Line, not GUI
