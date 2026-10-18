
from datetime import datetime
import os

print("Welcome to Personal Journal Manager!")
print()

# -------------------- Safe User Input --------------------

def int_input(message):
    while True:
        try:
            number = int(input(message))

            if number < 1 or number > 7:
                print("Please select option between 1 to 7.")
                print()
            else:
                return number

        except ValueError:
            print("Option value must be an integer!")
            print()


def text_input(message):
    while True:
        text = input(message).strip()

        if text == "":
            print("This field cannot be empty.")
            print()
        else:
            return text


# -------------------- File Setup --------------------

file_path = "File Operator/journal.txt"

# Create the folder if it does not exist.
os.makedirs("File Operator", exist_ok=True)

# Create the journal file on first use without deleting existing entries.
with open(file_path, "a", encoding="utf-8"):
    pass


# -------------------- Journal Manager --------------------

class JournalManager:

    def add_entry(self):

        entry = text_input("Enter your journal entry : \n")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # a mode: append a new entry.
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"[{timestamp}]\n")
            file.write(f"{entry}\n\n")

        print()
        print("Entry added successfully!")

    def view_entries(self):

        try:
            # r mode: read journal entries.
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()

            if file_content != "":
                print()
                print("Your Journal Entries:")
                print("--------------------------------")
                print(file_content)

            else:
                print("No journal entries found. Please add some entries.")

        except FileNotFoundError:
            print("Journal file does not exist. Please add a new entry.")

    def search_entry(self):

        try:
            # r mode: read journal entries.
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()

        except FileNotFoundError:
            print("Journal file does not exist. Please add a new entry.")
            return

        if file_content == "":
            print("No journal entries found. Please add some entries.")
            return

        matching_word = text_input("Enter a keyword or date (yyyy-mm-dd) to search : ")

        journal_entries = file_content.split("\n\n")

        print()
        print("Matching Entries:")
        print("--------------------------------")

        found = False

        for entries in journal_entries:

            if matching_word.lower() in entries.lower():

                print(entries)
                print()
                found = True

        if not found:
            print(f"No entries were found for the date or keyword : {matching_word}")

    def delete_entries(self):

        if not os.path.isfile(file_path):
            print("No journal entries to delete.")
            return

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        if content == "":
            print("No journal entries to delete.")
            return

        while True:

            confirmation = text_input("Are you sure you want to delete all entries (yes/no) : ").lower()

            if confirmation == "yes":

                # Delete the actual file instead of clearing its contents.
                os.remove(file_path)

                print("All journal entries have been deleted.")
                break

            elif confirmation == "no":
                print("Deletion cancelled! Your entries are safe!")
                break

            else:
                print("Invalid input! Please enter yes or no.")

    def x_mode(self):

        demo_path = "File Operator/x_mode_demo.txt"

        # x mode creates a new file only if it does not already exist.
        with open(demo_path, "x", encoding="utf-8") as file:
            file.write("This file demonstrates x mode.\n")

        print("File created successfully using x mode.")

    def w_mode(self):

        demo_path = "File Operator/w_mode_demo.txt"

        # w mode creates a file or overwrites its existing content.
        with open(demo_path, "w", encoding="utf-8") as file:
            file.write("This file demonstrates w mode.\n")

        print("Write mode demonstrated successfully.")


# -------------------- Main Menu --------------------

journal = JournalManager()

while True:

    print()
    print("Please select an option (1 to 7):")
    print()
    print("1. Add a New Entry")
    print("2. View All Entries")
    print("3. Search for an Entry")
    print("4. Delete All Entries")
    print("5. Demonstrate x Mode")
    print("6. Demonstrate w Mode")
    print("7. Exit")
    print()

    choice = int_input("Select an option: ")

    try:

        if choice == 1:

            journal.add_entry()

        elif choice == 2:

            journal.view_entries()

        elif choice == 3:

            journal.search_entry()

        elif choice == 4:

            journal.delete_entries()

        elif choice == 5:

            journal.x_mode()

        elif choice == 6:

            journal.w_mode()
        
        elif choice == 7:

            print()
            print("Thank you for using Personal Journal Manager. Goodbye!")
            break

    except FileExistsError:
        print("FileExistsError: The x-mode demo file already exists. It was not overwritten.")

    except FileNotFoundError:
        print("FileNotFoundError: The requested file was not found.")

    except PermissionError:
        print("PermissionError: Permission denied during file operation.")

    except OSError as e:
        print(f"OSError: {e}")

    print()
    print("--- Choose another option ---")
    print()
