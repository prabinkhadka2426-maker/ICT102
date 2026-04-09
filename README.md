# 📚 Library Book Manager — ICT102 Mini Project

A desktop application for managing a library's book collection, built with Python and Tkinter. It supports adding books, borrowing, returning, searching, and viewing transaction history — all through a clean graphical interface.

---

## 🖥️ Screenshots

> Dashboard view with stat cards, recent books, and quick-action buttons.

---

## ✨ Features

- **Dashboard** — Live stats (total, available, borrowed) and recent books at a glance
- **Add Book** — Add books with title, author, genre, and year (with duplicate detection)
- **All Books** — View and filter the full collection by genre or availability
- **Borrow Book** — Select an available book and log it against a borrower's name
- **Return Book** — Return borrowed books with a single click
- **Search** — Search across title, author, and genre
- **Transaction History** — Full log of all borrow and return actions

---

## 🛠️ Requirements

| Requirement | Details |
|---|---|
| Python | 3.10 or higher (for `match/case` support) |
| Tkinter | Included with standard Python installation |
| External libraries | **None** — no `pip install` needed |

> **Note:** Python 3.10+ is required because the code uses the `match/case` statement introduced in that version.

---

## 🚀 How to Run

### Step 1 — Check your Python version

Open a terminal (Command Prompt / PowerShell on Windows, Terminal on Mac/Linux) and run:

```bash
python --version
```

Make sure it shows **Python 3.10 or higher**. If not, download the latest Python from [python.org](https://www.python.org/downloads/).

---

### Step 2 — Clone or Download the Repository

**Option A — Clone with Git:**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

**Option B — Download ZIP:**
1. Click the green **Code** button on GitHub
2. Select **Download ZIP**
3. Extract the folder and open it

---

### Step 3 — Run the Application

```bash
python library_manager.py
```

> Replace `library_manager.py` with the actual filename if it is different.

The application window will open immediately — no additional setup required.

---

## 📁 Project Structure

```
your-repo-name/
│
├── library_manager.py   # Main application file (all code is here)
└── README.md            # This file
```

---

## 📖 How to Use

| Page | What to Do |
|---|---|
| **Dashboard** | Open the app — stats and recent books load automatically |
| **Add Book** | Click **Add Book** in the sidebar → fill in the form → click **➕ Add Book** |
| **All Books** | Click **All Books** → use the filter dropdowns → click **Apply** |
| **Borrow Book** | Click **Borrow Book** → select a book from the list → enter your name → click **Confirm Borrow** |
| **Return Book** | Click **Return Book** → select the borrowed book → click **Confirm Return** |
| **Search** | Click **Search** → type a keyword → press Enter or click **🔍 Search** |
| **History** | Click **History** to see all borrow and return records |

---

## 🧠 Programming Concepts Demonstrated (ICT102)

This project was built to demonstrate the following core programming concepts:

- **`if / elif / else`** — Input validation in `add_book()`, `borrow_book()`, `return_book()`
- **`for` loop** — Iterating over the book list for filtering, searching, and duplicate checking
- **`while` loop** — Used in `borrow_book()` to locate a book by ID
- **`match / case`** — Assigning genre codes (e.g. `FIC`, `SCI`) when adding a book
- **Functions** — Modular design: `add_book()`, `view_books()`, `borrow_book()`, `return_book()`, `search_books()`, `get_statistics()`
- **Data types** — Strings, integers, booleans, lists, and dictionaries
- **OOP (Classes)** — The entire GUI is encapsulated in the `LibraryApp` class

---

## ⚠️ Troubleshooting

**`SyntaxError: invalid syntax` near `match`**
→ Your Python version is below 3.10. Update Python from [python.org](https://www.python.org/downloads/).

**`ModuleNotFoundError: No module named 'tkinter'`**
→ On Linux, install Tkinter manually:
```bash
sudo apt-get install python3-tk
```

**The window does not appear**
→ Make sure you are running the file with `python` (not opening it in a text editor). On some systems, use `python3` instead:
```bash
python3 library_manager.py
```

---

## 👤 Author

- **Course:** ICT102
- **Project:** Mini Project — Library Book Manager
- **Language:** Python 3.10+
- **GUI Library:** Tkinter (standard library)