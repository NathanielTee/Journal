import os
import json
from cryptography.fernet import Fernet
from datetime import datetime

# Tentukan path untuk menyimpan data
data_directory = r"D:\Project Nathan\Python\Personal Journal\data"
journal_file = os.path.join(data_directory, "journal_entries.json")
key_file = os.path.join(data_directory, "secret.key")

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Save the key to a file
def save_key(key):
    with open(key_file, "wb") as file_handler:
        file_handler.write(key)

# Load the key from a file
def load_key():
    return open(key_file, "rb").read()

# Encrypt the entry
def encrypt_entry(entry, key):
    f = Fernet(key)
    encrypted_entry = f.encrypt(entry.encode())
    return encrypted_entry

# Decrypt the entry
def decrypt_entry(encrypted_entry, key):
    f = Fernet(key)
    decrypted_entry = f.decrypt(encrypted_entry).decode()
    return decrypted_entry

# Create a new journal entry
def create_entry():
    print("Enter your journal entry. Press Enter twice when you're done:")
    entry_lines = []
    while True:
        line = input()  # Read a single line of input
        if line == "":  # Stop if the user presses Enter without typing anything
            break
        entry_lines.append(line)
    
    entry = "\n".join(entry_lines)  # Join all lines with a newline character
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    encrypted_entry = encrypt_entry(entry, key)

    with open(journal_file, "a") as file:
        json.dump({"date": timestamp, "entry": encrypted_entry.decode()}, file)
        file.write("\n")
    
    print("Entry saved!")

# View past entries by date
def view_entries():
    if not os.path.exists(journal_file):
        print("No journal entries found.")
        return
    
    with open(journal_file, "r") as file:
        for line in file:
            entry = json.loads(line)
            date = entry["date"]
            encrypted_entry = entry["entry"].encode()
            decrypted_entry = decrypt_entry(encrypted_entry, key)
            print(f"{date}: {decrypted_entry}")

# Search for keywords in entries
def search_entries(keyword):
    if not os.path.exists(journal_file):
        print("No journal entries found.")
        return
    
    with open(journal_file, "r") as file:
        for line in file:
            entry = json.loads(line)
            encrypted_entry = entry["entry"].encode()
            decrypted_entry = decrypt_entry(encrypted_entry, key)
            if keyword.lower() in decrypted_entry.lower():
                print(f"Found entry on {entry['date']}: {decrypted_entry}")

# Delete a journal entry
def delete_entry():
    if not os.path.exists(journal_file):
        print("No journal entries found.")
        return

    # Load all entries from the journal file
    with open(journal_file, "r") as file:
        entries = [json.loads(line) for line in file.readlines()]

    if not entries:
        print("No entries to delete.")
        return

    # Display all entries with index
    print("\nEntries:")
    for index, entry in enumerate(entries, start=1):
        print(f"{index}. {entry['date']}: {decrypt_entry(entry['entry'].encode(), key)}")

    # Ask the user which entry to delete
    try:
        entry_num = int(input("\nEnter the number of the entry you want to delete: "))
        if 1 <= entry_num <= len(entries):
            # Remove the selected entry
            del entries[entry_num - 1]

            # Write the remaining entries back to the journal file
            with open(journal_file, "w") as file:
                for entry in entries:
                    json.dump(entry, file)
                    file.write("\n")

            print("Entry deleted.")
        else:
            print("Invalid entry number.")
    except ValueError:
        print("Please enter a valid number.")

# Main function to run the journal
def main():
    global key
    # Check if a key exists; if not, generate one
    if not os.path.exists(key_file):
        key = generate_key()
        save_key(key)
        print("Encryption key generated.")
    else:
        key = load_key()
    
    while True:
        print("\nPersonal Journal Menu:")
        print("1. Create New Entry")
        print("2. View Past Entries")
        print("3. Search Entries by Keyword")
        print("4. Delete Entry")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ")
        
        if choice == "1":
            create_entry()
        elif choice == "2":
            view_entries()
        elif choice == "3":
            keyword = input("Enter keyword to search: ")
            search_entries(keyword)
        elif choice == "4":
            delete_entry()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Buat direktori jika belum ada
    os.makedirs(data_directory, exist_ok=True)
    main()
