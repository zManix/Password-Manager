import sqlite3
from cryptography.fernet import Fernet
import os
import random
import string
from colorama import Fore, init
import sys

# Überprüfen, ob wir uns auf einem Windows-System befinden
if os.name == 'nt':
    import msvcrt
else:
    import tty
    import termios

# Initialize colorama
init(autoreset=True)


# Funktion zur Passwort-Eingabe mit Asterisken
def input_password(prompt="Password: "):
    print(prompt, end="", flush=True)
    password = ""
    while True:
        char = _getch()
        if char == '\r' or char == '\n':  # Enter
            print('')
            return password
        elif char == '\x08' or char == '\x7f':  # Backspace
            if len(password) > 0:
                sys.stdout.write('\b \b')
                sys.stdout.flush()
                password = password[:-1]
        elif char == '\x03':  # Ctrl+C
            raise KeyboardInterrupt
        else:
            sys.stdout.write('*')
            sys.stdout.flush()
            password += char


def _getch():
    if os.name == 'nt':
        return msvcrt.getch().decode('utf-8')
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# Generate a key for encryption/decryption
def generate_key():
    return Fernet.generate_key()


# Load an existing key or generate a new one
def load_key():
    if os.path.exists('secret.key'):
        return open('secret.key', 'rb').read()
    else:
        key = generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)
        return key


# Encrypt a password
def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password


# Decrypt a password
def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password


# Create the SQLite database and table
def init_db():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


# Add a new password
def add_password(service_name, username, password, key):
    encrypted_password = encrypt_password(password, key)
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Accounts (service_name, username, password)
    VALUES (?, ?, ?)
    ''', (service_name, username, encrypted_password))
    conn.commit()
    conn.close()


# Retrieve a password
def retrieve_password(service_name, key):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT username, password FROM Accounts WHERE service_name=?
    ''', (service_name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        username, encrypted_password = result
        decrypted_password = decrypt_password(encrypted_password, key)
        return username, decrypted_password
    else:
        return None


# Generate a random password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


# Main menu
def main():
    key = load_key()
    init_db()
    while True:
        print(Fore.BLUE + "=" * 50)
        print("Password Manager")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. Exit")
        print(Fore.BLUE + "=" * 50)
        choice = input("Choose an option: ")

        if choice == '1':
            print(Fore.GREEN + "-" * 50)
            service_name = input("Enter the service name: ")
            username = input("Enter the username: ")
            generate = input("Do you want to generate a password? (y/n): ").lower()
            if generate == 'y':
                length = int(input("Enter the desired password length: "))
                password = generate_password(length)
                print(f"Generated password: {password}")
            else:
                password = input_password("Enter the password: ")
            add_password(service_name, username, password, key)
            print(Fore.GREEN + "Password added successfully.")
            print(Fore.GREEN + "-" * 50)

        elif choice == '2':
            print(Fore.GREEN + "-" * 50)
            service_name = input("Enter the service name: ")
            result = retrieve_password(service_name, key)
            if result:
                username, password = result
                print(f"Username: {username}")
                print(f"Password: {password}")
            else:
                print(Fore.RED + "No password found for this service.")
            print(Fore.GREEN + "-" * 50)

        elif choice == '3':
            print(Fore.RED + "=" * 50)
            print("Exiting Password Manager")
            print(Fore.RED + "=" * 50)
            break

        else:
            print(Fore.YELLOW + "=" * 50)
            print("Invalid choice. Please try again.")
            print(Fore.YELLOW + "=" * 50)


if __name__ == "__main__":
    main()
