import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
from PIL import Image
import encode_faces
import os


class App(tk.Tk):

    def __init__(self, *args, **kw):
        tk.Tk.__init__(self, *args, **kw)

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

        self.update_details()

        container = tk.Frame(self)
        container.pack(expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (TableView, EditForm, AddForm, PhotoView):
            page_name = f.__name__
            frame = f(container, self)
            self.frames[page_name] = frame

        self.old_frame = "TableView"

        self.show_frame("TableView")

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


class TableView(tk.Frame):

    def __init__(self, parent, controller, **kw):
        tk.Frame.__init__(self, parent, **kw)

        self.controller = controller

        tk.Button(self, text="Register another user",
                  command=lambda: self.controller.show_frame("Register")).grid(sticky="w")

        self.draw_table()

    def highlight_button(self):
        if self.opts.isDark:
            self.opts.highlight_button()

    def refresh(self):
        self.table.destroy()
        self.rbuttons.destroy()
        self.opts.destroy()
        self.draw_table()

    def draw_table(self):

        self.table = Table(self, self.controller)
        self.table.grid(row=1, column=0)

        self.rbuttons = RadioButtons(self, self.controller)
        self.rbuttons.grid(row=1, column=1)

        self.opts = Options(self, self.controller)
        self.opts.grid(row=2)

    def del_record(self):
        choice = messagebox.askquestion(
            "Delete",
            f"Are you sure you'd like to delete record {self.controller.results[int(self.rbuttons.get_int_var())]}?",
            icon="warning")

        if choice == "yes":
            with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

                cur = db.cursor()

                cur.execute("PRAGMA foreign_keys = ON;")

                db.commit()

                cur.execute("DELETE FROM people WHERE person_id = ?",
                            (self.rbuttons.get_int_var()+1,))

                db.commit()

        self.controller.update_details()
        self.refresh()

    def update_edit_form(self):
        record_num = self.rbuttons.get_int_var()
        self.controller.frames["EditForm"].update(record_num)
        self.controller.show_frame("EditForm")

    def add_photos(self):
        self.details = filedialog.askopenfilenames(
            initialdir="..",
            title="Select file", filetypes=[("Images", ".jpg .JPG .png")])
        record_num = self.rbuttons.get_int_var()

        image_names = ""

        for image in self.details:
            temp = image.split("/")
            image_names += temp[-1] + "\n"

        choice = messagebox.askquestion(
            "Add photos",
            f"Are you sure you want to associate photos: \n\n{image_names}\nwith record: \n\n{self.controller.results[record_num]}")

        if choice == "yes":
            with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

                cur = db.cursor()

                cur.execute("PRAGMA foreign_keys = ON;")

                db.commit()

                unique_id = record_num + 1

                for path in self.details:
                    blob = self.controller.cvt_to_blob(path)
                    cur.execute("""INSERT INTO images (image, person_id)
                                    VALUES (?, ?)""", (blob, unique_id))

                    db.commit()

            messagebox.showinfo("efew", "Photos added successfully!")

    def encode(self):
        choice = messagebox.askquestion(
            "adfs", "Are you sure you'd like to update encodings with current data?")

        if choice == "yes":
            info = tk.Label(self, text="Encoding faces...")
            info.grid()
            self.controller.update()
            encode_faces.encode()
            messagebox.showinfo("dsf", "faces encoded successfully!")
            info.destroy()


class Form(tk.Frame):

    def __init__(self, parent, controller, **kw):
        tk.Frame.__init__(self, parent, **kw)

        self.controller = controller

        self.title = tk.StringVar()
        self.id = tk.StringVar()
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.email = tk.StringVar()

        self.widgets()

    def widgets(self):
        tk.Label(self, textvariable=self.title, font=(
            "Arial", 20, "bold"), padx=20).grid(columnspan=2)
        tk.Label(self, text="UNIQUE ID:").grid(columnspan=2)
        tk.Label(self, textvariable=self.id).grid(columnspan=2)
        tk.Label(self, text="First Name:").grid(columnspan=2)
        tk.Entry(self, textvariable=self.first_name).grid(
            columnspan=2, sticky="nsew")
        tk.Label(self, text="Last name:").grid(columnspan=2)
        tk.Entry(self, textvariable=self.last_name).grid(
            columnspan=2, sticky="nsew")
        tk.Label(self, text="Email Address:").grid(columnspan=2)
        tk.Entry(self, textvariable=self.email).grid(
            columnspan=2, sticky="nsew")
        tk.Button(self, text="Cancel", command=self.cancel).grid(
            row=10, column=0)

    def cancel(self):
        choice = messagebox.askquestion(
            "Cancel", "Are you sure you'd like to cancel?", icon="warning")

        if choice == "yes":
            self.controller.show_frame("TableView")


class AddForm(Form):

    def __init__(self, parent, controller, **kw):
        Form.__init__(self, parent, controller, **kw)

        self.controller = controller

        self.title.set("ADD RECORD")

        tk.Button(self, text="Add", command=self.add_record).grid(
            row=10, column=1)

    def clear(self):
        try:
            self.id.set(
                str(self.controller.results[-1][0] + 1))
        except IndexError:
            self.id.set(1)
        self.first_name.set("")
        self.last_name.set("")
        self.email.set("")

    def add_record(self):
        choice = messagebox.askquestion(
            "dscsdf", "Are you sure you'd like to add a record with these details?\nPLEASE NOTE: You must add photos of this person for them to be recognised.")
        if choice == "yes":
            with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

                cur = db.cursor()

                cur.execute("PRAGMA foreign_keys = ON;")

                db.commit()

                cur.execute("""INSERT INTO people (first_name, last_name, email)
                                VALUES (?, ?, ?)""", (self.first_name.get(), self.last_name.get(), self.email.get()))

                db.commit()

            messagebox.showinfo("efew", "Record added successfully!")

            self.controller.update_details()
            self.controller.frames["TableView"].refresh()
            self.controller.show_frame("TableView")


class EditForm(Form):

    def __init__(self, parent, controller, **kw):
        Form.__init__(self, parent, controller, **kw)

        self.controller = controller

        self.title.set("ENTER CHANGES")

        tk.Button(self, text="Confirm Changes",
                  command=self.edit).grid(row=10, column=1)

    def update(self):
        record_num = self.controller.frames["TableView"].rbuttons.get_int_var()
        record = self.controller.results[record_num]
        for detail, field in zip(record, (self.id, self.first_name, self.last_name, self.email)):
            field.set(detail)

    def edit(self):
        choice = messagebox.askquestion(
            "Confirm", "Are you sure you'd like to confirm these changes?", icon="warning")
        if choice == "yes":
            with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

                cur = db.cursor()

                cur.execute("""UPDATE people
                                SET first_name = ?,
                                    last_name = ?,
                                    email = ?
                                WHERE person_id = ?""",
                            (self.first_name.get(), self.last_name.get(), self.email.get(), self.id.get()))

                db.commit()

        self.controller.update_details()
        self.controller.frames["TableView"].refresh()
        self.controller.show_frame("TableView")


class PhotoView(tk.Frame):

    def __init__(self, parent, controller, **kw):
        tk.Frame.__init__(self, parent, **kw)

        self.controller = controller
        self.title = tk.StringVar()

        tk.Label(self, textvariable=self.title,
                 font=("Arial", 16, "bold")).grid()
        self.images = tk.Frame(self)
        self.images.grid()

    def update(self):
        record = self.controller.results[self.controller.frames["TableView"].rbuttons.get_int_var(
        )]

        name = record[1] + " " + record[2]

        self.images.destroy()
        self.images = tk.Frame(self)
        self.images.grid()

        with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

            cur = db.cursor()

            cur.execute(
                """SELECT image FROM images WHERE person_id = ?""", (record[0], ))

            self.image_blobs = cur.fetchall()

            db.commit()

        if self.image_blobs:
            self.title.set("Images of " + name)
            self.image = tk.IntVar()

            for row in range(len(self.image_blobs)):
                tk.Label(
                    self.images, text=f"Photo {row + 1}").grid(row=row, column=1)
                tk.Radiobutton(self.images, variable=self.image,
                               value=row).grid(row=row, column=1, columnspan=2)

            new_row = len(self.image_blobs)

            tk.Button(self.images, text="Back",
                      command=lambda: self.controller.show_frame("TableView")).grid(row=new_row, column=0)

            tk.Button(self.images, text="View image",
                      command=self.open_image).grid(row=new_row, column=1)

            tk.Button(self.images, text="Delete image",
                      command=self.del_img).grid(row=new_row, column=2)

        else:
            self.title.set("No images of " + name + " :(")
            tk.Button(self.images, text="Back to Table",
                      command=lambda: self.controller.show_frame("TableView")).grid()

    def open_image(self):
        image = self.image.get()
        with open(os.path.realpath("../temp_images/image.jpg"), "wb") as file:
            file.write(self.image_blobs[image][0])
        im = Image.open(os.path.realpath("../temp_images/image.jpg"))
        im.show()

    def del_img(self):
        choice = messagebox.askquestion(
            "hello", "Are you sure you want to delete this photo?", icon="warning")
        if choice == "yes":
            image = self.image.get()
            with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

                cursor = db.cursor()

                cursor.execute("DELETE FROM images WHERE image = ?",
                               (self.image_blobs[image]))

                db.commit()

        self.update()


class Table(tk.Frame):

    def __init__(self, parent, controller, **kw):
        tk.Frame.__init__(self, parent, **kw)

        self["background"] = "black"

        for column, heading in enumerate(["Unique ID", "Forename", "Surname", "Email Address"]):
            tk.Label(self, text=heading, font=("Arial", 20, "bold"), padx=25).grid(
                row=0, column=column, padx=1, pady=1, sticky="nsew")

        for row, record in enumerate(controller.results, start=1):
            for column, detail in enumerate(record):
                tk.Label(self, text=detail, anchor="w", font=("Arial", 14)).grid(
                    row=row, column=column, padx=1, pady=1, sticky="nsew")


class RadioButtons(tk.Frame):

    def __init__(self, parent, controller, **kw):
        tk.Frame.__init__(self, parent, **kw)

        self.var = tk.IntVar()
        self.var.set(-1)

        tk.Label(self, text="", font=(
            "Arial", 20, "bold")).grid(pady=1)
        for button in range(len(controller.results)):
            tk.Radiobutton(self, variable=self.var, value=button,
                           font=("Arial", 14), command=lambda: parent.highlight_button()).grid(pady=1)

    def get_int_var(self):
        return self.var.get()


class Options(tk.Frame):

    def __init__(self, parent, controller, **kw):
        tk.Frame.__init__(self, parent, **kw)

        self.controller = controller

        self.parent = parent
        self.isDark = True

        tk.Button(self, text="Encode data",
                  command=self.parent.encode).grid(row=0, column=0, padx=5)

        tk.Button(self, text="Add Record",
                  command=lambda: [controller.frames["AddForm"].clear(), controller.show_frame("AddForm")]).grid(row=0, column=1, padx=5)

        for column, text in enumerate(["Delete Record", "Edit Record", "Add Photos", "View Photos"], start=2):
            tk.Label(self, text=text, bg="gray40",
                     fg="gray25", padx=10, pady=4).grid(row=0, column=column, padx=5)

    def highlight_button(self):
        for column, text in enumerate([("Delete Record", self.parent.del_record),
                                       ("Edit Record", lambda: [self.controller.frames["EditForm"].update(
                                       ), self.controller.show_frame("EditForm")]),
                                       ("Add Photos", self.parent.add_photos),
                                       ("View Photos",
                                        lambda: [self.controller.frames["PhotoView"].update(),
                                                 self.controller.show_frame("PhotoView")])], start=2):
            tk.Button(self, text=text[0], command=text[1]).grid(
                row=0, column=column)

        self.isDark = False


if __name__ == "__main__":
    app = App()
    app.mainloop()
