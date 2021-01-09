import tkinter as tk
import sqlite3
from tkinter_login import Login, Register, Welcome
from tkinter_db_view import TableView, EditForm, AddForm, PhotoView, Form, RadioButtons, Options, Table
import os


class App(tk.Tk):

    def __init__(self, *args, **kw):
        tk.Tk.__init__(self, *args, **kw)

        self.title("Database")

        with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

            cursor = db.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS people (
                            person_id INTEGER PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT,
                            email TEXT
                            )""")

            db.commit()

            cursor.execute("""CREATE TABLE IF NOT EXISTS images (
                            image BLOB,
                            person_id INTEGER,
                            FOREIGN KEY (person_id)
                                REFERENCES people (person_id)
                                    ON UPDATE CASCADE
                                    ON DELETE CASCADE
                            )""")

            db.commit()

        with sqlite3.connect(os.path.realpath("../databases/logins.db")) as db:

            cursor = db.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS details (
                            email TEXT NOT NULL,
                            password TEXT NOT NULL,
                            receive INTEGER NOT NULL)""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS sender (
                            email TEXT NOT NULL,
                            password TEXT NOT NULL)""")

            db.commit()

        self.update_details()
        self.update_logins()

        container = tk.Frame(self)
        container.pack(expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.first = False if self.login_results else True

        for f in (TableView, EditForm, AddForm, PhotoView, Login, Register, Welcome):
            page_name = f.__name__
            frame = f(container, self)
            self.frames[page_name] = frame

        self.old_frame = "Login"

        if self.login_results:
            self.show_frame("Login")
        else:
            self.show_frame("Welcome")

    def update_details(self):
        with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

            cur = db.cursor()

            cur.execute("SELECT * FROM people")

            db.commit()

            self.results = cur.fetchall()

    def show_frame(self, new_frame):
        self.frames[self.old_frame].grid_forget()
        try:
            self.frames[new_frame].grid()
        except:
            self.frames[self.old_frame].grid()
        else:
            self.old_frame = new_frame

    def cvt_to_blob(self, filename):
        with open(filename, "rb") as file:
            blob = file.read()
        return blob

    def update_logins(self):
        with sqlite3.connect(os.path.realpath("../databases/logins.db")) as db:

            cur = db.cursor()

            cur.execute("SELECT * FROM details")

            self.login_results = cur.fetchall()


if __name__ == "__main__":
    app = App()
    app.mainloop()
