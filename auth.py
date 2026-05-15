import re
import hashlib
import os
import getpass


MASTER_FILE = "data/master.txt"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def is_strong_password(password):
    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True


def setup_or_login():
    # CREATE MASTER PASSWORD (FIRST RUN)
    if not os.path.exists(MASTER_FILE):
        print("\nNo master password found. Create one.")

        while True:
            password = getpass.getpass("\nSet master password: ")

            if is_strong_password(password):
                with open(MASTER_FILE, "w") as f:
                    f.write(hash_password(password))

                print("Master password set successfully.")
                break
            else:
                print("\nWeak password!")
                print("Must contain:")
                print("- At least 8 characters")
                print("- Uppercase letter (A-Z)")
                print("- Lowercase letter (a-z)")
                print("- Number (0-9)")
                print("- Special character (!@#$...)")

        return True

    # LOGIN FLOW
    with open(MASTER_FILE, "r") as f:
        saved_password = f.read()

    attempts = 3

    while attempts > 0:
        password = getpass.getpass("Enter master password: ")

        if hash_password(password) == saved_password:
            print("Access granted.")
            return True
        else:
            attempts -= 1
            print(f"Wrong password. Attempts left: {attempts}")

    print("Too many failed attempts. Access denied.")
    return False

