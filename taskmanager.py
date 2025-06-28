import sqlite3
import os
from datetime import datetime

def create_database():
    """Create the database with tasks table and history tracking."""
    conn = sqlite3.connect('A1_09_4_q3.db')
    cursor = conn.cursor()
    
    # Create the main tasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending',
        priority TEXT DEFAULT 'medium',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create the history table for version control
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks_history (
        history_id INTEGER PRIMARY KEY,
        task_id INTEGER,
        title TEXT,
        description TEXT,
        status TEXT,
        priority TEXT,
        operation TEXT NOT NULL,
        changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES tasks(id)
    )
    ''')
    
    conn.commit()
    return conn

def setup_triggers(conn):
    """Set up triggers to track changes to the tasks table."""
    cursor = conn.cursor()
    
    # Trigger for INSERT operations
    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS tasks_insert_trigger
    AFTER INSERT ON tasks
    BEGIN
        INSERT INTO tasks_history (
            task_id, title, description, status, priority, 
            operation, changed_at
        )
        VALUES (
            NEW.id, NEW.title, NEW.description, NEW.status, 
            NEW.priority, 'INSERT', CURRENT_TIMESTAMP
        );
    END;
    ''')
    
    # Trigger for UPDATE operations
    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS tasks_update_trigger
    AFTER UPDATE ON tasks
    BEGIN
        INSERT INTO tasks_history (
            task_id, title, description, status, priority, 
            operation, changed_at
        )
        VALUES (
            NEW.id, NEW.title, NEW.description, NEW.status, 
            NEW.priority, 'UPDATE', CURRENT_TIMESTAMP
        );
    END;
    ''')
    
    # Trigger for DELETE operations
    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS tasks_delete_trigger
    AFTER DELETE ON tasks
    BEGIN
        INSERT INTO tasks_history (
            task_id, title, description, status, priority, 
            operation, changed_at
        )
        VALUES (
            OLD.id, OLD.title, OLD.description, OLD.status, 
            OLD.priority, 'DELETE', CURRENT_TIMESTAMP
        );
    END;
    ''')
    
    conn.commit()

def initialize_task_manager():
    """Initialize the task manager with version control."""
    # Create database and tables
    conn = create_database()
    
    # Set up triggers for history tracking
    setup_triggers(conn)
    
    return conn

def add_task(conn, title, description, status='pending', priority='medium'):
    """Add a new task and record it in history."""
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tasks (title, description, status, priority, updated_at)
    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (title, description, status, priority))
    task_id = cursor.lastrowid
    conn.commit()
    print("Task {task_id} added successfully.")
    return task_id

def update_task(conn, task_id, title=None, description=None, status=None, priority=None):
    """Update a task and record the change in history."""
    cursor = conn.cursor()
    
    # First check if the task exists
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        print(f"No task found with ID {task_id}.")
        return False
    
    # Build update query based on provided parameters
    update_parts = []
    values = []
    
    if title is not None:
        update_parts.append("title = ?")
        values.append(title)
    if description is not None:
        update_parts.append("description = ?")
        values.append(description)
    if status is not None:
        update_parts.append("status = ?")
        values.append(status)
    if priority is not None:
        update_parts.append("priority = ?")
        values.append(priority)
    
    if not update_parts:
        print("No updates provided.")
        return False
    
    # Add updated_at timestamp
    update_parts.append("updated_at = CURRENT_TIMESTAMP")
    
    # Execute the update
    query = f"UPDATE tasks SET {', '.join(update_parts)} WHERE id = ?"
    values.append(task_id)
    
    cursor.execute(query, values)
    conn.commit()
    print(f"Task {task_id} updated successfully.")
    return True

def complete_task(conn, task_id):
    """Mark a task as completed."""
    return update_task(conn, task_id, status='completed')

def delete_task(conn, task_id):
    """Delete a task and record the deletion in history."""
    cursor = conn.cursor()
    
    # First check if the task exists
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        print(f"No task found with ID {task_id}.")
        return False
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    print(f"Task {task_id} deleted successfully.")
    return True

def list_tasks(conn, filter_status=None):
    """List all tasks, optionally filtered by status."""
    cursor = conn.cursor()
    
    query = "SELECT id, title, description, status, priority, created_at, updated_at FROM tasks"
    params = []
    
    if filter_status:
        query += " WHERE status = ?"
        params.append(filter_status)
    
    query += " ORDER BY id ASC"
    
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    
    if not tasks:
        print("No tasks found.")
        return
    
    print("\nCurrent Tasks:")
    print("-" * 100)
    print(f"{'ID':^5}|{'Title':^20}|{'Description':^30}|{'Status':^10}|{'Priority':^10}|{'Updated At':^20}")
    print("-" * 100)
    
    for task in tasks:
        task_id, title, description, status, priority, _, updated_at = task
        # Truncate description if too long
        description = (description[:27] + '...') if description and len(description) > 30 else description
        print(f"{task_id:^5}|{title[:20]:^20}|{description:^30}|{status:^10}|{priority:^10}|{updated_at:^20}")

def get_task_history(conn, task_id):
    """Retrieve the complete history of a task."""
    cursor = conn.cursor()
    cursor.execute('''
    SELECT 
        history_id, task_id, title, description, status, 
        priority, operation, changed_at
    FROM tasks_history
    WHERE task_id = ?
    ORDER BY changed_at ASC
    ''', (task_id,))
    
    history = cursor.fetchall()
    return history

def display_task_history(conn, task_id):
    """Display the history of a task in a readable format."""
    history = get_task_history(conn, task_id)
    
    if not history:
        print(f"No history found for task {task_id}.")
        return
    
    print(f"\nHistory for Task {task_id}:")
    print("-" * 100)
    print(f"{'History ID':^10}|{'Operation':^10}|{'Changed At':^25}|{'Title':^20}|{'Status':^10}|{'Priority':^10}")
    print("-" * 100)
    
    for record in history:
        history_id, _, title, _, status, priority, operation, changed_at = record
        title = title[:20] if title else ""
        print(f"{history_id:^10}|{operation:^10}|{changed_at:^25}|{title:^20}|{status:^10}|{priority:^10}")

def restore_task_version(conn, history_id):
    """Restore a task to a previous version from history."""
    cursor = conn.cursor()
    
    # Get the history record
    cursor.execute('''
    SELECT task_id, title, description, status, priority
    FROM tasks_history
    WHERE history_id = ?
    ''', (history_id,))
    
    history_record = cursor.fetchone()
    if not history_record:
        print(f"No history record found with ID {history_id}.")
        return False
    
    task_id, title, description, status, priority = history_record
    
    # Check if the task still exists
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        # Task was deleted, need to recreate it
        cursor.execute('''
        INSERT INTO tasks (id, title, description, status, priority, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (task_id, title, description, status, priority))
    else:
        # Task exists, update it
        cursor.execute('''
        UPDATE tasks 
        SET title = ?, description = ?, status = ?, priority = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''', (title, description, status, priority, task_id))
    
    conn.commit()
    print(f"Task {task_id} restored to version from history ID {history_id}.")
    return True

def display_menu():
    """Display the available commands to the user."""
    print("\n=== Task Management CLI with Version Control ===")
    print("Available commands:")
    print("  add         - Add a new task")
    print("  edit        - Edit an existing task")
    print("  complete    - Mark a task as complete")
    print("  list        - List all tasks")
    print("  pending     - List pending tasks")
    print("  completed   - List completed tasks")
    print("  delete      - Delete a task")
    print("  history     - View history of a task")
    print("  restore     - Restore a task to a previous version")
    print("  quit        - Exit the program")
    print("=============================================")

def main():
    """Main function to run the task management CLI."""
    print("Initializing Task Management CLI with Version Control...")
    conn = initialize_task_manager()
    
    print("Welcome to Task Management CLI Tool")
    
    while True:
        display_menu()
        command = input("Enter a command: ").lower().strip()
        
        if command == "add":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            priority = input("Enter priority (low/medium/high) [medium]: ") or "medium"
            add_task(conn, title, description, priority=priority)
            
        elif command == "edit":
            list_tasks(conn)
            try:
                task_id = int(input("Enter the ID of the task to edit: "))
                title = input("Enter new title (leave empty to keep current): ")
                description = input("Enter new description (leave empty to keep current): ")
                status = input("Enter new status (pending/in-progress/completed) (leave empty to keep current): ")
                priority = input("Enter new priority (low/medium/high) (leave empty to keep current): ")
                
                update_args = {}
                if title: update_args['title'] = title
                if description: update_args['description'] = description
                if status: update_args['status'] = status
                if priority: update_args['priority'] = priority
                
                update_task(conn, task_id, **update_args)
            except ValueError:
                print("Invalid ID. Please enter a number.")
            
        elif command == "complete":
            list_tasks(conn)
            try:
                task_id = int(input("Enter the ID of the task to mark as complete: "))
                complete_task(conn, task_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
            
        elif command == "list":
            list_tasks(conn)
            
        elif command == "pending":
            list_tasks(conn, filter_status="pending")
            
        elif command == "completed":
            list_tasks(conn, filter_status="completed")
            
        elif command == "delete":
            list_tasks(conn)
            try:
                task_id = int(input("Enter the ID of the task to delete: "))
                delete_task(conn, task_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
            
        elif command == "history":
            list_tasks(conn)
            try:
                task_id = int(input("Enter the ID of the task to view history: "))
                display_task_history(conn, task_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
            
        elif command == "restore":
            task_id = int(input("Enter the ID of the task to view history: "))
            display_task_history(conn, task_id)
            try:
                history_id = int(input("Enter the history ID to restore to: "))
                restore_task_version(conn, history_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
            
        elif command == "quit":
            print("Thank you for using Task Management CLI. Goodbye!")
            conn.close()
            break
            
        else:
            print(f"Unknown command: '{command}'. Please try again.")

if __name__ == "__main__":
    main()