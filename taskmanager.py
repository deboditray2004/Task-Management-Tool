import sqlite3
import os
from datetime import datetime

class TaskManagerDB:
    def __init__(self, db_path='taskmanager.db'):
        self.conn = sqlite3.connect(db_path)
        self._initialize_db()

    def _initialize_db(self):
        """Create the database and setup triggers."""
        cursor = self.conn.cursor()
        
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
        
        # Setup Triggers
        triggers = [
            ("tasks_insert_trigger", "AFTER INSERT", "NEW", "INSERT"),
            ("tasks_update_trigger", "AFTER UPDATE", "NEW", "UPDATE"),
            ("tasks_delete_trigger", "AFTER DELETE", "OLD", "DELETE")
        ]
        
        for trig_name, trig_event, trig_var, op in triggers:
            cursor.execute(f'''
            CREATE TRIGGER IF NOT EXISTS {trig_name}
            {trig_event} ON tasks
            BEGIN
                INSERT INTO tasks_history (
                    task_id, title, description, status, priority, 
                    operation, changed_at
                )
                VALUES (
                    {trig_var}.id, {trig_var}.title, {trig_var}.description, {trig_var}.status, 
                    {trig_var}.priority, '{op}', CURRENT_TIMESTAMP
                );
            END;
            ''')
            
        self.conn.commit()

    def check_task_exists(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        return cursor.fetchone() is not None

    def add_task(self, title, description, status='pending', priority='medium'):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO tasks (title, description, status, priority, updated_at)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (title, description, status, priority))
        self.conn.commit()
        return cursor.lastrowid

    def update_task(self, task_id, title=None, description=None, status=None, priority=None):
        if not self.check_task_exists(task_id):
            return False
            
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
            return False
            
        update_parts.append("updated_at = CURRENT_TIMESTAMP")
        query = f"UPDATE tasks SET {', '.join(update_parts)} WHERE id = ?"
        values.append(task_id)
        
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        return True

    def complete_task(self, task_id):
        return self.update_task(task_id, status='completed')

    def delete_task(self, task_id):
        if not self.check_task_exists(task_id):
            return False
            
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        return True

    def list_tasks(self, filter_status=None, filter_priority=None, search_query=None):
        cursor = self.conn.cursor()
        query = "SELECT id, title, description, status, priority, created_at, updated_at FROM tasks"
        params = []
        conditions = []
        
        if filter_status:
            conditions.append("status = ?")
            params.append(filter_status)
        if filter_priority and filter_priority != "None":
            conditions.append("priority = ?")
            params.append(filter_priority)
        if search_query:
            conditions.append("(LOWER(title) LIKE ? OR LOWER(description) LIKE ?)")
            params.extend([f"%{search_query.lower()}%", f"%{search_query.lower()}%"])
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += " ORDER BY id ASC"
        cursor.execute(query, params)
        return cursor.fetchall()

    def get_task_history(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT history_id, task_id, title, description, status, priority, operation, changed_at
        FROM tasks_history WHERE task_id = ? ORDER BY changed_at ASC
        ''', (task_id,))
        return cursor.fetchall()

    def restore_task_version(self, history_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT task_id, title, description, status, priority
        FROM tasks_history WHERE history_id = ?
        ''', (history_id,))
        record = cursor.fetchone()
        
        if not record:
            return False, None
            
        task_id, title, description, status, priority = record
        
        if not self.check_task_exists(task_id):
            cursor.execute('''
            INSERT INTO tasks (id, title, description, status, priority, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (task_id, title, description, status, priority))
        else:
            cursor.execute('''
            UPDATE tasks SET title = ?, description = ?, status = ?, priority = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', (title, description, status, priority, task_id))
            
        self.conn.commit()
        return True, task_id

    def close(self):
        self.conn.close()

class TaskCLI:
    def __init__(self):
        self.db = TaskManagerDB()

    def display_menu(self):
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

    def print_tasks(self, tasks):
        if not tasks:
            print("No tasks found.")
            return
            
        print("\nCurrent Tasks:")
        print("-" * 100)
        print(f"{'ID':^5}|{'Title':^20}|{'Description':^30}|{'Status':^10}|{'Priority':^10}|{'Updated At':^20}")
        print("-" * 100)
        
        for task in tasks:
            task_id, title, description, status, priority, _, updated_at = task
            desc = (description[:27] + '...') if description and len(description) > 30 else (description or "")
            print(f"{task_id:^5}|{title[:20]:^20}|{desc:^30}|{status:^10}|{priority:^10}|{updated_at:^20}")

    def run(self):
        print("Initializing Task Management CLI with Version Control...")
        print("Welcome to Task Management CLI Tool")
        
        while True:
            self.display_menu()
            command = input("Enter a command: ").lower().strip()
            
            if command == "add":
                title = input("Enter task title: ")
                desc = input("Enter task description: ")
                priority = input("Enter priority (low/medium/high) [medium]: ") or "medium"
                tid = self.db.add_task(title, desc, priority=priority)
                print(f"Task {tid} added successfully.")
                
            elif command == "edit":
                self.print_tasks(self.db.list_tasks())
                try:
                    task_id = int(input("Enter the ID of the task to edit: "))
                    title = input("Enter new title (leave empty to keep current): ")
                    desc = input("Enter new description (leave empty to keep current): ")
                    status = input("Enter new status (pending/completed) (leave empty to keep current): ")
                    priority = input("Enter new priority (low/medium/high) (leave empty to keep current): ")
                    
                    update_args = {}
                    if title: update_args['title'] = title
                    if desc: update_args['description'] = desc
                    if status: update_args['status'] = status
                    if priority: update_args['priority'] = priority
                    
                    if self.db.update_task(task_id, **update_args):
                        print(f"Task {task_id} updated successfully.")
                    else:
                        print(f"Failed to update task {task_id}.")
                except ValueError:
                    print("Invalid ID.")
                
            elif command == "complete":
                self.print_tasks(self.db.list_tasks(filter_status="pending"))
                try:
                    task_id = int(input("Enter the ID of the task to complete: "))
                    if self.db.complete_task(task_id):
                        print(f"Task {task_id} marked as completed.")
                    else:
                        print(f"Failed to complete task {task_id}.")
                except ValueError:
                    print("Invalid ID.")
                    
            elif command in ["list", "pending", "completed"]:
                status_filter = None
                if command == "pending": status_filter = "pending"
                if command == "completed": status_filter = "completed"
                self.print_tasks(self.db.list_tasks(filter_status=status_filter))
                
            elif command == "delete":
                self.print_tasks(self.db.list_tasks())
                try:
                    task_id = int(input("Enter the ID of the task to delete: "))
                    if self.db.delete_task(task_id):
                        print(f"Task {task_id} deleted successfully.")
                    else:
                        print(f"Task {task_id} not found.")
                except ValueError:
                    print("Invalid ID.")
                    
            elif command == "history":
                try:
                    task_id = int(input("Enter the ID of the task to view history: "))
                    history = self.db.get_task_history(task_id)
                    if not history:
                        print(f"No history found for task {task_id}.")
                    else:
                        print(f"\nHistory for Task {task_id}:")
                        print("-" * 100)
                        print(f"{'Hist ID':^10}|{'Operation':^10}|{'Changed At':^25}|{'Title':^20}|{'Status':^10}|{'Priority':^10}")
                        print("-" * 100)
                        for rec in history:
                            hid, _, title, _, status, priority, op, changed_at = rec
                            t = title[:20] if title else ""
                            print(f"{hid:^10}|{op:^10}|{changed_at:^25}|{t:^20}|{status:^10}|{priority:^10}")
                except ValueError:
                    print("Invalid ID.")
                    
            elif command == "restore":
                try:
                    history_id = int(input("Enter the history ID to restore to: "))
                    success, task_id = self.db.restore_task_version(history_id)
                    if success:
                        print(f"Task {task_id} restored successfully to history version {history_id}.")
                    else:
                        print(f"History ID {history_id} not found.")
                except ValueError:
                    print("Invalid ID.")
                    
            elif command == "quit":
                print("Goodbye!")
                self.db.close()
                break
            else:
                print("Unknown command.")

def main():
    cli = TaskCLI()
    cli.run()

if __name__ == "__main__":
    main()