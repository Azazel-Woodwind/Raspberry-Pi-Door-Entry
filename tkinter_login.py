import tkinter as tk
from tkinter import messagebox
import sqlite3


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        with sqlite3.connect("logins.db") as db:

            cursor = db.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS details (
                        email TEXT NOT NULL,
                        password TEXT NOT NULL,
                        receive INTEGER NOT NULL)""")

            db.commit()

        self.update_logins()

        self.first = False if self.login_results else True

        container = tk.Frame(self)
        container.pack(expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (Login, Register):
            name = f.__name__
            frame = f(container, self)
            self.frames[name] = frame

        self.old_frame = "Login"

        if self.login_results:
            self.show_frame("Login")
        else:
            self.show_frame("Register")

    def show_frame(self, new_frame):
        self.frames[self.old_frame].grid_forget()
        try:
            self.frames[new_frame].grid()
        except:
            self.frames[self.old_frame].grid()
        else:
            self.old_frame = new_frame

    def update_logins(self):
        with sqlite3.connect("logins.db") as db:

            cur = db.cursor()

            cur.execute("SELECT * FROM details")

            self.login_results = cur.fetchall()


class Login(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.controller = controller

        self.email = tk.StringVar()
        self.password = tk.StringVar()

        self.widgets()

    def widgets(self):
        tk.Label(self, text="LOGIN", font=("Arial", 16, "bold")).grid()
        tk.Label(self, text="Email Address:").grid()
        tk.Entry(self, textvariable=self.email).grid(sticky="nsew")
        tk.Label(self, text="Password").grid()
        tk.Entry(self, textvariable=self.password,
                 show="*").grid(sticky="nsew")
        tk.Button(self, text="Sign in", command=self.login).grid()

    def login(self):
        email = self.email.get()
        pw = self.password.get()
        self.email.set("")
        self.password.set("")
        found = False
        for record in self.controller.login_results:
            if record[0] == email and record[1] == pw:
                found = True
                messagebox.showinfo("sdnif", "Login success!")
                self.controller.show_frame("TableView")
        if not found:
            messagebox.showinfo("bdfiw", "Incorrect username or password")


class Register(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.controller = controller

        self.email = tk.StringVar()
        self.email_con = tk.StringVar()
        self.password = tk.StringVar()
        self.password_con = tk.StringVar()
        self.var = tk.IntVar()
        self.var.set(-1)

        self.widgets()

    def widgets(self):
        tk.Label(self, text="REGISTER NEW USER").grid(columnspan=2)
        tk.Label(self, text="Email Address:").grid(columnspan=2)
        tk.Entry(self, textvariable=self.email).grid(
            columnspan=2, sticky="nsew")
        tk.Label(self, text="Confirm Email Address:").grid(columnspan=2)
        tk.Entry(self, textvariable=self.email_con).grid(
            columnspan=2, sticky="nsew")
        tk.Label(self, text="Password:").grid(columnspan=2)
        tk.Entry(self, textvariable=self.password,
                 show="*").grid(columnspan=2, sticky="nsew")
        tk.Label(self, text="Confirm Password:").grid(columnspan=2)
        tk.Entry(self, textvariable=self.password_con,
                 show="*").grid(columnspan=2, sticky="nsew")
        tk.Radiobutton(self, text="Receive an email when someone press doorbell",
                       variable=self.var, value=1).grid(columnspan=2)
        tk.Radiobutton(self, text="Do not receive an email when someone press doorbell",
                       variable=self.var, value=0).grid(columnspan=2)
        if not self.controller.first:
            tk.Button(self, text="Go back", command=lambda: self.controller.show_frame(
                "TableView")).grid(row=12, column=0)
            tk.Button(self, text="Register", command=self.check).grid(
                row=12, column=1)
        else:
            tk.Button(self, text="Register",
                      command=self.check).grid(columnspan=2)

    def check(self):
        message = ""
        if self.email.get() != self.email_con.get():
            message += "Emails do not match\n"
        if self.password.get() != self.password_con.get():
            message += "Passwords do not match\n"
        if self.var.get() == -1:
            message += "Please select whether you would like to receive emails"

        if message == "":
            self.register()
        else:
            messagebox.showwarning("fdsf", message)

    def register(self):
        email = self.email.get()
        password = self.password.get()
        self.email.set("")
        self.email_con.set("")
        self.password.set("")
        self.password_con.set("")
        with sqlite3.connect("logins.db") as db:

            cursor = db.cursor()

            cursor.execute("""INSERT OR IGNORE INTO details (email, password, receive)
                                VALUES (?, ?, ?)""", (email, password, self.var.get()))

            db.commit()

        messagebox.showinfo("fnsdind", "Register Success!")
        self.controller.update_logins()
        self.controller.show_frame("Login")


if __name__ == "__main__":
    app = App()
    app.mainloop()
