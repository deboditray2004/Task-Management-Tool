# ✅ Task Management System (GUI + CLI)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Database-SQLite3-green.svg" alt="Database">
  <img src="https://img.shields.io/badge/License-MIT-purple.svg" alt="License">
</p>

A full-featured, object-oriented **Task Management System** built with Python that supports both a **Graphical User Interface (GUI)** and a **Command Line Interface (CLI)**.

This application allows users to manage their tasks efficiently, with advanced features like search, dynamic sorting, in-line editing, comprehensive task history tracking, and CSV export. The underlying architecture is cleanly abstracted into a robust database manager, ensuring zero side-effects across the interfaces.

---

## 🎯 Features

### 🖥 Graphical Interface (`gui.py`)
- **Intuitive Dashboard:** Add, update, delete, and mark tasks as complete with a click.
- **Color-Coded Priorities:** Easily distinguish tasks (Low = Blue, Medium = Yellow, High = Red).
- **Visual Cues:** Completed tasks feature a satisfying green strikethrough.
- **Advanced Filtering:** Real-time search and priority-based sorting.
- **Export Capabilities:** Export all tasks directly to a CSV file for backups or reports.

### 💻 Command Line Interface (`taskmanager.py`)
- **Fast & Lightweight:** Add, edit, complete, and delete tasks directly from your terminal.
- **Tabular Data:** View tasks in a clean, perfectly formatted terminal table.
- **Full Version Control:** Leveraging SQLite triggers, every change is audited. 
- **Time Travel:** View a task's entire history and restore it to any previous state to undo accidental edits or deletions.

---

## 🚀 Getting Started

### ✅ Prerequisites
- Python 3.x
- No external dependencies required! (Built purely on standard libraries: `tkinter`, `sqlite3`, `csv`)

### ▶️ Run the GUI
To launch the graphical application, run:
```bash
python gui.py
```

### ▶️ Run the CLI
To launch the interactive terminal application, run:
```bash
python taskmanager.py
```

---

## 🏗 System Architecture

The codebase follows clean Object-Oriented Programming (OOP) principles:
- **`TaskManagerDB`:** A dedicated data access layer encapsulating all SQLite operations, ensuring a strict boundary between database logic and input/output.
- **`TaskCLI`:** Handles terminal inputs and tabular outputs cleanly.
- **`TaskManagerGUI`:** A structured `tkinter` class utilizing the shared `TaskManagerDB` for seamless data synchronization.

---

## 🔄 Version Control with SQLite Triggers

The system automatically audits data mutations at the database level. Every time a task is:
- ✅ **Added**
- ✏️ **Updated**
- ❌ **Deleted**

A native SQLite trigger logs the previous state to the `tasks_history` table. This provides a bulletproof audit trail and reliable rollback functionality without cluttering the application logic.

---

## 📜 License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute with attribution.

---

<p align="center">
  <i>Built with ❤️ using Python, SQLite, and Tkinter — designed for simplicity, flexibility, and real-world usefulness.</i>
</p>
