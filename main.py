import customtkinter as ctk
import sqlite3
import bcrypt



key = b'rb5kDyTWLmw_x_Eb_aTUUVmUjVlKGH59ietNBjegyzs='

def is_admin(username):
    return username == "admin"


error_label = None
username_entry = None
password_entry = None

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
app = ctk.CTk()
app.geometry("500x400")
app.title("Login System")


def clear_window():
    for widget in app.winfo_children():
        widget.destroy()


def home(username):
    clear_window()

    title = ctk.CTkLabel(
        app,
        text=f"Welcome, {username}!",
        font=("Arial", 24)
    )
    title.pack(pady=30)

    logout_btn = ctk.CTkButton(
        app,
        text="Logout",
        command=login_screen
    )
    logout_btn.pack(pady=20)

def show_error(msg):
    global error_label
    if error_label:
        error_label.configure(text=msg)


def login():
    username = username_entry.get()
    password = password_entry.get()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    row = cursor.fetchone()

    if row and bcrypt.checkpw(password.encode(), row[0].encode()):
        if is_admin(username):
            admin_panel(username)
        else:
            home(username)
    else:
        show_error("Invalid login")

def login_screen():
    global username_entry
    global password_entry
    global message_label

    clear_window()

    title = ctk.CTkLabel(
        app,
        text="Login",
        font=("Arial", 28)
    )
    title.pack(pady=20)

    username_entry = ctk.CTkEntry(
        app,
        placeholder_text="Username",
        width=250
    )
    username_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(
        app,
        placeholder_text="Password",
        show="*",
        width=250
    )
    password_entry.pack(pady=10)

    login_btn = ctk.CTkButton(
        app,
        text="Login",
        command=login
    )
    login_btn.pack(pady=20)

    message_label = ctk.CTkLabel(
        app,
        text=""
    )
    message_label.pack()

def admin_panel(username):
    clear_window()

    # BACK BUTTON
    ctk.CTkButton(app, text="← Back", command=login_screen).pack(anchor="w", padx=10, pady=10)

    ctk.CTkLabel(app, text="Admin Panel", font=("Arial", 24)).pack(pady=10)

    # ADD USER
    frame = ctk.CTkFrame(app)
    frame.pack(pady=10)

    new_user = ctk.CTkEntry(frame, placeholder_text="Username")
    new_user.grid(row=0, column=0, padx=5)

    new_pass = ctk.CTkEntry(frame, placeholder_text="Password")
    new_pass.grid(row=0, column=1, padx=5)

    def add_user():
        u = new_user.get()
        p = new_pass.get()

        if not u or not p:
            return

        hashed = bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

        try:
            cursor.execute(
                "INSERT INTO users(username, password) VALUES (?, ?)",
                (u, hashed)
            )
            conn.commit()
            admin_panel(username)
        except:
            pass

    ctk.CTkButton(frame, text="Add", command=add_user).grid(row=0, column=2, padx=5)

    # USERS LIST
    list_frame = ctk.CTkFrame(app)
    list_frame.pack(fill="both", expand=True, pady=10)

    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()

    for uid, uname in users:
        row = ctk.CTkFrame(list_frame)
        row.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(row, text=uname, width=200, anchor="w").pack(side="left", padx=10)

        def delete(u=uid):
            cursor.execute("DELETE FROM users WHERE id=?", (u,))
            conn.commit()
            admin_panel(username)

        ctk.CTkButton(row, text="Delete", fg_color="red", command=delete).pack(side="right", padx=10)



login_screen()

app.mainloop()

conn.close()
