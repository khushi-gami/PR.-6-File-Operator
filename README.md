khushi-gami-PR.-6-File-Operator (VIDEO)

# PR.-6-File-Operator

# 📝 Personal Journal Manager

## 📌 Project Overview
Personal Journal Manager is a Python-based command-line application that allows users to add, view, search, and delete journal entries. Each entry is automatically saved with its date and time in a text file.

## ✨ Features
- **Add Entry:** Save a journal entry with an automatic timestamp.
- **View Entries:** Display all previously saved entries.
- **Search Entries:** Find entries using a keyword or date.
- **Delete Entries:** Delete all journal entries after confirmation.
- **Input Validation:** Prevent empty entries and invalid menu options.
- **Exception Handling:** Handle file-related errors safely.
- **Persistent Storage:** Keep journal entries saved in a text file.

## 🛠️ Python Concepts Used

### 1. Importing Modules
- `datetime`: Gets the current date and time for each journal entry.
- `os`: Uses `os.path.isfile()` to check whether the journal file exists before reading, searching, or deleting entries.

### 2. Functions
- `int_input()`: Accepts an integer menu option and validates that it is between 1 and 5. A `while` loop repeats the prompt if the input is invalid.
- `text_input()`: Accepts text, removes extra spaces using `.strip()`, and prevents empty input.

### 3. Object-Oriented Programming (OOP)
The `JournalManager` class groups journal-related operations into separate methods:
- `add_entry()`
- `view_entries()`
- `search_entry()`
- `delete_entries()`

An object, `journal = JournalManager()`, is created to call these methods.

### 4. Date and Time
`datetime.now()` gets the current date and time, while `strftime("%Y-%m-%d %H:%M:%S")` formats it into a readable timestamp.

### 5. File Handling
The project uses three file modes:
- **`a` (Append):** Adds new entries without removing existing content. Creates the file if it does not exist, provided the parent folder exists.
- **`r` (Read):** Reads saved entries for viewing and searching.
- **`w` (Write):** Clears the file when the user confirms deletion.

The `with open()` statement automatically closes the file after the operation.

### 6. Searching Logic
The file content is divided into individual entries using `split("\n\n")`. The program loops through these entries and checks whether the search keyword appears in each entry.

Using `.lower()` makes the search case-insensitive. A `found` flag tracks whether a matching entry was found.

### 7. Input Validation
- `int()` converts menu input into an integer.
- `if` conditions restrict menu choices to 1–5.
- `.strip()` and an empty-string check prevent blank journal entries.
- A confirmation loop accepts only `yes` or `no` before deleting entries.

### 8. Exception Handling
`try` and `except` blocks handle errors without abruptly stopping the menu:
- `ValueError`: Handles invalid integer input.
- `FileNotFoundError`: Handles a missing journal file.
- `PermissionError`: Handles permission-related file access problems.
- `OSError`: Handles other operating-system and file-related errors.

Specific file exceptions are caught before the general `OSError`.

### 9. Loops and Conditional Statements
- `while True`: Keeps the application running until the user chooses Exit.
- `for` loop: Checks each journal entry during searching.
- `if`, `elif`, and `else`: Control menu selection, input validation, search results, and deletion confirmation.
- `break`: Exits a loop when the user chooses to exit or finishes the deletion confirmation.

## ▶️ How to Run
1. Install Python 3.
2. Save the code in a Python file.
3. Ensure the `File Operator` folder exists in the working directory.
4. Open a terminal in the project directory.
5. Run the program:

   `python your_filename.py`

   Replace `your_filename.py` with your actual Python filename.

## 📂 Project Structure

```text
Personal-Journal-Manager/
├── your_filename.py
└── File Operator/
    └── journal.txt
```

The `journal.txt` file stores the journal entries. The program does not automatically create the parent folder.

## 🎯 Learning Outcomes
Through this project, I practised Python functions, OOP, loops, conditional statements, string methods, date-time formatting, file handling, input validation, and exception handling by building a practical command-line application.

## ⚠️ Important Note
The Delete All Entries option clears all saved journal entries after confirmation. The application currently deletes all entries together rather than deleting a single selected entry.

