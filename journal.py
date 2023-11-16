import os
import subprocess
import datetime

def create_entry():
    entry_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    entry_filename = f"journal_{entry_date}.txt"

    with open(entry_filename, 'w') as file:
        file.write("# Journal Entry\n\n")
        file.write(f"## {entry_date}\n\n")
        file.write("Write your thoughts here...")

    edit_entry(entry_filename)

def list_entries():
    entries = [file for file in os.listdir() if file.startswith("journal_") and file.endswith(".txt")]
    
    if not entries:
        print("No journal entries found.")
    else:
        print("Available journal entries:")
        for entry in entries:
            print(entry)

def read_entry():
    list_entries()
    entry_choice = input("Enter the entry filename to read: ")

    if entry_choice in os.listdir() and entry_choice.startswith("journal_") and entry_choice.endswith(".txt"):
        edit_entry(entry_choice)
    else:
        print("Invalid entry filename.")

def edit_entry(filename):
    editor_command = f"nvim {filename}"
    subprocess.run(editor_command, shell=True)

def main():
    while True:
        print("\n1. Create Entry")
        print("2. List Entries")
        print("3. Read Entry")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_entry()
        elif choice == '2':
            list_entries()
        elif choice == '3':
            read_entry()
        elif choice == '4':
            print("Exiting the Journaling App. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

