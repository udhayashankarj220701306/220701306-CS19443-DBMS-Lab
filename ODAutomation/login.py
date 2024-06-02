import tkinter
from tkinter import messagebox, ttk
from hashlib import sha256
from configs import config
import sv_ttk
from home import home
import threading

class User:
    def __init__(self, id, name, email, phno, role=None):
        self.id = id
        self.name = name
        self.email = email
        self.phno = phno
        self.role = role

curr_user = None
def connect():
    global con
    print(1111)
    con=config()
    print(2222)
def passhash(password):
    return sha256(password.encode('utf-8')).hexdigest()

def authentication(email, password, parent):
    def connect_and_authenticate():
        print("before")
        cur = con.cursor()
        print("after")
        cur.execute(f"SELECT id, username, email, phno FROM users WHERE email='{email}' AND password='{passhash(password)}'")
        user = cur.fetchone()
        print(user)
        if user:
            user_id = user[0]
            role = 0
            cur.execute(f"""
                            SELECT -1 AS role FROM students WHERE user_id = {user_id}
                            UNION
                            SELECT 1 AS role FROM class WHERE incharge_id = {user_id}
                            UNION
                            SELECT 2 AS role FROM class WHERE counselor_id = {user_id}
                            UNION
                            SELECT 3 AS role FROM dept WHERE hod_id = {user_id}
                        """)
            role_result = cur.fetchone()
            print(role_result)
            if role_result:
                role = role_result[0]

            global curr_user
            curr_user = User(user[0], user[1], user[2], user[3], role)
            if role == -1:
                print("Student logged in")
            else:
                print("Staff logged in")

            parent.destroy()
            home(root, curr_user, con)

        else:
            print("logging failed")
            messagebox.showerror("Login Failed", "Invalid username or password")

    threading.Thread(target=connect_and_authenticate).start()

def on_focus_in(entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, 'end')

def on_focus_out(entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        if placeholder == 'Password\t':
            entry.configure(show="")
    else:
        if placeholder == 'Password\t':
            entry.configure(show="*")

class Login(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame", padding=15)

        self.columnconfigure(0, weight=1)
        threading.Thread(target=connect).start()
        self.add_widgets(parent)

    def add_widgets(self, parent):
        self.email = ttk.Entry(self)
        self.email.insert(0, "Email\t")
        self.email.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")

        self.password = ttk.Entry(self)
        self.password.insert(0, "Password\t")
        self.password.grid(row=2, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.email.bind('<Button-1>', lambda x: on_focus_in(self.email, "Email\t"))
        self.email.bind('<FocusOut>', lambda x: on_focus_out(self.email, "Email\t"))

        self.password.bind('<Button-1>', lambda x: on_focus_in(self.password, "Password\t"))
        self.password.bind('<FocusOut>', lambda x: on_focus_out(self.password, "Password\t"))

        self.separator = ttk.Separator(self)
        self.separator.grid(row=5, column=0, pady=10, sticky="ew")

        self.login = ttk.Button(self, text="LOG IN", style="Accent.TButton", command=lambda: authentication(self.email.get(), self.password.get(), parent))
        self.login.grid(row=7, column=0, padx=5, pady=10, sticky="ew")


class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        label = ttk.Label(self, text="")
        label.grid(row=0, column=0)
        big_font_label = ttk.Label(self, text="REC", font=("Arial", 30, "bold"), foreground="#56C8FF")
        big_font_label.grid(row=1, column=1)
        Login(self).grid(row=2, column=1, padx=10, pady=(10, 0), sticky="nsew")
        label = ttk.Label(self, text="")
        label.grid(row=3, column=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=0, minsize=200)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=400)
        self.grid_columnconfigure(2, weight=1)

root = tkinter.Tk()
root.title("Login")

sv_ttk.set_theme("dark")
App(root).pack(expand=True, fill="both")

root.mainloop()

