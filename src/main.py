import tkinter as tk
import sqlite3
from tkinter_login import Login, Register, Welcome
from tkinter_db_view import EditSignal, TableView, EditForm, AddForm, PhotoView, Form, RadioButtons, Options, Table
import os
import re

class App(tk.Tk):

    def __init__(self, *args, **kw):
        tk.Tk.__init__(self, *args, **kw)

        self.title("Database Management")

        #create database and tables for person details
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
        #create separate database for login information
        with sqlite3.connect(os.path.realpath("../databases/logins.db")) as db:

            cursor = db.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS details (
                            email TEXT NOT NULL,
                            password TEXT NOT NULL,
                            receive INTEGER NOT NULL)""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS sender (
                            email TEXT NOT NULL,
                            password TEXT NOT NULL)""")

            cursor.execute("SELECT * FROM sender")

            sender = cursor.fetchall()

            db.commit()

        try:
            file = open(os.path.realpath("../signal.txt"), "r")
        except:
            self.signal = False
        else:
            file.close()
            self.signal = True

        #gather information from tables on startup to be used by other
        #classes.
        self.update_details()
        self.update_logins()

        #creates frame that contains all pages that stays in the 
        #middle of all the screen
        container = tk.Frame(self)
        container.pack(expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #initialises dictionary relating page name to
        #its respective frame for page switching
        self.frames = {}

        #loops through all frame classes
        #corresponding to each page
        for f in (TableView, EditForm, AddForm, PhotoView, Login, Register, Welcome, EditSignal):
            page_name = f.__name__

            #initialises instance of each frame and
            #places in container made. Passes current
            #instance as a parameter so the frame can access the "parent"
            frame = f(container, self)

            #adds to dictionary
            self.frames[page_name] = frame

        self.old_frame = "Login"

        if sender:
            if self.login_results:
                self.show_frame("Login")
            else:
                self.show_frame("Register")
        else:
            self.show_frame("Welcome")

    def update_details(self):

        """creates array attribute of current records 
            on authorised persons"""

        with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

            cur = db.cursor()

            cur.execute("SELECT * FROM people")

            db.commit()

            self.results = cur.fetchall()

    def show_frame(self, new_frame):

        """Switches the visible frame"""

        #deletes old frame, grids new frame,
        #sets new frame as old frame
        self.frames[self.old_frame].grid_forget()
        self.frames[new_frame].grid()
        self.old_frame = new_frame

    def cvt_to_blob(self, filename):
        with open(filename, "rb") as file:
            blob = file.read()
        return blob

    def update_logins(self):

        """creates array attribute of current records 
            on login details"""

        with sqlite3.connect(os.path.realpath("../databases/logins.db")) as db:

            cur = db.cursor()

            cur.execute("SELECT * FROM details")

            self.login_results = cur.fetchall()

    @staticmethod
    def validate(email, email_con, pw, pw_con, reg=True):
        message = ""

        #first checks if any fields empty
        if not email or not email_con or not pw or not pw_con:
            return "Please fill in the required fields"
        else:
            #checks if the confirm fields match original
            if email != email_con:
                message += "Emails do not match\n"
            else:
                #if so, validate that a real email with regex format checking
                if not re.search(".+@.+\..+", email):
                    message += "Enter a valid email\n"
            #same with password
            if pw != pw_con:
                message += "Passwords do not match\n"
            else:
                if not reg:
                    return message
                #length check
                if not (8 <= len(pw) <= 20):
                    message += "Password must be between 8 and 20 characters long\n"
                #format check
                upper=lower=spc=num=False
                for ch in pw:
                    if ch.isupper():
                        upper = True
                    elif ch.islower():
                        lower = True
                    elif ch.isnumeric():
                        num = True
                    else:
                        spc = True
                if not (upper and lower and spc and num):
                    message += "Password must contain at least 1 lowercase letter," +\
                        "1 upper case letter, 1 number and 1 special character"
        return message
                
if __name__ == "__main__":
    app = App()
    app.mainloop()
