# ✅ Task Management System (GUI + CLI)

A full-featured **Task Management System** built with Python that supports both a **Graphical User Interface (GUI)** and a **Command Line Interface (CLI)**.

This application lets users manage their tasks efficiently, with features like search, sort, edit, task history tracking, and CSV export.

---

## 📁 Project Structure

```
.
├── gui.py            # Tkinter-based GUI for task management
├── taskmanager.py    # CLI version with SQLite and version control
├── taskmanager.db    # SQLite database (auto-generated)
└── README.md         # Project documentation
```

---

## 🎯 Features

### 🖥 GUI Interface (gui.py)

- Add, update, delete, and mark tasks as complete
- Color-coded priority levels (Low = Blue, Medium = Yellow, High = Red)
- Strikethrough for completed tasks (in green)
- Search tasks by title or description
- Sort tasks by priority
- Separate views for pending and completed tasks
- Inline editing of task fields via form interface
- Export all tasks to CSV

### 💻 CLI Interface (taskmanager.py)

- Add, edit, complete, and delete tasks via command line
- View all tasks in a clean tabular format
- Full task version history via SQLite triggers
- Restore tasks from history (undo deletes or changes)
- Automatic audit trail of all operations

---

## 🚀 Getting Started

### ✅ Requirements

- Python 3.x
- No external dependencies (uses built-in libraries: tkinter, sqlite3, csv)

### ▶️ Run the GUI

```
python gui.py
```

### ▶️ Run the CLI

```
python taskmanager.py
```

---

## 🔄 Version Control with SQLite Triggers

Every time a task is:

- ✅ Added
- ✏️ Updated
- ❌ Deleted

A trigger logs the previous version to the tasks\_history table. This allows:

- Full audit trail of changes
- Restoring accidentally deleted or changed tasks
- Reliable rollback functionality

---

## 📤 Exporting Tasks

- Use the Export CSV button in the GUI to save all tasks to a .csv file
- Useful for backups, reports, or importing into other applications

---

## 📌 Example Use Cases

- ✅ Daily to‑do list and task manager
- 🧪 Track how tasks evolve over time
- 🔄 Undo mistakes like accidental deletes or edits
- 📋 Generate and share task reports

---

## 🛠️ Future Enhancements

- Add due dates with a calendar picker
- Popup-based edit forms for improved UX
- Notifications/reminders for upcoming deadlines
- Multi-user support with authentication

---

## 📜 License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute with attribution.

---

## 🙌 Acknowledgments

Built with ❤️ using Python, SQLite, and Tkinter — designed for simplicity, flexibility, and real-world usefulness.

