# Task Management System (GUI & CLI)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Database-SQLite3-green.svg" alt="Database">
  <img src="https://img.shields.io/badge/License-MIT-purple.svg" alt="License">
</p>

A full-featured, object-oriented Task Management System built with Python that supports both a Graphical User Interface (GUI) and a Command Line Interface (CLI).

This application allows users to manage their tasks efficiently, with advanced features like search, dynamic sorting, in-line editing, comprehensive task history tracking, and CSV export. The underlying architecture is cleanly abstracted into a robust database manager, ensuring zero side-effects across the interfaces.

---

## Features

### Graphical Interface (`gui.py`)
- **Intuitive Dashboard:** Add, update, delete, and mark tasks as complete with a click.
- **Color-Coded Priorities:** Easily distinguish tasks (Low = Blue, Medium = Yellow, High = Red).
- **Visual Cues:** Completed tasks feature a clear strikethrough.
- **Advanced Filtering:** Real-time search and priority-based sorting.
- **Export Capabilities:** Export all tasks directly to a CSV file for backups or reports.

### Command Line Interface (`taskmanager.py`)
- **Fast & Lightweight:** Add, edit, complete, and delete tasks directly from your terminal.
- **Tabular Data:** View tasks in a clean, perfectly formatted terminal table.
- **Full Version Control:** Leveraging SQLite triggers, every change is audited. 
- **Time Travel:** View a task's entire history and restore it to any previous state to undo accidental edits or deletions.

---

## File Structure

```text
Task-Management-Tool/
├── gui.py              # Graphical User Interface entry point and main window class
├── taskmanager.py      # Core database logic (TaskManagerDB), CLI (TaskCLI), and script entry point
├── taskmanager.db      # SQLite database file (auto-generated upon running the application)
└── readme.md           # Project documentation
```

---

## Getting Started

### Prerequisites
- Python 3.x
- No external dependencies required. (Built purely on standard libraries: `tkinter`, `sqlite3`, `csv`)

### Installation
1. Clone the repository to your local machine.
2. Navigate into the project directory:
```bash
cd Task-Management-Tool
```

---

## How to Use

### Running the Graphical Interface
To launch the graphical application, run:
```bash
python gui.py
```
- **Adding Tasks:** Use the top bar to input a Title, Description, and Priority, then click "Add Task".
- **Editing Tasks:** Click the "Edit" column of any active task to modify its details.
- **Completing/Deleting:** Select one or multiple tasks and use the buttons on the bottom left.
- **Exporting:** Click "Export CSV" to save the visible tasks to your local file system.

### Running the Command Line Interface
To launch the interactive terminal application, run:
```bash
python taskmanager.py
```
Upon launching, you will be presented with a prompt:
```
=== Task Management CLI with Version Control ===
Available commands:
  add         - Add a new task
  edit        - Edit an existing task
  complete    - Mark a task as complete
  list        - List all tasks
  pending     - List pending tasks
  completed   - List completed tasks
  delete      - Delete a task
  history     - View history of a task
  restore     - Restore a task to a previous version
  quit        - Exit the program
=============================================
Enter a command: 
```
Simply type the command you wish to execute (e.g., `add`, `list`, `complete`) and follow the on-screen prompts.

---

## System Architecture

The codebase follows strict Object-Oriented Programming (OOP) principles:
- **`TaskManagerDB`:** A dedicated data access layer encapsulating all SQLite operations, ensuring a strict boundary between database logic and input/output.
- **`TaskCLI`:** Handles terminal inputs and tabular outputs cleanly.
- **`TaskManagerGUI`:** A structured `tkinter` class utilizing the shared `TaskManagerDB` for seamless data synchronization.

---

## Version Control with SQLite Triggers

The system automatically audits data mutations at the database level. Every time a task is:
- **Added**
- **Updated**
- **Deleted**

A native SQLite trigger logs the previous state to the `tasks_history` table. This provides a bulletproof audit trail and reliable rollback functionality without cluttering the application logic.

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute with attribution.
