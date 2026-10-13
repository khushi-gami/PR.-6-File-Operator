
from datetime import datetime
import os

print("Welcome to Personal Journal Manager !")

print()

# for safe user input

def int_input(message):
    while True:
        try:
            number = int(input(message))
            if number < 1 or number > 5:
                print("Please select option between 1 to 5.")
                print()
            else:
                return number
        except ValueError:
            print("option value must be an interger !")
            print()
            
def text_input(message):
    while True:
        text = input(message).strip()
        if text == "":
            print("This field cannot be empty.")
            print()
        else:
            return text
        

file_path = "File Operator/journal.txt"     
          
class JournalManager:
        
    def add_entry(self):
 
        entry = text_input("Enter your journal entry : \n")
        now = datetime.now()

        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            
        with open(f"{file_path}","a") as file:
            file.write(f"[{timestamp}] \n ")
            file.write(f"{entry} \n\n")
                    
            print()
            print("Entry added successfully!")
                    
    def view_entries(self):
        
        if os.path.isfile(f"{file_path}"):
            
            with open(f"{file_path}","r") as file:
                file_content = file.read()
                
            if file_content != "":
                        
                print()
                print("Your Journal Entries : ")
                print("--------------------------------")
                print(file_content)
                
            else:
                print("No journal entries found. Please add some entries to view entries details.")
                    
        else:
            raise FileNotFoundError("The journal file does not exist.")
                
    
    def search_entry(self):
        
        if os.path.isfile(f"{file_path}"):
            
            with open(f"{file_path}","r") as file:
                file_content = file.read()
                
            if file_content != "":
                        
                matching_word = text_input("Enter a keyword or date(yyyy-mm-dd) to search : ")
                journal_entries = file_content.split("\n\n")
                
                print()
                print("Matching Entries : ")
                print("--------------------------------")
                
                found = False
                
                for entries in journal_entries:
                    
                    if matching_word.lower() in entries.lower():
                        
                        print(f"{entries}\n")
                        
                        found = True
                        
                if not found:      
                    print(f"No Entries were found for the date or keyword : {matching_word}")
                
            else:
                print("No journal entries found. Please add some entries to search.")
                    
        else:
            raise FileNotFoundError("The journal file does not exist.")
    
    def delete_entries(self):
        
        if os.path.isfile(file_path):

            with open(file_path, "r") as file:
                content = file.read()

            if content != "":

                while True:
                    delete_file_confirmation = text_input("Are you sure you want to delete all entries (yes/no): ").lower()

                    if delete_file_confirmation == "yes":

                        with open(file_path, "w") as file:
                            pass

                        print("All journal entries have been deleted.")
                        break

                    elif delete_file_confirmation == "no":
                        print("Deletion cancelled! Your entries are safe!")
                        break

                    else:
                        print("Invalid input! Please enter yes or no.")

            else:
                print("No journal entries to delete. Please add some entries to delete.")

        else:
            raise FileNotFoundError("The journal file does not exist.")

    

journal = JournalManager()


while True:
    
    print("Please select an option (1 to 5): ")
    print()
    print("1. Add a New Entry")
    print("2. View All Entries")
    print("3. Search for an Entry")
    print("4. Delete All Entries")
    print("5. Exit")
    
    print()
    
    choice = int_input("Select an option : ")
    
    if choice == 1:
        
        try:
            journal.add_entry()
        except PermissionError:
            print("PermissionError : Permission denied while writing to the journal file.")
        except OSError as e:
            print(f"OSError : {e}")
            
    elif choice == 2:
        
        try:
            journal.view_entries()
        except FileNotFoundError as e:
            print(f"FileNotFoundError : {e}")
        except PermissionError:
            print("PermissionError : Permission denied while reading the journal file.")
        except OSError as e:
            print(f"OSError : {e}")
            
    elif choice == 3:
        
        try:
            journal.search_entry()
        except FileNotFoundError as e:
            print(f"FileNotFoundError : {e}")
        except PermissionError:
            print("PermissionError : Permission denied while searching the journal file.")
        except OSError as e:
            print(f"OSError : {e}")
        
    elif choice == 4:
        
        try:
            journal.delete_entries()
        except FileNotFoundError as e:
            print(f"FileNotFoundError : {e}")
        except PermissionError:
            print("PermissionError : Permission denied while deleting journal entries.")
        except OSError as e:
            print(f"OSError : {e}")

    elif choice == 5:
        
        print()
        print("Thank you for using Personal Journal Manager. Goodbye !")
        break
        
    print()
    print("--- Choose another Option ---")
    print()
