import os
import subprocess
from cryptography.fernet import Fernet
from datetime import date

today = date.today()


def generate_key():
    return Fernet.generate_key()

def load_key(key_file):
    return open(key_file, "rb").read()

def save_key(key, key_file):
    with open(key_file, "wb") as keyfile:
        keyfile.write(key)

def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        data = file.read()

    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data)

    with open(file_path + ".encrypted", "wb") as file:
        file.write(encrypted_data)

def decrypt_file(encrypted_file_path, key):
    with open(encrypted_file_path, "rb") as file:
        encrypted_data = file.read()

    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data)

    original_file_path = encrypted_file_path.rstrip(".encrypted")
    with open(original_file_path, "wb") as file:
        file.write(decrypted_data)

def edit_and_encrypt():
    temp_file = f"{today}.md"
    
    # Open the file with nvim
    subprocess.run(["nvim", temp_file])

    # Check if the temporary file exists and is not empty
    if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
        key_file = "./secrets/secret.key"

        if not os.path.exists(key_file):
            key = generate_key()
            save_key(key, key_file)
        else:
            key = load_key(key_file)

        encrypt_file(temp_file, key)
        print(f"Encryption completed. Encrypted file saved as {temp_file}.encrypted")

        # Remove the temporary file
        os.remove(temp_file)
    else:
        print("No changes or empty file. Encryption aborted.")

def main():
    choice = input("Do you want to (C)reate an entry or (R)ead one? ").upper()

    if choice == "C":
        edit_and_encrypt()
    elif choice == "R":
        encrypted_file_path_raw = input("Enter the desired date (YYYY-MM-DD): ")
        encrypted_file_path = f"./{encrypted_file_path_raw}.md.encrypted"

        if not os.path.exists(encrypted_file_path):
            print("Encrypted file not found.")
            return

        key_file = "./secrets/secret.key"
        key = load_key(key_file)

        decrypt_file(encrypted_file_path, key)
        print(f"Decryption completed. Decrypted file saved as {encrypted_file_path.rstrip('.encrypted')}")
        subprocess.run(["rm", encrypted_file_path])
        subprocess.run(["nvim", f"{today}.m" ])
    else:
        print("Invalid choice. Please choose E or D.")

if __name__ == "__main__":
    main()

