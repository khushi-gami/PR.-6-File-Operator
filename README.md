PR.-6-File-Operator (VIDEO)
https://drive.google.com/file/d/1dXW875JJdIB4uowmV82xpyw92A4U6FsN/view?usp=sharing

# PR.-6-File-Operator (Personal Journal Manager)

## 📌 Project Overview

Personal Journal Manager is a Python-based command-line application that allows users to create, view, search, and delete journal entries. Each journal entry is automatically saved with the current date and time in a text file.

The application uses Python file handling, object-oriented programming, input validation, and exception handling to provide a simple and reliable journaling experience.

The program automatically creates the required folder and journal file on first use, so users do not need to create them manually.

## ✨ Features

- **Add Entry:** Save a journal entry with an automatically generated timestamp.
- **View Entries:** Display all previously saved journal entries.
- **Search Entries:** Search journal entries using a keyword or date.
- **Delete All Entries:** Delete the journal file after user confirmation.
- **Input Validation:** Prevent empty journal entries and invalid menu options.
- **Exception Handling:** Handle file-related errors safely without unexpectedly terminating the application.
- **Automatic File Creation:** Create the required directory and journal file if they do not exist.
- **Persistent Storage:** Preserve journal entries between program runs unless the user deletes them.
- **File Mode Demonstrations:** Demonstrate Python's `r`, `w`, `a`, and `x` file modes.

## 🛠️ Python Concepts Used

### 1. Importing Modules

The project uses the following modules:

- **`datetime`:** Retrieves the current date and time for each journal entry.
- **`os`:** Creates the required directory, checks whether the journal file exists, and deletes the file when requested.

### 2. Functions and Input Validation

**`int_input(message)`**

- Accepts the user's menu selection.
- Converts the input into an integer using `int()`.
- Allows only menu options from 1 to 7.
- Uses a `while` loop to repeat the prompt when the input is invalid.
- Handles invalid integer input using `ValueError`.

**`text_input(message)`**

- Accepts text from the user.
- Uses `.strip()` to remove leading and trailing whitespace.
- Prevents the user from submitting an empty or whitespace-only entry.
- Repeats the prompt until valid text is provided.

### 3. Object-Oriented Programming (OOP)

The `JournalManager` class groups the journal operations into separate methods:

- `add_entry()` — adds a new journal entry.
- `view_entries()` — displays saved entries.
- `search_entry()` — searches entries using a keyword or date.
- `delete_entries()` — deletes all entries by removing the journal file after confirmation.
- `x_mode()` — demonstrates exclusive file creation.
- `w_mode()` — demonstrates write mode.

An object is created using:

`journal = JournalManager()`

The program uses this object to call the required methods.

### 4. Date and Time

The project uses Python's `datetime` module to attach a timestamp to each entry.

- `datetime.now()` retrieves the current local date and time.
- `strftime("%Y-%m-%d %H:%M:%S")` formats the timestamp into a readable string.

Example:

`[2026-10-18 10:30:00]`

This timestamp helps users identify when each journal entry was created.

### 5. File and Directory Management

The project automatically creates the required directory and journal file when the program starts.

**Creating the directory:**

`os.makedirs("File Operator", exist_ok=True)`

- Creates the `File Operator` directory if it does not exist.
- Does not raise an error merely because the directory already exists.

**Creating the journal file:**

`with open(file_path, "a", encoding="utf-8"):`

- Creates `journal.txt` if it does not exist, provided the parent directory is available.
- Preserves existing journal entries.
- Avoids accidentally clearing previously saved data during startup.

### 6. Python File Modes

The project demonstrates all four required file modes.

| Mode | Purpose | Behaviour in this project |
|---|---|---|
| `r` — Read | Read existing file content | Used to view and search journal entries. |
| `w` — Write | Write content to a file | Demonstrated using a separate `w_mode_demo.txt` file. Creates the file if missing and overwrites existing content. |
| `a` — Append | Add content to the end of a file | Used to save new journal entries without removing previous entries. Also creates the journal file if missing. |
| `x` — Exclusive creation | Create a new file only if it does not exist | Demonstrated using a separate `x_mode_demo.txt` file. Raises `FileExistsError` if the file already exists. |

The `with open()` statement automatically closes the file when the file operation is complete.

**Important:** The `w` and `x` demonstrations use separate files so that they do not overwrite or interfere with the user's journal entries.

### 7. Searching Logic

The search feature allows users to search for entries using a keyword or date.

- `file.read()` reads the complete journal file.
- `split("\n\n")` separates entries using the blank line between them.
- A `for` loop checks each entry.
- `.lower()` makes the search case-insensitive.
- A Boolean variable named `found` tracks whether a matching entry was found.

If a match exists, the matching entry is displayed. Otherwise, the program informs the user that no matching entries were found.

### 8. Deleting Journal Entries

The Delete All Entries feature removes the actual journal file instead of merely clearing its contents.

The process is as follows:

1. `os.path.isfile(file_path)` checks whether the journal file exists.
2. The program reads the file to check whether it contains entries.
3. If the file is missing or empty, the program displays an appropriate message.
4. The program asks the user to confirm the deletion by entering `yes` or `no`.
5. If the user enters `yes`, `os.remove(file_path)` deletes the journal file.
6. If the user enters `no`, the deletion is cancelled.
7. Invalid confirmation input causes the program to ask again.

The startup setup recreates the journal file on the next program launch if it has been deleted.

**Note:** This feature deletes all journal entries together. It does not delete an individual selected entry.

### 9. Exception Handling

The project uses `try` and `except` blocks to handle errors safely.

| Exception | Purpose |
|---|---|
| `ValueError` | Handles invalid integer input in `int_input()`. |
| `FileNotFoundError` | Handles cases where a requested file is missing. |
| `FileExistsError` | Handles attempts to create an existing file using `x` mode. |
| `PermissionError` | Handles file operations denied because of insufficient permissions. |
| `OSError` | Handles other operating-system and file-related errors. |

Specific file exceptions are handled before the more general `OSError` exception.

The `view_entries()` and `search_entry()` methods also handle a missing journal file locally. The main menu provides additional protection for file-related errors that are not handled inside individual methods.

### 10. Loops and Conditional Statements

- **`while True`:** Keeps the application running until the user chooses Exit.
- **`for` loop:** Checks journal entries during searching.
- **`if`, `elif`, and `else`:** Control menu selection, validation, search results, and deletion confirmation.
- **`break`:** Exits a loop when the user chooses Exit or completes the deletion confirmation.
- **`return`:** Stops a method early when no file or journal entries are available.

## 📂 Project Structure

```text
File Operator/
├── file-operator.py          # Main command-line program
├── file-operator-ui.py       # GUI implementation
├── journal.txt               # Journal data file, created automatically
├── x_mode_demo.txt           # Created when x-mode demonstration succeeds
└── w_mode_demo.txt           # Created or overwritten by w-mode demonstration
```

The journal file and demonstration files are created when required. The `File Operator` directory is created automatically if it does not already exist.

**Note:** The demonstration files may not exist until the corresponding menu options are selected.

## 🎯 Learning Outcomes

By completing this project, I practised:

- Python functions and reusable input-validation logic.
- Object-oriented programming using classes and methods.
- File handling using `r`, `w`, `a`, and `x` modes.
- Automatic directory and file creation.
- Reading, appending, overwriting, and deleting files.
- Date and time formatting with the `datetime` module.
- Searching text using string methods and loops.
- Exception handling and error prevention.
- Conditional statements, loops, and user confirmation.
- Building a practical command-line application with persistent storage.

## ⚠️ Important Notes

- The program automatically creates the parent directory and journal file on startup, if it's not exist.
- The `a` mode preserves existing journal entries when adding new entries.
- The `w` mode demonstration overwrites the content of its separate demonstration file.
- The `x` mode demonstration creates a new file only if it does not already exist.
- Selecting Delete All Entries removes the actual `journal.txt` file after confirmation.
- The journal file is recreated automatically when the application starts again.
- The application deletes all entries together rather than deleting a single selected entry.
