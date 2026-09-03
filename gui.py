import tkinter as tk
from tkinter import messagebox
import hashlib
import json
import os
import base64
import time

attempts = 3

is_locked = False

INACTIVITY_LIMIT = 120  # seconds (2 minutes)
SETTINGS_FILE = "data/settings.json"
SECURITY_LOG_FILE = "data/security_log.json"

last_activity = 0
auto_lock_job = None

encryption_key = None
SORT_METHOD = "newest"
CATEGORY_MODE = False

CURRENT_VERSION = "1.0.0"
LATEST_VERSION = "1.0.0"

import os
import sys

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)



def hide_all_frames():
    root.unbind_all("<MouseWheel>")
    for widget in root.winfo_children():
        widget.place_forget()
        widget.pack_forget()

def open_dashboard_safe():
    hide_all_frames()
    show_dashboard()





def derive_key(master_password):
    key = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(key)


def load_settings():

    global INACTIVITY_LIMIT
    global SORT_METHOD
    global CATEGORY_MODE

    import os
    import json

    # 🔥 ADD THIS LINE
    os.makedirs("data", exist_ok=True)

    
        

    if not os.path.exists(SETTINGS_FILE):

        default_settings = {
            "auto_lock": 120,
            "sort_method": "newest",
            "category_mode": False
        }

        with open(SETTINGS_FILE, "w") as f:
            json.dump(default_settings, f, indent=4)

    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)

    INACTIVITY_LIMIT = settings.get("auto_lock", 120)
    SORT_METHOD = settings.get("sort_method", "newest")
    CATEGORY_MODE = settings.get("category_mode", False)

# ---------------- CREATE FUNCTION ----------------

def create_master_password(password_entry, confirm_entry, hint_entry, setup_window):

    global encryption_key

    password = password_entry.get()
    confirm = confirm_entry.get()
    hint = hint_entry.get().strip()

    if len(password) < 6:
        messagebox.showwarning(
            "Weak Password",
            "Password must be at least 6 characters."
        )
        return

    if password != confirm:
        messagebox.showerror(
            "Mismatch",
            "Passwords do not match."
        )
        return

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    with open("data/master.txt", "w") as f:
        f.write(password_hash)

    from datetime import datetime

    password_data = {
        "last_changed": datetime.now().strftime("%Y-%m-%d")
    }

    with open("data/password_age.json", "w") as f:
        json.dump(password_data, f, indent=4)

    with open("data/hint.txt", "w") as f:
        f.write(hint)

    

    with open("data/vault.json", "w") as f:
        json.dump([], f)

    encryption_key = derive_key(password)

    

    
    messagebox.showinfo(
        "Success",
        "Vault created successfully. Please log in to continue."
    )
    print("STEP: BEFORE SECURITY NOTICE")
    setup_window.destroy()
    print("STEP: AFTER DESTROY")
    
    root.after(200, show_security_notice)
    print("STEP: AFTER SECURITY NOTICE CALL")

def first_time_setup():
    print("DEBUG: first_time_setup started")
    global login_window

    try:
        login_window.destroy()
    except:
        pass

    # ---------------- RESET VAULT FILES ----------------

    import json
    import os

    files_to_reset = {
        "data/vault.json": [],
        "data/security_log.json": [],
        "data/password_age.json": {},
        "data/hint.txt": ""
    }

    for path, default_data in files_to_reset.items():

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as file:

            if path.endswith(".json"):
                json.dump(default_data, file, indent=4)

            else:
                file.write(default_data)

    setup_window = tk.Toplevel(root)
    setup_window.title("Create Master Password")
    setup_window.geometry("520x620")
    setup_window.configure(bg="#030712")
    setup_window.resizable(True, True)

    setup_window.grab_set()
    setup_window.focus_force()
    setup_window.protocol("WM_DELETE_WINDOW", root.destroy)


    

    # ---------------- TITLE ----------------

    tk.Label(
        setup_window,
        text="Welcome To VaultShield",
        font=("Segoe UI", 18, "bold"),
        fg="white",
        bg="#030712"
    ).pack(pady=(20, 10))

    tk.Label(
        setup_window,
        text=(
            "Create your master password.\n"
            "This password protects your entire vault.\n\n"
            "If forgotten, it cannot be recovered."
        ),
        font=("Segoe UI", 10),
        fg="#9ca3af",
        bg="#030712",
        justify="center"
    ).pack(pady=(0, 25))

    # ---------------- PASSWORD ----------------
    print("DEBUG: about to create button")
    
    tk.Label(
        setup_window,
        text="Create Master Password",
        fg="white",
        bg="#030712"
    ).pack(anchor="w", padx=40)

    # ---------------- PASSWORD FRAME ----------------

    password_frame = tk.Frame(
        setup_window,
        bg="#030712"
    )

    password_frame.pack(fill="x", padx=40, pady=(5, 20))

    show_password = False

    password_entry = tk.Entry(
        password_frame,
        show="*",
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat",
        font=("Segoe UI", 11)
    )

    password_entry.pack(side="left", fill="x", expand=True, ipady=8)

    def toggle_password():

        nonlocal show_password

        show_password = not show_password

        if show_password:
            password_entry.config(show="")
            password_eye.config(text="🙈")

        else:
            password_entry.config(show="*")
            password_eye.config(text="👁")

    password_eye = tk.Button(
        password_frame,
        text="👁",
        command=toggle_password,
        bg="#111827",
        fg="white",
        activebackground="#1f2937",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI Emoji", 11)
    )

    password_eye.pack(side="left", padx=5)


    # ---------------- CONFIRM ----------------

    tk.Label(
        setup_window,
        text="Confirm Password",
        fg="white",
        bg="#030712"
    ).pack(anchor="w", padx=40)

    # ---------------- CONFIRM PASSWORD FRAME ----------------

    confirm_frame = tk.Frame(
        setup_window,
        bg="#030712"
    )

    confirm_frame.pack(fill="x", padx=40, pady=(5, 20))

    show_confirm = False

    confirm_entry = tk.Entry(
        confirm_frame,
    show="*",
    bg="#111827",
    fg="white",
    insertbackground="white",
    relief="flat",
    font=("Segoe UI", 11)
    )

    confirm_entry.pack(side="left", fill="x", expand=True, ipady=8)

    def toggle_confirm():

        nonlocal show_confirm

        show_confirm = not show_confirm

        if show_confirm:
            confirm_entry.config(show="")
            confirm_eye.config(text="🙈")

        else:
            confirm_entry.config(show="*")
            confirm_eye.config(text="👁")

    confirm_eye = tk.Button(
        confirm_frame,
        text="👁",
        command=toggle_confirm,
        bg="#111827",
        fg="white",
        activebackground="#1f2937",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI Emoji", 11)
    )

    confirm_eye.pack(side="left", padx=5)



    # ---------------- HINT ----------------

    tk.Label(
        setup_window,
        text="Password Hint (Optional)",
        fg="white",
        bg="#030712"
    ).pack(anchor="w", padx=40)

    hint_entry = tk.Entry(
        setup_window,
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat",
        font=("Segoe UI", 11)
    )

    hint_entry.pack(fill="x", padx=40, pady=(5, 25), ipady=8)

    tk.Button(
        setup_window,
        text="Create Vault",
        command=lambda: create_master_password(
            password_entry,
            confirm_entry,
            hint_entry,
            setup_window
        ),
        bg="#7c3aed",
        fg="white",
        activebackground="#8b5cf6",
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        font=("Segoe UI", 11, "bold"),
        cursor="hand2"
    ).pack(pady=15)

    

        

def clear_screen():
    root.update_idletasks()
    for widget in root.winfo_children():
        widget.destroy()    



def save_auto_lock_setting(seconds):

    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)

    settings["auto_lock"] = seconds

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def save_sort_settings(method, category_mode):

    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)

    settings["sort_method"] = method
    settings["category_mode"] = category_mode

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def log_security_event(event, detail=""):
    from datetime import datetime
    import json, os

    if not os.path.exists(SECURITY_LOG_FILE):
        logs = []
    else:
        try:
            with open(SECURITY_LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []

    logs.append({
        "event": event,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "detail": detail
    })

    # keep only last 100 logs
    logs = logs[-100:]

    with open(SECURITY_LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)        


def check_password():
    global is_locked

    global attempts
    global encryption_key

    entered = password_entry.get()
    entered_hash = hashlib.sha256(entered.encode()).hexdigest()

    with open("data/master.txt", "r") as f:
        stored_hash = f.read().strip()

    if entered_hash == stored_hash:
        encryption_key = derive_key(entered)

        login_window.destroy()

        root.configure(bg="#030712")

        is_locked = False

        log_security_event("Login successful", "User logged into vault")

        root.deiconify()
        root.update_idletasks()

        try:
            root.state("zoomed")

        except:
            root.attributes("-fullscreen", True)
        
        root.after(0, show_dashboard)

        # run password reminder AFTER UI fully loads
        root.after(300, check_password_age)

        reset_activity()
        check_inactivity()

    else:
        attempts -= 1

        log_security_event(
            "LOGIN_FAILED_ATTEMPT",
            f"{3 - attempts} failed attempt(s)"
        )

        if attempts <= 0:
            messagebox.showerror(
                "Locked",
                "Too many failed attempts. Application will close."
            )
            root.destroy()
            return

        password_entry.delete(0, tk.END)  # 👈 clear input after wrong try
        if attempts_label and attempts_label.winfo_exists():
            attempts_label.config(
                text=f"Attempts Remaining: {attempts}"
            )

        if attempts > 0:
            messagebox.showerror(
                "Error",
                f"Incorrect password\nAttempts left: {attempts}"
            )
        else:
            messagebox.showerror(
                "Locked Out",
                "Too many failed attempts.\nTry again later."
            )
            root.destroy()  # closes the whole app




def save_password(label_entry, username_entry, password_entry, category_entry):
    import json, os
    from cryptography.fernet import Fernet

    global encryption_key  # 👈 IMPORTANT
    print("KEY IN SAVE:", encryption_key)

    f = Fernet(encryption_key)  # 👈 create encryption object

    raw_password = password_entry.strip()

    data = {
        "label": label_entry.strip(),
        "username": username_entry.strip(),
        "password": f.encrypt(raw_password.encode()).decode(),
        "category": category_entry.strip()
    }

    if not data["label"] or not raw_password:
        messagebox.showwarning(
            "Missing Information",
            "Label and Password are required."
        )
        return

    file_path = "data/vault.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as f_json:
            try:
                vault = json.load(f_json)
            except:
                vault = []
    else:
        vault = []

    vault.append(data)

    with open(file_path, "w") as f_json:
        json.dump(vault, f_json, indent=4)

    messagebox.showinfo("Success", "Saved successfully")

    log_security_event("Password added", f"Label: {data['label']}")


def view_passwords():
    global encryption_key
    import json
    import hashlib
    from tkinter import messagebox, simpledialog
    from cryptography.fernet import Fernet

    if not encryption_key:
        messagebox.showerror("Error", "Encryption key not loaded")
        return

    file_path = "data/vault.json"

    try:
        with open(file_path, "r") as f:
            data = json.load(f)

            # ---------------- SORTING ----------------

            categorized = {}

            for item in data:
                category = item.get("category")

                # normalize category
                if not category or not str(category).strip():
                    category = "Uncategorized"

                else:
                    category = str(category).strip()

                if category not in categorized:
                    categorized[category] = []

                categorized[category].append(item)


                # ---------------- NO CATEGORIES FOUND ----------------

                if not categorized:

                    messagebox.showinfo(
                        "No Categories",
                        "No passwords saved with categories found."
                    )

                    data = list(reversed(data))

                else:

                    categorized = dict(
                        sorted(
                            categorized.items(),
                            key=lambda x: x[0].lower()
                        )
                    )

            else:

                if SORT_METHOD == "newest":
                    data = list(reversed(data))

                elif SORT_METHOD == "oldest":
                    pass

                elif SORT_METHOD == "a-z":
                    data.sort(
                        key=lambda x: x.get("label", "").lower()
                    )
                elif SORT_METHOD == "z-a":
                    data.sort(
                        key=lambda x: x.get("label", "").lower(),
                        reverse=True
                    )

    except:
        messagebox.showinfo("Vault", "No saved items found.")
        return

    if not data:
        messagebox.showinfo("Vault", "Vault is empty.")
        return

    hide_all_frames()

    root.configure(bg="#030712")

    view_window = tk.Frame(root, bg="#030712")
    view_window.pack(fill="both", expand=True)

    # ---------------- TOP SECTION ----------------

    top_frame = tk.Frame(view_window, bg="#030712")
    top_frame.pack(fill="x", padx=20, pady=20)

    tk.Button(
        top_frame,
        text="⬅ Back",
        command=show_dashboard,
        bg="#111827",
        fg="white",
        activebackground="#1f2937",
        relief="flat",
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2",
        font=("Segoe UI", 10)
    ).pack(side="left")

    tk.Label(
        top_frame,
        text="Vault Entries",
        font=("Segoe UI", 22, "bold"),
        fg="white",
        bg="#030712"
    ).pack(side="left", padx=20)

    # ---------------- SCROLLABLE AREA ----------------

    main_frame = tk.Frame(view_window, bg="#030712")
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame, bg="#030712", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    content_frame = tk.Frame(canvas, bg="#030712")
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_frame.bind("<Configure>", on_configure)

    def mouse_scroll(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<MouseWheel>", mouse_scroll)

    # ---------------- EDIT ENTRY ----------------
    def edit_entry(i, lst):

        current_item = lst[i]
        entered_password = simpledialog.askstring(
            "Master Password",
            "Enter master password to edit:",
            show="*"
        )

        if not entered_password:
            return

        entered_hash = hashlib.sha256(
            entered_password.encode()
        ).hexdigest()

        with open("data/master.txt", "r") as f:
            stored_hash = f.read().strip()

        if entered_hash != stored_hash:
             messagebox.showerror(
                "Access_denied",
                "Incorrect_master_password"
             )
             return






        edit_window = tk.Toplevel(root)
        edit_window.transient(root)
        edit_window.grab_set()

        edit_window.title("Edit Entry")
        edit_window.geometry("450x650")
        edit_window.configure(bg="#030712")

        tk.Label(
            edit_window,
            text=f"Editing: {current_item.get('label')}",
            fg="white",
            bg="#030712",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=20)

       

       
       # ---------------- FORM CONTAINER ----------------
        form_frame = tk.Frame(
            edit_window,
            bg="#030712"
        )
            

        form_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # ---------------- LABEL FIELD ----------------

        tk.Label(
            form_frame,
            text="Label",
            fg="white",
            bg="#030712",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(10, 5))

        label_entry = tk.Entry(
            form_frame,
            bg="#111827",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 11)
        )

        label_entry.insert(0, current_item.get("label", ""))

        label_entry.pack(fill="x", ipady=8)

        # ---------------- USERNAME FIELD -----------------
        
        tk.Label(
            form_frame,
            text="Username",
            fg="white",
            bg="#030712",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(18, 5))

        user_entry = tk.Entry(
            form_frame,
            bg="#111827",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 11)
        )

        user_entry.insert(0, current_item.get("username", ""))

        user_entry.pack(fill="x", ipady=8)

        # ---------------- CATEGORY FIELD ----------------

        tk.Label(
            form_frame,
            text="Category",
            fg="white",
            bg="#030712",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(18, 5))

        cat_entry = tk.Entry(
            form_frame,
            bg="#111827",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 11)
        )

        cat_entry.insert(0, current_item.get("category", ""))

        cat_entry.pack(fill="x", ipady=8)

        # ---------------- PASSWORD FIELD ----------------

        tk.Label(
            form_frame,
            text="Password",
            fg="white",
            bg="#030712",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(18, 5))

        password_frame = tk.Frame(
            form_frame,
            bg="#111827"
        )

        password_frame.pack(fill="x")

        password_entry = tk.Entry(
            password_frame,
            show="*",
            bg="#111827",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 11),
            bd=0
        )

        password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(10, 0),
            ipady=10
        )

        try:
            f = Fernet(encryption_key)

            decrypted_password = f.decrypt(
                current_item["password"].encode()
            ).decode()

            password_entry.insert(0, decrypted_password)

        except:
            password_entry.insert(0, "")
                

        # ---------------- PASSWORD TOGGLE ----------------

        password_visible = False

        def toggle_password():
            nonlocal password_visible

            if password_visible:
                password_entry.config(show="*")
                toggle_btn.config(text="👁")
                password_visible = False

            else:
                password_entry.config(show="")
                toggle_btn.config(text="🔒")
                password_visible = True

        
        toggle_btn = tk.Button(
            password_frame,
            text="👁",
            command=toggle_password,
            bg="#111827",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 11)
        )

        toggle_btn.pack(side="right", padx=10)


        









       
       
       
       


       


       


       


       


       


        

        

        

        def save():

            current_item["label"] = label_entry.get()
            current_item["username"] = user_entry.get()
            current_item["category"] = cat_entry.get()

            new_password = password_entry.get()

            f = Fernet(encryption_key)

            encrypted_password = f.encrypt(
                new_password.encode()
            ).decode()

            current_item["password"] = encrypted_password

            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)

            messagebox.showinfo("Saved", "Entry updated successfully")

            log_security_event(
                "Password edited",
                f"Label: {current_item['label']}"
            )

            edit_window.destroy()
            refresh()

        button_frame = tk.Frame(
            edit_window,
            bg="#030712"
        )

        button_frame.pack(pady=25)

        tk.Button(
            button_frame,
            text="Cancel",
            command=edit_window.destroy,
            bg="#111827",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Save Changes",
            command=save,
            bg="#7c3aed",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=10)

    # ---------------- DELETE ENTRY ----------------
    def delete_entry(i, lst):

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this entry?"
        )

        if not confirm:
            return

        

        item_to_delete = lst[i]

        if item_to_delete in data:
            data.remove(item_to_delete)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
            

        messagebox.showinfo("Deleted", "Entry deleted successfully")

        log_security_event("Password deleted", "A vault entry was removed")

        

        if len(data) == 0:
            messagebox.showinfo("Vault Empty", "No more saved passwords.")

            show_dashboard()
            return

        refresh()





    # ---------------- REFRESH ----------------

    

    def refresh():
        view_window.destroy()
        view_passwords()

    # ================= CATEGORY MODE =================

    if CATEGORY_MODE and categorized:

        for category_name, items in categorized.items():

            tk.Label(
                content_frame,
                text=category_name.upper(),
                bg="#030712",
                fg="#8b5cf6",
                font=("Segoe UI", 14, "bold")
            ).pack(anchor="w", padx=18, pady=(18, 5))

            for index, item in enumerate(items):

                frame = tk.Frame(
                    content_frame,
                    bg="#1e1e2f",
                    bd=0,
                    padx=12,
                    pady=10
                )
                frame.pack(fill="x", padx=12, pady=8)

                tk.Label(
                    frame,
                    text=f"Label: {item.get('label')}",
                    bg="#1e1e2f",
                    fg="white",
                    font=("Arial", 11, "bold")
                ).pack(anchor="w")

                tk.Label(
                    frame,
                    text=f"Username: {item.get('username')}",
                    bg="#1e1e2f",
                    fg="#cfcfcf",
                    font=("Arial", 10)
                ).pack(anchor="w")

                tk.Label(
                    frame,
                    text=f"Category: {item.get('category')}",
                    bg="#1e1e2f",
                    fg="#a0a0a0",
                    font=("Arial", 9, "italic")
                ).pack(anchor="w")

                # ---------------- FIXED PASSWORD STATE (PER ITEM) ----------------
                state = {"visible": False}

                pwd_label = tk.Label(
                    frame,
                    text="Password: ********",
                    bg="#1e1e2f",
                    fg="#ffcc66",
                    font=("Arial", 10)
                )
                pwd_label.pack(anchor="w", pady=5)

                copy_btn = tk.Button(
                    frame,
                    text="Copy",
                    bg="#2d2d44",
                    fg="white",
                    activebackground="#3a3a5a",
                    relief="flat",
                )
                copy_btn.pack_forget()

                def copy_password(pwd):
                    root.clipboard_clear()
                    root.clipboard_append(pwd)
                    messagebox.showinfo("Copied", "Password copied to clipboard")

                    log_security_event("Password copied", "Category view password copied")

                def toggle_password(item=item, label=pwd_label, btn=copy_btn, state=state):

                    try:
                        f = Fernet(encryption_key)
                        decrypted = f.decrypt(item["password"].encode()).decode()
                    except:
                        decrypted = "Decryption Error"

                    if not state["visible"]:
                        label.config(text=f"Password: {decrypted}")
                        btn.config(command=lambda p=decrypted: copy_password(p))
                        btn.pack(anchor="w", pady=2)
                        state["visible"] = True
                    else:
                        label.config(text="Password: ********")
                        btn.pack_forget()
                        state["visible"] = False

                tk.Button(
                    frame,
                    text="Show/Hide",
                    command=toggle_password,
                    bg="#3b3b5c",
                    fg="white",
                    relief="flat",
                    padx=8
                ).pack(anchor="w", pady=5)

                button_frame = tk.Frame(frame, bg="#1e1e2f")
                button_frame.pack(anchor="w", pady=5)

                tk.Button(
                    button_frame,
                    text="Edit",
                    command=lambda i=index, lst=items: edit_entry(i, lst),
                    bg="#2563eb",
                    fg="white",
                    relief="flat",
                    padx=10
                ).pack(side="left", padx=5)

                tk.Button(
                    button_frame,
                    text="Delete",
                    command=lambda i=index, lst=items: delete_entry(i, lst),
                    bg="#dc2626",
                    fg="white",
                    relief="flat",
                    padx=10
                ).pack(side="left", padx=5)

                



    # ================= NORMAL MODE =================

    else:

        for index, item in enumerate(data):

            frame = tk.Frame(
                content_frame,
                bg="#1e1e2f",
                bd=0,
                padx=12,
                pady=10
            )
            frame.pack(fill="x", padx=12, pady=8)

            tk.Label(
                frame,
                text=f"Label: {item.get('label')}",
                bg="#1e1e2f",
                fg="white",
                font=("Arial", 11, "bold")
            ).pack(anchor="w")

            tk.Label(
                frame,
                text=f"Username: {item.get('username')}",
                bg="#1e1e2f",
                fg="#cfcfcf",
                font=("Arial", 10)
            ).pack(anchor="w")

            tk.Label(
                frame,
                text=f"Category: {item.get('category')}",
                bg="#1e1e2f",
                fg="#a0a0a0",
                font=("Arial", 9, "italic")
            ).pack(anchor="w")

            # ---------------- FIXED PASSWORD STATE (PER ITEM) ----------------
            state = {"visible": False}

            pwd_label = tk.Label(
                frame,
                text="Password: ********",
                bg="#1e1e2f",
                fg="#ffcc66",
                font=("Arial", 10)
            )
            pwd_label.pack(anchor="w", pady=5)

            button_frame = tk.Frame(frame, bg="#1e1e2f")
            button_frame.pack(anchor="w", pady=5)

            tk.Button(
                button_frame,
                text="Edit",
                command=lambda i=index, lst=data: edit_entry(i, lst),
                bg="#2563eb",
                fg="white",
                relief="flat",
                padx=10
            ).pack(side="left", padx=5)

            tk.Button(
                button_frame,
                text="Delete",
                command=lambda i=index, lst=data: delete_entry(i, lst),
                bg="#dc2626",
                fg="white",
                relief="flat",
                padx=10
            ).pack(side="left", padx=5)

            copy_btn = tk.Button(
                frame,
                text="Copy",
                bg="#2d2d44",
                fg="white",
                activebackground="#3a3a5a",
                relief="flat",
            )
            copy_btn.pack_forget()

            def copy_password(pwd):
                root.clipboard_clear()
                root.clipboard_append(pwd)
                messagebox.showinfo("Copied", "Password copied to clipboard")

                log_security_event("Password copied", "A vault entry password was copied")

            def toggle_password(item=item, label=pwd_label, btn=copy_btn, state=state):

                try:
                    f = Fernet(encryption_key)
                    decrypted = f.decrypt(item["password"].encode()).decode()
                except:
                    decrypted = "Decryption Error"

                if not state["visible"]:
                    label.config(text=f"Password: {decrypted}")
                    btn.config(command=lambda p=decrypted: copy_password(p))
                    btn.pack(anchor="w", pady=2)
                    state["visible"] = True
                else:
                    label.config(text="Password: ********")
                    btn.pack_forget()
                    state["visible"] = False

            tk.Button(
                frame,
                text="Show/Hide",
                command=toggle_password,
                bg="#3b3b5c",
                fg="white",
                relief="flat",
                padx=8
            ).pack(anchor="w", pady=5)

        


# Main root (hidden first)
root = tk.Tk()

root.configure(bg="#030712")

container = tk.Frame(root, bg="#030712")
container.pack(fill="both", expand=True)

root.title("VaultShield - Secure Password Manager")
try:
    root.iconbitmap(resource_path("docs/icon.ico"))
except tk.TclError:
    pass  # Ignore if icon is not found

root.geometry("400x400")
root.configure(bg="#030712")

root.withdraw()  # hide main window initially
login_window = None
password_entry = None
attempts_label = None









def search_vault():
    global encryption_key
    import json
    from tkinter import messagebox

    from cryptography.fernet import Fernet
    
    global encryption_key
    f = Fernet(encryption_key)

    file_path = "data/vault.json"

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except:
        messagebox.showinfo("Vault", "No saved items found.")
        return

    search_window = tk.Toplevel(root)
    search_window.title("Search Vault")
    search_window.configure(bg="#030712")

    window_width = 540
    window_height = 620

    screen_width = search_window.winfo_screenwidth()
    screen_height = search_window.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    search_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    search_window.transient(root)
    search_window.grab_set()
    search_window.focus_force()


    tk.Label(
        search_window,
        text="Search Vault",
        font=("Segoe UI", 20, "bold"),
        fg="white",
        bg="#030712"
    ).pack(pady=(20, 5))

    tk.Label(
        search_window,
        text="Type to search by label or category",
        font=("Segoe UI", 10),
        fg="#9ca3af",
        bg="#030712"
    ).pack(pady=(0, 20))

    search_entry = tk.Entry(
        search_window,
        width=38,
        font=("Segoe UI", 11),
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat"
    )

    search_entry.pack(pady=10, ipady=8)

    results_container = tk.Frame(
        search_window,
        bg="#030712"
    )
    results_container.pack(fill="both", expand=True)

    canvas = tk.Canvas(
        results_container,
        bg="#030712",
        highlightthickness=0
    )
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(
        results_container,
        orient="vertical",
        command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    content_frame = tk.Frame(
        canvas,
        bg="#030712"
    )

    canvas.create_window(
        (0, 0),
        window=content_frame,
        anchor="nw"
    )

    def mouse_scroll(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )
    
    canvas.bind("<MouseWheel>", mouse_scroll)
    content_frame.bind("<MouseWheel>", mouse_scroll)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_frame.bind("<Configure>", on_configure)

    def mouse_scroll(event):
        try:
            if canvas.winfo_exists():
                canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )
        except:
            pass

    canvas.bind("<MouseWheel>", mouse_scroll)        



    def update_results(*args):
        query = search_entry.get().lower()

        # clear previous results
        for widget in content_frame.winfo_children():
            widget.destroy()

        if not query:
            return

        found = False

        for item in data:
            if (
                query in item.get("label", "").lower()
                or query in item.get("category", "").lower()
            ):
                found = True

                frame = tk.Frame(
                    content_frame,
                    bg="#1e1e2f",
                    bd=0,
                    padx=12,
                    pady=10
                )
                frame.pack(fill="x", padx=12, pady=8)

                tk.Label(
                    frame,
                    text=f"Label: {item.get('label')}",
                    bg="#1e1e2f",
                    fg="white",
                    font=("Arial", 11, "bold")
                ).pack(anchor="w")
                
                tk.Label(
                    frame,
                    text=f"Username: {item.get('username')}",
                    bg="#1e1e2f",
                    fg="#cfcfcf",
                    font=("Arial", 10)
                ).pack(anchor="w")

                tk.Label(
                    frame,
                    text=f"Category: {item.get('category')}",
                    bg="#1e1e2f",
                    fg="#a0a0a0",
                    font=("Arial", 9, "italic")
                ).pack(anchor="w")

                # -------- PASSWORD SECTION --------
                password_visible = False

                password_label = tk.Label(
                    frame,
                    text="Password: ********",
                    bg="#1e1e2f",
                    fg="#ffcc66",
                    font=("Arial", 10)
                )
                password_label.pack(anchor="w", pady=5)

                copy_btn = tk.Button(
                    frame,
                    text="📋 Copy Password",
                    bg="#2563eb",
                    fg="white",
                    activebackground="#3b82f6",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    font=("Segoe UI", 9, "bold"),
                    padx=10,
                    pady=4
                )

                def copy_password(pwd=item.get("password")):
                    root.focus_force()
                    root.clipboard_clear()
                    root.clipboard_append(pwd)
                    root.update_idletasks()
                    root.update()
                    messagebox.showinfo("Copied", "Password copied to clipboard")

                def toggle_password(lbl=password_label, btn=copy_btn, pwd=item.get("password")):
                    nonlocal password_visible

                    if password_visible:
                        lbl.config(text="Password: ********")
                        btn.pack_forget()
                        password_visible = False
                    else:
                        try:
                            f = Fernet(encryption_key)  # 🔐 create Fernet here
                            decrypted = f.decrypt(pwd.encode()).decode()  # 🔓 decrypt
                        except:
                            decrypted = "Decryption Error"


                        lbl.config(text=f"Password: {decrypted}")
                        btn.config(command=lambda: copy_password(decrypted))
                        btn.pack(anchor="w", pady=2)
                        password_visible = True

                tk.Button(
                    frame,
                    text="👁 Show Password",
                    command=toggle_password,
                    bg="#7c3aed",
                    fg="white",
                    activebackground="#8b5cf6",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    font=("Segoe UI", 9, "bold"),
                    padx=10,
                    pady=4
                ).pack(anchor="w", pady=5)

        if not found:
            tk.Label(
                content_frame,
                text="No results found",
                bg="#1e1e2f",
                fg="#a0a0a0",
                font=("Arial", 11, "italic")
            ).pack(pady=20)

    search_entry.bind("<KeyRelease>", update_results)

def reset_activity(event=None):
    global last_activity
    last_activity = time.time()

def check_inactivity():
    global auto_lock_job

    if root.state() == "withdrawn":
        return

    if time.time() - last_activity > INACTIVITY_LIMIT:
        auto_lock()

    auto_lock_job = root.after(5000, check_inactivity)

def show_login_window():

    global login_window
    global password_entry
    global attempts_label

    try:
        login_window.destroy()
    except:
        pass

    login_window = tk.Toplevel(root)
    login_window.title("Secure Login")
    login_window.geometry("420x320")
    login_window.configure(bg="#030712")
    login_window.resizable(False, False)

    login_window.protocol("WM_DELETE_WINDOW", root.destroy)

    tk.Label(
        login_window,
        text="Password Manager Login",
        font=("Segoe UI", 14, "bold"),
        fg="white",
        bg="#030712"
    ).pack(pady=15)

    tk.Label(
        login_window,
        text="Enter Master Password",
        fg="#9ca3af",
        bg="#030712"
    ).pack(pady=5)

    password_frame = tk.Frame(
        login_window,
        bg="#111827"
    )

    password_frame.pack(pady=10)

    password_entry = tk.Entry(
        password_frame,
        show="*",
        width=30,
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat",
        font=("Segoe UI", 11)
    )

    password_entry.pack(
        side="left",
        padx=(10, 0),
        ipady=8
    )

    password_visible = False

    def toggle_password():

        nonlocal password_visible

        if password_visible:
            password_entry.config(show="*")
            toggle_btn.config(text="👁")
            password_visible = False

        else:
            password_entry.config(show="")
            toggle_btn.config(text="🔒")
            password_visible = True

    toggle_btn = tk.Button(
        password_frame,
        text="👁",
        command=toggle_password,
        bg="#111827",
        fg="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 11)
    )

    toggle_btn.pack(side="right", padx=10)


    password_entry.bind(
        "<Return>",
        lambda event: check_password()
    )

    tk.Button(
        login_window,
        text="Login",
        width=15,
        command=check_password,
        bg="#7c3aed",
        fg="white",
        activebackground="#8b5cf6",
        relief="flat",
        cursor="hand2",
        font=("Segoe UI", 10, "bold")
    ).pack(pady=10)

    attempts_label = tk.Label(
        login_window,
        text=f"Attempts Remaining: {attempts}",
        fg="#f87171",
        bg="#030712",
        font=("Segoe UI", 9)
    )

    attempts_label.pack(pady=5)

    def show_hint():

        try:
            with open("data/hint.txt", "r") as f:
                hint = f.read().strip()

            if not hint:
                hint = "No password hint saved."

        except:
            hint = "No password hint found."

        messagebox.showinfo(
            "Password Hint",
            hint
        )
    
    def reset_vault_flow():

        warning = messagebox.askyesno(
            "WARNING",
            "Resetting your vault will permanently delete:\n\n"
            "• All saved passwords\n"
            "• Master password\n"
            "• Security history\n"
            "• All vault data\n\n"
            "This action CANNOT be undone.\n\n"
            "Do you want to continue?"
        )

        if not warning:
            return

        reset_window = tk.Toplevel(login_window)
        reset_window.title("Reset Vault")
        reset_window.geometry("420x320")
        reset_window.configure(bg="#030712")
        reset_window.resizable(False, False)

        tk.Label(
            reset_window,
            text="Type the confirmation words below",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg="#030712"
        ).pack(pady=(25, 10))

        tk.Label(
            reset_window,
            text=(
                "Enter your vault reset confirmation phrase.\n\n"
                "This phrase was shown during first-time setup."
            ),
            font=("Segoe UI", 10),
            fg="#f87171",
            bg="#030712",
            justify="center"
        ).pack(pady=5)
        

        confirm_entry = tk.Entry(
            reset_window,
            bg="#111827",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 11)
        )

        confirm_entry.pack(pady=20, ipady=8, ipadx=40)

        def final_reset():

            typed = confirm_entry.get().strip()

            if typed != "VAULTSHIELD RESET CONFIRM":
                messagebox.showerror(
                    "Incorrect Confirmation",
                    "The confirmation words do not match."
                )
                return

            import os

            files_to_clear = [
                "data/vault.json",
                "data/master.txt",
                "data/hint.txt",
                "data/security_logs.json",
                "data/password_age.json"
            ]

            for file in files_to_clear:

                try:
                    if os.path.exists(file):
                        os.remove(file)

                except:
                    pass

            messagebox.showinfo(
                "Vault Reset",
                "Vault has been reset successfully.\n\n"
                "The app will now restart."
            )

            reset_window.destroy()
            login_window.destroy()

            start_app()

        tk.Button(
            reset_window,
            text="Reset Vault",
            command=final_reset,
            bg="#dc2626",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        ).pack(pady=15)


    def forgot_password_options():

        option = messagebox.askyesnocancel(
            "Forgot Password",
            "Choose an option:\n\n"
            "YES = View Password Hint\n"
            "NO = Reset Vault\n"
            "CANCEL = Go Back"
        )
        if option is True:
            show_hint()

        elif option is False:
            reset_vault_flow()

    tk.Button(
        login_window,
        text="Forgot Password?",
        command=forgot_password_options,
        bg="#030712",
        fg="#8b5cf6",
        activebackground="#030712",
        activeforeground="#a78bfa",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 9, "underline")
    ).pack(pady=(5, 0))
                

def show_login_again():
    global login_window, password_entry

    # prevent duplicate login windows
    try:
        login_window.destroy()
    except:
        pass

    login_window = tk.Toplevel(root)
    login_window.title("Re-Login Required")
    login_window.geometry("420x320")
    login_window.configure(bg="#030712")

    # 🔥 FORCE WINDOW TO FRONT
    login_window.update_idletasks()
    login_window.lift()
    login_window.attributes("-topmost", True)
    login_window.after(100, lambda: login_window.attributes("-topmost", False))

    # 🔥 CENTER IT (VERY IMPORTANT)
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()

    x = (screen_width // 2) - 210
    y = (screen_height // 2) - 160

    login_window.geometry(f"420x320+{x}+{y}")

    print("exists:", login_window.winfo_exists())
    print("state:", login_window.state())


    # ---------------- TITLE ----------------
    tk.Label(
        login_window,
        text="Session Locked 🔒",
        font=("Segoe UI", 18, "bold"),
        fg="white",
        bg="#030712"
    ).pack(pady=(25, 5))

    tk.Label(
        login_window,
        text="Enter your password to continue",
        font=("Segoe UI", 10),
        fg="#9ca3af",
        bg="#030712"
    ).pack(pady=(0, 20))

    # ---------------- PASSWORD FIELD ----------------

    password_frame = tk.Frame(login_window, bg="#030712")
    password_frame.pack(pady=10)

    password_entry = tk.Entry(
        password_frame,
        show="*",
        width=28,
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat",
        font=("Segoe UI", 11)
    )
    password_entry.pack(side="left", ipady=8)

    # ---------------- TOGGLE (FIXED) ----------------

    show_password = False  # local state ONLY

    def toggle_password():
        nonlocal show_password

        show_password = not show_password

        if show_password:
            password_entry.config(show="")
            eye_button.config(text="🙈")
        else:
            password_entry.config(show="*")
            eye_button.config(text="👁")

    eye_button = tk.Button(
        password_frame,
        text="👁",
        command=toggle_password,
        bg="#111827",
        fg="white",
        activebackground="#1f2937",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI Emoji", 11)
    )
    eye_button.pack(side="left", padx=5)

    # ---------------- BUTTON ----------------

    tk.Button(
        login_window,
        text="Unlock",
        command=check_password,
        bg="#7c3aed",
        fg="white",
        activebackground="#8b5cf6",
        relief="flat",
        padx=20,
        pady=8,
        font=("Segoe UI", 10, "bold")
    ).pack(pady=15)

    login_window.protocol("WM_DELETE_WINDOW", root.destroy)

    print("LOGIN CALLED")


def auto_lock():
    global is_locked

    is_locked = True

    messagebox.showwarning("Locked", "Session timed out due to inactivity")

    root.withdraw()

    show_login_again()


def check_password_age():

    import json
    import os
    from datetime import datetime
    from tkinter import messagebox

    print("PASSWORD AGE CHECK RUNNING")

    file_path = "data/password_age.json"
    print("READING FROM:", os.path.abspath(file_path))

    # ---------------- CREATE FILE IF MISSING ----------------
    if not os.path.exists(file_path):
        from datetime import datetime

        data = {
            "last_changed": datetime.now().strftime("%Y-%m-%d")
        }

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        return  # nothing to warn yet

    # ---------------- LOAD DATA ----------------
    with open(file_path, "r") as f:
        data = json.load(f)

    saved_date = data.get("last_changed")

    if not saved_date:
        return

    old_date = datetime.strptime(saved_date, "%Y-%m-%d")
    today = datetime.now()

    days_passed = (today - old_date).days

    print("DAYS PASSED:", days_passed)

    # ---------------- WARNINGS ----------------

    if 80 <= days_passed < 90:

        messagebox.showwarning(
            "Security Reminder",
            f"Your master password is {days_passed} days old.\n\n"
            "Consider changing it soon."
        )

    elif days_passed >= 90:

        messagebox.showwarning(
            "Password Age Alert",
            f"Your master password is {days_passed} days old.\n\n"
            "It is strongly recommended to change it."
        )

def show_security_notice():
    print("SECURITY NOTICE OPENED")

    
    
    notice_window = tk.Toplevel(root)
    notice_window.title("VaultShield Security Notice")

    notice_window.state("zoomed")
    notice_window.minsize(1000, 700)

    notice_window.configure(bg="#030712")

    

    notice_window.lift()
    notice_window.attributes("-topmost", True)
    notice_window.after(100, lambda: notice_window.attributes("-topmost", False))

    def focus():
        notice_window.focus_force()

    notice_window.after(100, focus)

    # ---------------- TITLE ----------------

    tk.Label(
        notice_window,
        text="Welcome To VaultShield",
        font=("Segoe UI", 20, "bold"),
        fg="white",
        bg="#030712"
    ).pack(pady=(20, 5))

    tk.Label(
        notice_window,
        text="Please read this important information carefully.",
        font=("Segoe UI", 10),
        fg="#9ca3af",
        bg="#030712"
    ).pack(pady=(0, 20))

    # ---------------- TEXT AREA ----------------

    text_frame = tk.Frame(
        notice_window,
        bg="#030712"
    )

    text_frame.pack(fill="both", expand=True, padx=20, pady=10)

    text_box = tk.Text(
        text_frame,
        wrap="word",
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat",
        font=("Segoe UI", 10),
        padx=15,
        pady=15
    )

    text_box.pack(fill="both", expand=True)

    notice_text = """

WELCOME TO VAULTSHIELD

VaultShield securely stores and encrypts your passwords locally on your device.

━━━━━━━━━━━━━━━━━━
MASTER PASSWORD
━━━━━━━━━━━━━━━━━━

Your master password is the key to your vault.

VaultShield DOES NOT store your real password and it CANNOT be recovered if forgotten.

If you lose your master password, the only option is to reset your vault permanently.

Choose a password you will remember.


━━━━━━━━━━━━━━━━━━
PASSWORD HINT
━━━━━━━━━━━━━━━━━━

The password hint is optional but highly recommended.

Hints help you remember your master password without revealing it directly.

If you create a hint, it can be viewed from the login screen using the "Forgot Password?" option.


━━━━━━━━━━━━━━━━━━
RESETTING YOUR VAULT
━━━━━━━━━━━━━━━━━━

If you completely forget your master password, you may reset your vault.

WARNING:
Resetting permanently deletes:
• all saved passwords
• security activity
• vault data
• master password

This action CANNOT be undone.


━━━━━━━━━━━━━━━━━━
RESET CONFIRMATION PHRASE
━━━━━━━━━━━━━━━━━━

To reset your vault, you must type the exact confirmation phrase below:

VAULTSHIELD RESET CONFIRM


IMPORTANT:
VaultShield will NEVER show this phrase again.

Remember it carefully.


━━━━━━━━━━━━━━━━━━
RECENT SECURITY ACTIVITY
━━━━━━━━━━━━━━━━━━

VaultShield records important security actions such as:
• successful logins
• failed login attempts
• password additions
• password edits
• copied passwords

This helps you monitor suspicious activity inside your vault.


━━━━━━━━━━━━━━━━━━
PRIVACY & SECURITY
━━━━━━━━━━━━━━━━━━

• Your data stays on your device
• No cloud storage
• No external servers
• No account tracking
• Your vault is encrypted locally

You are responsible for keeping your master password safe.

"""

    text_box.insert("1.0", notice_text)

    text_box.config(state="disabled")

    # ---------------- BUTTON ----------------

    def continue_to_dashboard():
        notice_window.destroy()

        root.deiconify()   # 🔥 ENSURE ROOT IS VISIBLE

        root.after(50, show_dashboard)

        

    tk.Button(
        notice_window,
        text="I Understand",
        command=continue_to_dashboard,
        bg="#7c3aed",
        fg="white",
        activebackground="#8b5cf6",
        relief="flat",
        padx=25,
        pady=10,
        font=("Segoe UI", 11, "bold"),
        cursor="hand2"
    ).pack(pady=20)

def show_dashboard():
    print("DASHBOARD LOADED")
    
    # 🔥 ALWAYS ENSURE ROOT IS VISIBLE
    root.deiconify()

    # 🔥 FORCE MAXIMIZED STATE
    root.update_idletasks()

    try:
        root.state("zoomed")  # Windows

    except:
        root.attributes("-fullscreen", True)  # fallback

    
    
    root.configure(bg="#030712")

    dashboard_frame = tk.Frame(root, bg="#030712")
    dashboard_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # ---------------- TITLE ----------------

    tk.Label(
        dashboard_frame,
        text="Vault Dashboard",
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#121221"
    ).pack(pady=(10, 5))

    tk.Label(
        dashboard_frame,
        text="Secure. Simple. Yours.",
        font=("Arial", 11),
        fg="#aaaaaa",
        bg="#121221"
    ).pack(pady=(0, 25))

    # ---------------- GRID FRAME ----------------

    grid_frame = tk.Frame(dashboard_frame, bg="#030712")
    grid_frame.pack()

    # ---------------- CARD CREATOR ----------------

    def create_card(parent, title, desc, icon, command, row, col, accent):

        card = tk.Frame(
            parent,
            bg="#111827",
            width=340,
            height=230,
            highlightthickness=1,
            highlightbackground="#1f2937",
            cursor="hand2"
        )

        card.grid(row=row, column=col, padx=22, pady=22)
        card.grid_propagate(False)

        

        # ---------------- TOP SECTION ----------------

        top_section = tk.Frame(card, bg="#111827")
        top_section.pack(fill="x", padx=20, pady=(20, 10))

        
        # icon box
        icon_frame = tk.Frame(
            top_section,
            bg=accent,
            width=55,
            height=55
        )

        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)

        icon_label = tk.Label(
            icon_frame,
            text=icon,
            font=("Arial", 22),
            bg=accent,
            fg="white"
        )

        icon_label.pack(expand=True)

        # text section
        text_frame = tk.Frame(top_section, bg="#111827")
        text_frame.pack(side="left", padx=15)

        title_label = tk.Label(
            text_frame,
            text=title,
            font=("Arial", 15, "bold"),
            bg="#111827",
            fg="white"
        )

        title_label.pack(anchor="w")

        desc_label = tk.Label(
            text_frame,
            text=desc,
            font=("Arial", 10),
            bg="#111827",
            fg="#b5b5c5",
            wraplength=170,
            justify="left"
        )

        desc_label.pack(anchor="w", pady=(5, 0))



        # ---------------- OPEN BUTTON ----------------
        open_btn = tk.Button(
            card,
            text="Open  ›",
            command=command,
            bg=accent,
            fg="white",
            activebackground=accent,
            activeforeground="white",
            relief="flat",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=18,
            pady=6,
            bd=0
        )

        open_btn.pack(pady=(10, 20))

        def btn_enter(e):
            if accent == "#7c3aed":
                open_btn.config(bg="#9f67ff")

        def btn_leave(e):
            open_btn.config(bg=accent)

        open_btn.bind("<Enter>", btn_enter)
        open_btn.bind("<Leave>", btn_leave)


        




    create_card(
        grid_frame,
        "Add Password",
        "Store a new password securely in your vault.",
        "＋",
        show_add_screen,
        0,
        0,
        "#8b5cf6"
    )

    create_card(
        grid_frame,
        "View Passwords",
        "View all your saved passwords.",
        "📁",
        view_passwords,
        0,
        1,
        "#3b82f6"
    )

    create_card(
        grid_frame,
        "Search Vault",
        "Search and find any password quickly.",
        "⌕",
        search_vault,
        1,
        0,
        "#10b981"
    )

    create_card(
        grid_frame,
        "Settings",
        "Manage your preferences and app settings.",
        "⚙",
        open_settings,
        1,
        1,
        "#f59e0b"
    )

    root.bind_all("<Any-KeyPress>", reset_activity)
    root.bind_all("<Any-Button>", reset_activity)

    def reveal_dashboard():
        dashboard_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    root.after(50, reveal_dashboard)

    


def check_for_updates():

    update_window = tk.Toplevel(root)
    update_window.title("Check For Updates")
    update_window.geometry("420x260")
    update_window.configure(bg="#030712")

    update_window.transient(root)
    update_window.grab_set()
    update_window.focus_force()
    update_window.resizable(False, False)

    # ---------------- TITLE ----------------

    title_label = tk.Label(
        update_window,
        text="Checking For Updates...",
        font=("Segoe UI", 16, "bold"),
        fg="white",
        bg="#030712"
    )

    title_label.pack(pady=(40, 15))

    # ---------------- STATUS ----------------

    status_label = tk.Label(
        update_window,
        text="Please wait while VaultShield checks for new features.",
        font=("Segoe UI", 10),
        fg="#9ca3af",
        bg="#030712",
        justify="center"
    )

    status_label.pack()

    # ---------------- LOADING BAR ----------------

    loading = tk.Label(
        update_window,
        text="⏳",
        font=("Segoe UI", 28),
        fg="#7c3aed",
        bg="#030712"
    )

    loading.pack(pady=25)

    # ---------------- CHECK PROCESS ----------------

    def finish_check():

        loading.destroy()

        if CURRENT_VERSION == LATEST_VERSION:

            title_label.config(
                text="You're Up To Date"
            )

            status_label.config(
                text=(
                    f"Current Version: {CURRENT_VERSION}\n\n"
                    "You already have the latest features and improvements."
                )
            )

        else:

            title_label.config(
                text="New Update Available 🚀"
            )

            status_label.config(
                text=(
                    f"Current Version: {CURRENT_VERSION}\n"
                    f"Latest Version: {LATEST_VERSION}\n\n"
                    "New Features:\n"
                    "• Improved vault performance\n"
                    "• Better UI responsiveness\n"
                    "• Security improvements\n"
                    "• Bug fixes and optimizations"
                )
            )

    # wait 2 seconds before showing result
    update_window.after(2000, finish_check)

    # ---------------- CLOSE BUTTON ----------------

    tk.Button(
        update_window,
        text="Close",
        command=update_window.destroy,
        bg="#7c3aed",
        fg="white",
        relief="flat",
        padx=18,
        pady=7,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2"
    ).pack(side="bottom", pady=20)


def theme_unavailable():

    messagebox.showinfo(
        "Theme",
        "This feature is currently unavailable."
    )


def change_master_password():

    confirm = messagebox.askyesno(
        "Change Master Password",
        "Changing your master password will re-secure your vault.\n\n"
        "Make sure you remember the new password.\n"
        "If forgotten, your vault cannot be recovered.\n\n"
        "Do you want to continue?"
    )

    if not confirm:
        return

    change_window = tk.Toplevel(root)
    change_window.transient(root)
    change_window.grab_set()
    change_window.title("Change Master Password")
    change_window.geometry("420x450")
    change_window.configure(bg="#030712")

    # ---------------- TITLE ----------------

    tk.Label(
        change_window,
        text="Master Password Security",
        font=("Segoe UI", 16, "bold"),
        fg="white",
        bg="#030712"
    ).pack(pady=(20, 10))

    tk.Label(
        change_window,
        text="Verify your identity before changing password.",
        font=("Segoe UI", 10),
        fg="#9ca3af",
        bg="#030712"
    ).pack(pady=(0, 20))

    # ---------------- CURRENT PASSWORD ----------------

    tk.Label(
        change_window,
        text="Current Password",
        fg="white",
        bg="#030712",
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=40)

    current_entry = tk.Entry(
        change_window,
        show="*",
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat",
        font=("Segoe UI", 11)
    )

    current_entry.pack(fill="x", padx=40, pady=(5, 20), ipady=8)

    # ---------------- REASON ----------------

    tk.Label(
        change_window,
        text="Reason For Password Change",
        fg="white",
        bg="#030712",
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=40)

    reason_entry = tk.Text(
        change_window,
        height=5,
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat",
        font=("Segoe UI", 10)
    )

    reason_entry.pack(fill="x", padx=40, pady=(5, 20))

    # ---------------- CONTINUE BUTTON ----------------

    def validate_reason():

        current_password = current_entry.get()
        reason = reason_entry.get("1.0", "end").strip()

        current_hash = hashlib.sha256(
            current_password.encode()
        ).hexdigest()

        with open("data/master.txt", "r") as f:
            stored_hash = f.read().strip()

        if current_hash != stored_hash:
            messagebox.showerror("Error", "Current password is incorrect.")
            return

        if len(reason) < 15:
            messagebox.showwarning(
                "Reason Too Short",
                "Please provide a more meaningful reason."
            )
            return

        invalid_reasons = ["idk", "none", "nothing", "123", "yes", "no"]

        if reason.lower() in invalid_reasons:
            messagebox.showwarning("Invalid Reason", "Please provide a valid reason.")
            return

        change_window.destroy()

        #---------------- NEW PASSWORD WINDOW ----------------
    
        new_window = tk.Toplevel(root)
        new_window.transient(root)
        new_window.grab_set()
        new_window.title("Create New Master Password")
        new_window.geometry("520x520")
        new_window.resizable(False, False)
        new_window.configure(bg="#030712")

        tk.Label(
            new_window,
            text="Create New Password",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#030712"
        ).pack(pady=(20, 10))

        tk.Label(
            new_window,
            text="Your vault will be re-secured.",
            font=("Segoe UI", 10),
            fg="#9ca3af",
            bg="#030712"
        ).pack(pady=(0, 20))

        tk.Label(
            new_window,
            text="New Master Password",
            fg="white",
            bg="#030712"
        ).pack(anchor="w", padx=40)

        new_password_frame = tk.Frame(new_window, bg="#030712")
        new_password_frame.pack(fill="x", padx=40, pady=(5, 20))

        new_password_entry = tk.Entry(
            new_password_frame,
            show="*",
            bg="#111827",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 11)
        )

        new_password_entry.pack(side="left", fill="x", expand=True, ipady=8)

        show_new_password = False

        def toggle_new_password():
            nonlocal show_new_password

            show_new_password = not show_new_password

            if show_new_password:
                new_password_entry.config(show="")
                toggle_new_btn.config(text="Hide")

            else:
                new_password_entry.config(show="*")
                toggle_new_btn.config(text="Show")

        toggle_new_btn = tk.Button(
            new_password_frame,
            text="Show",
            command=toggle_new_password,
            bg="#374151",
            fg="white",
            relief="flat",
            padx=10,
            cursor="hand2"
        )

        toggle_new_btn.pack(side="right", padx=(10, 0))







        tk.Label(
            new_window,
            text="Confirm New Password",
            fg="white",
            bg="#030712"
        ).pack(anchor="w", padx=40)

        confirm_frame = tk.Frame(new_window, bg="#030712")
        confirm_frame.pack(fill="x", padx=40, pady=(5, 20))

        confirm_entry = tk.Entry(
            confirm_frame,
            show="*",
            bg="#111827",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 11)
        )

        confirm_entry.pack(side="left", fill="x", expand=True, ipady=8)

        show_confirm_password = False

        def toggle_confirm_password():
            nonlocal show_confirm_password

            show_confirm_password = not show_confirm_password

            if show_confirm_password:
                confirm_entry.config(show="")
                toggle_confirm_btn.config(text="Hide")

            else:
                confirm_entry.config(show="*")
                toggle_confirm_btn.config(text="Show")

        toggle_confirm_btn = tk.Button(
            confirm_frame,
            text="Show",
            command=toggle_confirm_password,
            bg="#374151",
            fg="white",
            relief="flat",
            padx=10,
            cursor="hand2"
        )

        toggle_confirm_btn.pack(side="right", padx=(10, 0))

            


        # ---------------- NEW HINT (OPTIONAL) ----------------
        tk.Label(
            new_window,
            text="New Password Hint (Optional)",
            fg="white",
            bg="#030712"
        ).pack(anchor="w", padx=40)

        hint_entry = tk.Entry(
            new_window,
            bg="#111827",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Segoe UI", 11)
        )

        hint_entry.pack(fill="x", padx=40, pady=(5, 20), ipady=8)

        def finalize_password_change():

            global encryption_key

            new_password = new_password_entry.get()
            confirm_password = confirm_entry.get()

            if len(new_password) < 6:
                messagebox.showwarning(
                    "Weak Password",
                    "Password must be at least 6 characters."
                )

                new_window.destroy()
                return

            if new_password != confirm_password:
                messagebox.showerror(
                    "Mismatch",
                    "Passwords do not match."
                )

                new_window.destroy()
                return

            try:
                from cryptography.fernet import Fernet

                old_fernet = Fernet(encryption_key)

                with open("data/vault.json", "r") as f:
                    vault = json.load(f)

                decrypted_passwords = []

                for item in vault:
                    decrypted = old_fernet.decrypt(
                        item["password"].encode()
                    ).decode()

                    decrypted_passwords.append(decrypted)

                new_key = derive_key(new_password)
                new_fernet = Fernet(new_key)

                for index, item in enumerate(vault):
                    item["password"] = new_fernet.encrypt(
                        decrypted_passwords[index].encode()
                    ).decode()

                with open("data/vault.json", "w") as f:
                    json.dump(vault, f, indent=4)

                new_hash = hashlib.sha256(new_password.encode()).hexdigest()

                with open("data/master.txt", "w") as f:
                    f.write(new_hash)

                new_hint = hint_entry.get().strip()

                if new_hint:
                    with open("data/hint.txt", "w") as f:
                        f.write(new_hint)

                from datetime import datetime

                password_data = {
                    "last_changed": datetime.now().strftime("%Y-%m-%d")
                }

                with open("data/password_age.json", "w") as f:
                    json.dump(password_data, f, indent=4)


                encryption_key = new_key

                messagebox.showinfo("Success", "Master password changed successfully.")

                log_security_event("MASTER_PASSWORD_CHANGED")

                new_window.destroy()
                change_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to change password.\n\n{e}")

        tk.Button(
            new_window,
            text="Update Password",
            command=finalize_password_change,
            bg="#7c3aed",
            fg="white",
            activebackground="#8b5cf6",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        ).pack(pady=20)

    tk.Button(
        change_window,
        text="Continue",
        command=validate_reason,
        bg="#7c3aed",
        fg="white",
        activebackground="#8b5cf6",
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        font=("Segoe UI", 11, "bold"),
        cursor="hand2"
    ).pack(pady=20)


def open_sort_settings():

    global SORT_METHOD
    global CATEGORY_MODE

    # clear screen
    hide_all_frames()

    root.configure(bg="#030712")

    sort_frame = tk.Frame(
        root,
        bg="#030712"
    )

    sort_frame.pack(fill="both", expand=True)

    # ---------------- TOP BAR ----------------

    top_bar = tk.Frame(
        sort_frame,
        bg="#030712"
    )

    top_bar.pack(fill="x", padx=25, pady=20)

    tk.Button(
        top_bar,
        text="← Back",
        command=open_settings,
        bg="#111827",
        fg="white",
        activebackground="#1f2937",
        relief="flat",
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2",
        font=("Segoe UI", 10)
    ).pack(side="left")

    # ---------------- TITLE ----------------

    tk.Label(
        sort_frame,
        text="Sort Method",
        font=("Segoe UI", 24, "bold"),
        fg="white",
        bg="#030712"
    ).pack(pady=(20, 5))

    tk.Label(
        sort_frame,
        text="Choose how your vault entries are organized.",
        font=("Segoe UI", 10),
        fg="#9ca3af",
        bg="#030712"
    ).pack(pady=(0, 30))

    # ---------------- CONTAINER ----------------

    container = tk.Frame(
        sort_frame,
        bg="#030712"
    )

    container.pack(fill="both", expand=True, padx=20)

    # ---------------- SAVE FUNCTION ----------------

    def apply_sort(method, category):

        global SORT_METHOD
        global CATEGORY_MODE

        SORT_METHOD = method
        CATEGORY_MODE = category

        save_sort_settings(method, category)

        messagebox.showinfo(
            "Updated",
            "Vault sorting updated successfully."
        )

        open_settings()

    # ---------------- LABEL SECTION ----------------

    tk.Label(
        container,
        text="Sort By Label",
        font=("Segoe UI", 14, "bold"),
        fg="white",
        bg="#030712"
    ).pack(anchor="w", pady=(10, 15))

    sort_options = [
        ("Newest to Oldest (Default)", "newest"),
        ("Oldest to Newest", "oldest"),
        ("A-Z", "a-z"),
        ("Z-A", "z-a")
    ]

    for label, value in sort_options:

        active = (
            SORT_METHOD == value
            and CATEGORY_MODE == False
        )

        btn = tk.Button(
            container,
            text="✓ Currently Active" if active else label,
            command=lambda v=value: apply_sort(v, False),
            bg="#1f2937" if active else "#111827",
            fg="#9ca3af" if active else "white",
            activebackground="#1f2937",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=20,
            font=("Segoe UI", 11),
            cursor="arrow" if active else "hand2",
            state="disabled" if active else "normal"
        )

        btn.pack(fill="x", pady=8)

    # ---------------- CATEGORY SECTION ----------------

    tk.Label(
        container,
        text="Sort By Category",
        font=("Segoe UI", 14, "bold"),
        fg="white",
        bg="#030712"
    ).pack(anchor="w", pady=(30, 15))

    category_active = CATEGORY_MODE == True

    category_btn = tk.Button(
        container,
        text="✓ Currently Active" if category_active else "Group By Category",
        command=lambda: apply_sort("newest", True),
        bg="#1f2937" if category_active else "#111827",
        fg="#9ca3af" if category_active else "white",
        activebackground="#1f2937",
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=30,
        pady=20,
        font=("Segoe UI", 11),
        cursor="arrow" if category_active else "hand2",
        state="disabled" if category_active else "normal"
    )

    category_btn.pack(fill="x", pady=8)


def change_auto_lock_timer():

    global INACTIVITY_LIMIT

    # clear current screen
    hide_all_frames()

    root.configure(bg="#030712")

    timer_frame = tk.Frame(
        root,
        bg="#030712"
    )

    timer_frame.pack(fill="both", expand=True)

    # ---------------- TOP BAR ----------------

    top_bar = tk.Frame(
        timer_frame,
        bg="#030712"
    )

    top_bar.pack(fill="x", padx=25, pady=20)

    tk.Button(
        top_bar,
        text="← Back",
        command=open_settings,
        bg="#111827",
        fg="white",
        activebackground="#1f2937",
        relief="flat",
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2",
        font=("Segoe UI", 10)
    ).pack(side="left")

    # ---------------- TITLE ----------------

    tk.Label(
        timer_frame,
        text="Auto Lock Timer",
        font=("Segoe UI", 24, "bold"),
        fg="white",
        bg="#030712"
    ).pack(pady=(20, 5))

    tk.Label(
        timer_frame,
        text="Choose when your vault locks after inactivity.",
        font=("Segoe UI", 10),
        fg="#9ca3af",
        bg="#030712"
    ).pack(pady=(0, 30))

    # ---------------- TIMER CONTAINER ----------------

    container = tk.Frame(
        timer_frame,
        bg="#030712"
    )

    container.pack(fill="both", expand=True, padx=20)

    def set_timer(seconds, text):

        global INACTIVITY_LIMIT

        INACTIVITY_LIMIT = seconds

        save_auto_lock_setting(seconds)

        messagebox.showinfo(
            "Updated",
            f"Auto lock timer set to {text}"
        )

        open_settings()

    # ---------------- TIMER OPTIONS ----------------

    timers = [
        ("1 Minute", 60),
        ("2 Minutes (Default)", 120),
        ("5 Minutes", 300),
        ("10 Minutes", 600)
    ]

    for label, seconds in timers:

        is_active = INACTIVITY_LIMIT == seconds

        btn = tk.Button(
            container,
            text="✓ Currently Active" if is_active else label,
            command=lambda s=seconds, l=label: set_timer(s, l),
            bg="#1f2937" if is_active else "#111827",
            fg="#9ca3af" if is_active else "white",
            activebackground="#1f2937",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=22,
            font=("Segoe UI", 12),
            cursor="arrow" if is_active else "hand2",
            state="disabled" if is_active else "normal"
        )

        btn.pack(fill="x", pady=10)



def logout_user():

    global encryption_key
    global login_window
    global password_entry

    confirm = messagebox.askyesno(
        "Log Out",
        "Are you sure you want to log out?"
    )

    if not confirm:
        return

    # clear encryption key
    encryption_key = None

    # hide main app
    root.withdraw()

    # recreate login window
    login_window = tk.Toplevel(root)
    login_window.title("Secure Login")
    login_window.geometry("350x220")
    login_window.configure(bg="#030712")
    login_window.resizable(False, False)

    login_window.protocol("WM_DELETE_WINDOW", root.destroy)
    login_window.grab_set()
    login_window.focus_force()
    login_window.attributes("-topmost", True)

    # title
    tk.Label(
        login_window,
        text="Password Manager Login",
        font=("Segoe UI", 14, "bold"),
        fg="white",
        bg="#030712"
    ).pack(pady=15)

    tk.Label(
        login_window,
        text="Enter Master Password",
        fg="#9ca3af",
        bg="#030712"
    ).pack(pady=5)

    

    # ---------------- PASSWORD FIELD FRAME ----------------

    password_frame = tk.Frame(
        login_window,
        bg="#030712"
    )

    password_frame.pack(pady=10)

    password_entry = tk.Entry(
        password_frame,
        show="*",
        width=28,
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat",
        font=("Segoe UI", 11)
    )

    password_entry.pack(side="left", ipady=8)

    # ---------------- EYE TOGGLE ----------------

    show_password = False

    def toggle_password():

        nonlocal show_password

        show_password = not show_password

        if show_password:
            password_entry.config(show="")
            eye_button.config(text="🙈")
        
        else:
            password_entry.config(show="*")
            eye_button.config(text="👁")

    eye_button = tk.Button(
        password_frame,
        text="👁",
        command=toggle_password,
        bg="#111827",
        fg="white",
        activebackground="#1f2937",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI Emoji", 11)
    )

    eye_button.pack(side="left", padx=5)


    password_entry.bind(
        "<Return>",
        lambda event: check_password()
    )

    tk.Button(
        login_window,
        text="Login",
        width=15,
        command=check_password,
        bg="#7c3aed",
        fg="white",
        activebackground="#8b5cf6",
        relief="flat",
        cursor="hand2",
        font=("Segoe UI", 10, "bold")
    ).pack(pady=10)

def open_settings():

    hide_all_frames()
    
    settings_frame = tk.Frame(root, bg="#030712")
    settings_frame.pack(fill="both", expand=True)

    # ---------------- TOP BAR ----------------

    top_bar = tk.Frame(
        settings_frame,
        bg="#030712"
    )

    top_bar.pack(fill="x", padx=25, pady=20)

    tk.Button(
        top_bar,
        text="← Back",
        command=lambda: open_dashboard_safe(),
        bg="#111827",
        fg="white",
        activebackground="#1f2937",
        relief="flat",
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2",
        font=("Segoe UI", 10)
    ).pack(side="left")

    # ---------------- TITLE ----------------

    tk.Label(
        settings_frame,
        text="⚙ Settings",
        font=("Segoe UI", 24, "bold"),
        fg="white",
        bg="#030712"
    ).pack(pady=(10, 5))

    tk.Label(
        settings_frame,
        text="Manage your vault preferences",
        font=("Segoe UI", 10),
        fg="#9ca3af",
        bg="#030712"
    ).pack(pady=(0, 25))

    
    # ---------------- SCROLLABLE SETTINGS AREA ----------------

    main_frame = tk.Frame(
        settings_frame,
        bg="#030712"
    )

    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(
        main_frame,
        bg="#030712",
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        main_frame,
        orient="vertical",
        command=canvas.yview
    )

    scrollbar.pack(side="right", fill="y")

    canvas.pack(side="left", fill="both", expand=True)

    canvas.configure(yscrollcommand=scrollbar.set)

    container = tk.Frame(
        canvas,
        bg="#030712"
    )

    def mouse_scroll(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    root.bind_all("<MouseWheel>", mouse_scroll)

    canvas_window = canvas.create_window(
        (0, 0),
        window=container,
        anchor="nw"
    )

    def resize_canvas(event):
        canvas.itemconfig(
            canvas_window,
            width=event.width
        )
    
    canvas.bind("<Configure>", resize_canvas)

    

    def on_configure(event):
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    container.bind("<Configure>", on_configure)


    

    # bind to ALL widgets inside settings (this is the key fix)
    def bind_mousewheel(widget):
        widget.bind("<Enter>", lambda e: widget.focus_set())
        widget.bind("<MouseWheel>", mouse_scroll)

    bind_mousewheel(canvas)
    bind_mousewheel(container)




    def create_setting(text, command=None):

        btn = tk.Button(
            container,
            text=text,
            command=command,
            anchor="w",
            bg="#111827",
            fg="white",
            activebackground="#1f2937",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=22,
            font=("Segoe UI", 12),
            cursor="hand2"
        )

        btn.pack(fill="x", pady=8, padx=10)

        return btn

    # ---------------- SETTINGS ----------------

    create_setting("🔑 Change Master Password", change_master_password)

    create_setting("🛡 Recent Security Activity", open_security_activity)

    create_setting("⏱ Auto Lock Timer", change_auto_lock_timer)

    create_setting("📂 Sort Method", open_sort_settings)

    create_setting("🚪 Log Out", logout_user)

    create_setting("🗑 Delete All Entries", delete_all_entries)

    create_setting("⬇ Check For New Features", check_for_updates)

    create_setting("ℹ About App", about_app)


    



def about_app():

    about_window = tk.Toplevel(root)
    about_window.title("About App")
    
    about_window.configure(bg="#030712")

    window_width = 520
    window_height = 420

    screen_width = about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    about_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    about_window.transient(root)
    about_window.grab_set()
    about_window.focus_force()
    about_window.resizable(False, False)


    # ---------------- APP NAME ----------------

    tk.Label(
        about_window,
        text="VaultShield",
        font=("Segoe UI", 20, "bold"),
        fg="white",
        bg="#030712"
    ).pack(pady=(20, 5))

    # ---------------- TAGLINE ----------------

    tk.Label(
        about_window,
        text="Secure. Fast. Private.",
        font=("Segoe UI", 11),
        fg="#9ca3af",
        bg="#030712"
    ).pack(pady=(0, 15))

    # ---------------- DETAILS ----------------

    tk.Label(
        about_window,
        text=(
            "Version: 1.0.0\n\n"
            "VaultShield is a secure password manager designed to store, encrypt,\n"
            "and organize your credentials with a strong focus on privacy and control.\n\n"
            "All data is stored locally on your device. No cloud syncing. No external access.\n\n"
            "Built for speed, security, and a clean user experience.\n\n"
            "Developed by Jeyvin Derrick"
        ),
        font=("Segoe UI", 10),
        fg="white",
        bg="#030712",
        justify="center",
        wraplength=460  

    ).pack(padx=30)
        

    # ---------------- CLOSE BUTTON ----------------

    tk.Button(
        about_window,
        text="Close",
        command=about_window.destroy,
        bg="#7c3aed",
        fg="white",
        relief="flat",
        padx=18,
        pady=6,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2"
    ).pack(pady=20)


def open_security_activity():

    import json
    import os

    hide_all_frames()

    root.configure(bg="#030712")

    frame = tk.Frame(root, bg="#030712")
    frame.pack(fill="both", expand=True)

    # TOP BAR
    top = tk.Frame(frame, bg="#030712")
    top.pack(fill="x", padx=20, pady=20)

    tk.Button(
        top,
        text="← Back",
        command=open_settings,
        bg="#111827",
        fg="white",
        relief="flat",
        padx=15,
        pady=8
    ).pack(side="left")

    tk.Label(
        top,
        text="Recent Security Activity",
        font=("Segoe UI", 18, "bold"),
        fg="white",
        bg="#030712"
    ).pack(side="left", padx=20)

    # LOAD LOGS
    try:
        with open(SECURITY_LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    # SCROLL AREA
    canvas = tk.Canvas(frame, bg="#030712", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    scroll = tk.Scrollbar(frame, command=canvas.yview)
    scroll.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scroll.set)

    content = tk.Frame(canvas, bg="#030712")
    canvas.create_window((0, 0), window=content, anchor="nw")

    def on_configure(e):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content.bind("<Configure>", on_configure)

    if not logs:
        tk.Label(
            content,
            text="No security activity yet",
            fg="#9ca3af",
            bg="#030712",
            font=("Segoe UI", 12)
        ).pack(pady=40)
        return

    for log in reversed(logs):

        card = tk.Frame(content, bg="#111827", padx=15, pady=12)
        card.pack(fill="x", padx=20, pady=8)

        tk.Label(
            card,
            text=f"{log['event']}",
            fg="white",
            bg="#111827",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        tk.Label(
            card,
            text=f"{log['detail']}",
            fg="#9ca3af",
            bg="#111827"
        ).pack(anchor="w")

        tk.Label(
            card,
            text=f"{log['time']}",
            fg="#6b7280",
            bg="#111827",
            font=("Segoe UI", 9)
        ).pack(anchor="w")    

def delete_all_entries():

    confirm = messagebox.askyesno(
        "Delete All Entries",
        "⚠ This will permanently delete ALL saved passwords.\n\n"
        "This action cannot be undone.\n\n"
        "Do you want to continue?"
    )

    if not confirm:
        return

    # ---------------- SINGLE FLOW WINDOW ----------------

    flow_window = tk.Toplevel(root)
    flow_window.title("Delete All Entries")
    flow_window.geometry("420x300")
    flow_window.configure(bg="#030712")

    flow_window.transient(root)
    flow_window.grab_set()
    flow_window.focus_force()
    flow_window.resizable(False, False)

    container = tk.Frame(flow_window, bg="#030712")
    container.pack(fill="both", expand=True)

    # ---------------- PAGE 1: REASON ----------------

    tk.Label(
        container,
        text="Why are you deleting all entries?",
        font=("Segoe UI", 14, "bold"),
        fg="white",
        bg="#030712"
    ).pack(pady=20)

    reason_entry = tk.Text(
        container,
        height=5,
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat",
        font=("Segoe UI", 10)
    )

    reason_entry.pack(fill="x", padx=30, pady=10)

    def show_password_page():

        for widget in container.winfo_children():
            widget.destroy()

        tk.Label(
            container,
            text="Enter Master Password",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg="#030712"
        ).pack(pady=15)

        entry = tk.Entry(
            container,
            show="*",
            bg="#111827",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        entry.pack(pady=10, ipady=6)

        def final_delete():

            entered = entry.get()
            entered_hash = hashlib.sha256(entered.encode()).hexdigest()

            with open("data/master.txt", "r") as f:
                stored_hash = f.read().strip()

            if entered_hash != stored_hash:
                messagebox.showerror("Error", "Incorrect master password")
                return

            with open("data/vault.json", "w") as f:
                json.dump([], f)

            messagebox.showinfo(
                ("Deleted"),
                ("All entries have been permanently deleted.")
            )

            flow_window.destroy()

        tk.Button(
            container,
            text="Confirm Delete",
            command=final_delete,
            bg="#7c3aed",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            font=("Segoe UI", 10, "bold")
        ).pack(pady=15)

    def validate_reason():

        reason = reason_entry.get("1.0", "end").strip()

        invalid_reasons = ["idk", "none", "nothing", "123", "no", "yes"]

        if len(reason) < 15:
            messagebox.showwarning(
                ("invalid reason"),
                ("please provide a meaningful reason.")
            )
            return

        if reason.lower() in invalid_reasons:
            messagebox.showwarning(
                "Invalid Reason",
                "That reason is not acceptable."
            )
            return

        # ✅ MOVE TO NEXT STEP
        show_password_page()

    tk.Button(
        container,
        text="Continue",
        command=validate_reason,
        bg="#7c3aed",
        fg="white",
        relief="flat",
        padx=20,
        pady=8,
        font=("Segoe UI", 10, "bold")
    ).pack(pady=15)

def show_add_screen():

    add_window = tk.Toplevel(root)
    add_window.title("Add Entry")

    window_width = 380
    window_height = 560

    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    add_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    add_window.configure(bg="#030712")

    add_window.transient(root)
    add_window.grab_set()
    add_window.focus_force()
    add_window.resizable(False, False)

    tk.Label(
        add_window, text="Add New Entry", fg="white", bg="#030712",
         font=("Segoe UI", 16, "bold")
    ).pack(pady=15)

    

    tk.Label(add_window, text="Label *", fg="white", bg="#030712").pack(anchor="w", padx=40)
    
    label_entry = tk.Entry(
        add_window,
        width=34,
        font=("Segoe UI", 11),
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat"
    )
    label_entry.pack(pady=5, ipady=8)

    tk.Label(add_window, text="Username *", fg="white", bg="#030712").pack(anchor="w", padx=40)
    
    username_entry = tk.Entry(
        add_window,
        width=34,
        font=("Segoe UI", 11),
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat"
    )
    username_entry.pack(pady=5, ipady=8)


    tk.Label(add_window, text="Password *", fg="white", bg="#030712").pack(anchor="w", padx=40)
    
    # ---------------- PASSWORD FRAME ----------------

    password_frame = tk.Frame(
        add_window,
        bg="#030712"
    )

    password_frame.pack(pady=5)

    show_password = False

    password_entry = tk.Entry(
        password_frame,
        show="*",
        width=30,
        font=("Segoe UI", 11),
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat"
    )

    password_entry.pack(side="left", ipady=8)

    # ---------------- TOGGLE FUNCTION ----------------

    def toggle_password():

        nonlocal show_password

        show_password = not show_password

        if show_password:
            password_entry.config(show="")
            eye_button.config(text="🙈")

        else:
            password_entry.config(show="*")
            eye_button.config(text="👁")

    # ---------------- EYE BUTTON ----------------

    eye_button = tk.Button(
        password_frame,
        text="👁",
        command=toggle_password,
        bg="#111827",
        fg="white",
        activebackground="#1f2937",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI Emoji", 11)
    )

    eye_button.pack(side="left", padx=5)



    tk.Label(add_window, text="Category *", fg="#9ca3af", bg="#030712").pack(anchor="w", padx=40)
    tk.Label(
        add_window,
        text="(Optional)",
        fg="#9ca3af",
        bg="#030712",
        font=("Segoe UI", 8)
    ).pack()
    
    category_entry = tk.Entry(
        add_window,
        width=34,
        font=("Segoe UI", 11),
        bg="#111827",
        fg="white",
        insertbackground="white",
        relief="flat"
    )

    category_entry.pack(pady=5, ipady=8)

    def save():
        label = label_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        category = category_entry.get().strip()

        if not label:
            messagebox.showwarning("Missing Field", "Label is required.")
            return

        if not username:
            messagebox.showwarning("Missing Field", "Username is required.")
            return
        
        if not password:
            messagebox.showwarning("Missing Field", "Password is required.")
            return

        if not category:
            category = "Uncategorized"

        save_password(label, username, password, category)
        add_window.destroy()


    tk.Button(
        add_window,
        text="Save Entry",
        command=save,
        bg="#7c3aed",
        fg="white",
        relief="flat",
        padx=20,
        pady=10,
        font=("Segoe UI", 11, "bold")
    ).pack(pady=20)



# Main UI window






load_settings()




def start_app():

    global login_window

    try:
        login_window.destroy()

    except:
        pass

    if not os.path.exists("data/master.txt"):
        first_time_setup()

    else:
        show_login_window()
        
    print("STARTING APP...")

root.after(100, start_app)
root.mainloop()