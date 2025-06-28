import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
from tkinter.filedialog import asksaveasfilename
from datetime import datetime
from A1_09_4_q3 import initialize_task_manager, add_task, complete_task, delete_task, update_task
import csv

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f4f7")

        self.conn = initialize_task_manager()

        self.priority_var = tk.StringVar()
        self.sort_var = tk.StringVar(value="None")
        self.search_var = tk.StringVar()

        self.create_input_frame()
        self.create_tree_views()
        self.create_buttons()

        self.load_tasks()

    def create_input_frame(self):
        frame = tk.Frame(self.root, bg="#e3f2fd", pady=10)
        frame.pack(fill=tk.X, padx=10)

        tk.Label(frame, text="Title:", font=("Segoe UI", 10), bg="#e3f2fd").grid(row=0, column=0, padx=5)
        self.title_entry = tk.Entry(frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Description:", font=("Segoe UI", 10), bg="#e3f2fd").grid(row=0, column=2, padx=5)
        self.desc_entry = tk.Entry(frame, width=40)
        self.desc_entry.grid(row=0, column=3, padx=5)

        tk.Label(frame, text="Priority:", font=("Segoe UI", 10), bg="#e3f2fd").grid(row=0, column=4, padx=5)
        self.priority_dropdown = ttk.Combobox(frame, textvariable=self.priority_var, values=["low", "medium", "high"], state="readonly", width=10)
        self.priority_dropdown.set("medium")
        self.priority_dropdown.grid(row=0, column=5, padx=5)

        tk.Button(frame, text="Add Task", command=self.add_task_gui, bg="#1976d2", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5).grid(row=0, column=6, padx=10)

    def create_tree_views(self):
        search_frame = tk.Frame(self.root, bg="#f0f4f7")
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(search_frame, text="Search:", bg="#f0f4f7").pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.load_tasks).pack(side=tk.LEFT)
        tk.Button(search_frame, text="Export CSV", command=self.export_csv).pack(side=tk.RIGHT)

        self.task_tree = ttk.Treeview(self.root, columns=("ID", "Title", "Description", "Status", "Priority", "Updated", "Edit"), show='headings', selectmode="extended")
        for col in self.task_tree["columns"][:-1]:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=120)
        self.task_tree.heading("Edit", text="Edit")
        self.task_tree.column("Edit", width=80)
        self.task_tree.pack(fill=tk.BOTH, expand=True, pady=(10, 0), padx=10)

        tk.Label(self.root, text="Completed Tasks", bg="#f0f4f7", font=("Segoe UI", 10, "bold"), anchor="w").pack(fill=tk.X, padx=10, pady=(10, 0))
        self.completed_tree = ttk.Treeview(self.root, columns=("ID", "Title", "Description", "Status", "Priority", "Updated"), show='headings', selectmode="extended")
        for col in self.completed_tree["columns"]:
            self.completed_tree.heading(col, text=col)
            self.completed_tree.column(col, width=120)
        self.completed_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        for tree in (self.task_tree, self.completed_tree):
            tree.tag_configure('completed', foreground="green", font="SegoeUI 10 overstrike")
            tree.tag_configure('low', background="#e3f2fd")
            tree.tag_configure('medium', background="#fff9c4")
            tree.tag_configure('high', background="#ffcdd2")

        self.task_tree.bind("<ButtonRelease-1>", self.handle_edit_click)

    def create_buttons(self):
        frame = tk.Frame(self.root, bg="#f0f4f7")
        frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(frame, text="Mark as Complete", command=self.complete_task_gui, bg="#388e3c", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Delete Task", command=self.delete_task_gui, bg="#d32f2f", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Refresh", command=self.load_tasks, bg="#1976d2", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5).pack(side=tk.RIGHT, padx=5)

        tk.Label(frame, text="Sort by Priority:", bg="#f0f4f7", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=10)
        sort_dropdown = ttk.Combobox(frame, textvariable=self.sort_var, values=["None", "low", "medium", "high"], state="readonly", width=10)
        sort_dropdown.pack(side=tk.LEFT)
        sort_dropdown.bind("<<ComboboxSelected>>", lambda e: self.load_tasks())

    def get_selected_task_ids(self):
        trees = [self.task_tree, self.completed_tree]
        selected_ids = []
        for tree in trees:
            for item in tree.selection():
                selected_ids.append(tree.item(item)['values'][0])
        if not selected_ids:
            messagebox.showwarning("No Selection", "Please select at least one task.")
        return selected_ids

    def add_task_gui(self):
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        priority = self.priority_var.get()

        if not title:
            messagebox.showwarning("Input Error", "Task title is required.")
            return

        add_task(self.conn, title, desc, priority=priority)
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.priority_dropdown.set("medium")
        self.load_tasks()

    def complete_task_gui(self):
        task_ids = self.get_selected_task_ids()
        for task_id in task_ids:
            complete_task(self.conn, task_id)
        self.load_tasks()

    def delete_task_gui(self):
        task_ids = self.get_selected_task_ids()
        if task_ids:
            if messagebox.askyesno("Confirm Delete", "Delete selected task(s)?"):
                for task_id in task_ids:
                    delete_task(self.conn, task_id)
                self.load_tasks()

    def handle_edit_click(self, event):
        region = self.task_tree.identify("region", event.x, event.y)
        if region == "cell":
            col = self.task_tree.identify_column(event.x)
            if col == "#7":  # Edit column index
                item = self.task_tree.identify_row(event.y)
                if item:
                    values = self.task_tree.item(item)['values']
                    self.edit_task_details(values)

    def edit_task_details(self, values):
        task_id, title, desc, status, priority, updated = values[:6]

        new_title = askstring("Edit Task", "Title:", initialvalue=title)
        new_desc = askstring("Edit Task", "Description:", initialvalue=desc)
        new_priority = askstring("Edit Task", "Priority (low/medium/high):", initialvalue=priority)
        new_status = askstring("Edit Task", "Status (pending/completed):", initialvalue=status)

        if new_title and new_priority:
            update_task(
                self.conn, task_id,
                title=new_title,
                description=new_desc,
                status=new_status,
                priority=new_priority
            )
            self.load_tasks()

    def export_csv(self):
        path = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title, description, status, priority, updated_at FROM tasks")
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Title", "Description", "Status", "Priority", "Updated At"])
            for row in cursor.fetchall():
                writer.writerow(row)
        messagebox.showinfo("Export Complete", f"Tasks exported to {path}")

    def load_tasks(self):
        for tree in (self.task_tree, self.completed_tree):
            for item in tree.get_children():
                tree.delete(item)

        cursor = self.conn.cursor()
        base_query = "SELECT id, title, description, status, priority, updated_at FROM tasks"
        conditions = []
        params = []

        if self.sort_var.get() in ["low", "medium", "high"]:
            conditions.append("priority = ?")
            params.append(self.sort_var.get())

        search = self.search_var.get().strip().lower()
        if search:
            conditions.append("(LOWER(title) LIKE ? OR LOWER(description) LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        base_query += " ORDER BY id"

        for task in cursor.execute(base_query, params):
            task_id, title, desc, status, priority, updated_at = task
            tags = [priority]
            row = (task_id, title, desc, status, priority, updated_at, "Edit")
            if status == 'completed':
                tags.append('completed')
                self.completed_tree.insert('', 'end', values=row[:-1], tags=tags)
            else:
                self.task_tree.insert('', 'end', values=row, tags=tags)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
