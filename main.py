from auth import setup_or_login
from storage import add_entry, get_all_entries, search_entry, delete_entry
import getpass
from utils import encode_password, decode_password


def main():
    print("\n==== PASSWORD MANAGER ====\n")

    if not setup_or_login():
        print("Access denied.")
        return

    while True:
        print("\nMenu:")
        print("1. Add password")
        print("2. View passwords")
        print("3. Search password")
        print("4. Delete password")
        print("5. Exit")

        choice = input("\nChoose: ")

        # ➕ ADD PASSWORD
        if choice == "1":
            label = input("Label (e.g. Gmail, Laptop PIN): ")
            username = input("Username (optional): ")
            password = getpass.getpass("Password: ")
            category = input("Category (optional): ")

            entry = {
                "label": label,
                "username": username,
                "password": encode_password(password),
                "category": category
            }

            add_entry(entry)
            print("Saved successfully!")

        # 👀 VIEW ALL
        elif choice == "2":
            entries = get_all_entries()

            if not entries:
                print("No saved passwords.")
            else:
                for i, e in enumerate(entries, 1):
                    real_password = decode_password(e['password'])

                    print(f"\n[{i}] {e['label']}")
                    print(f"   Username : {e['username'] or '-'}")
                    print(f"   Password : {'*' * len(real_password)}")
                    print(f"   Category : {e['category'] or '-'}")

                    action = input("Press [R] to reveal password or Enter to continue: ")

                    if action.lower() == "r":
                        print(f"   🔓 Password: {real_password}")



        # 🔎 SEARCH
        elif choice == "3":
            keyword = input("Search label: ")
            results = search_entry(keyword)

            if not results:
                print("No matches found.")
            else:
                for e in results:
                    real_password = decode_password(e['password'])


                    print(f"\nLabel    : {e['label']}")
                    print(f"Username : {e['username'] or '-'}")
                    print(f"Password : {'*' * len(real_password)}")
                    print(f"Category : {e['category'] or '-'}")

                    action = input("Press [R] to reveal password or Enter to continue: ")

                    if action.lower() == "r":
                         print(f"   🔓 Password: {real_password}")


        # 🗑️ DELETE
        elif choice == "4":
            keyword = input("Enter label to delete: ")
            delete_entry(keyword)
            print("Deleted successfully (if match was found).")

        # 🚪 EXIT
        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()