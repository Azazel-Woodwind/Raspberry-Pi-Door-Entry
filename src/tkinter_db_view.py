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

        try:
            file = open(os.path.realpath("../signal.txt"), "r")
        except:
            self.signal = False
        else:
            file.close()
            self.signal = True

        self.update_details()

        container = tk.Frame(self)
        container.pack(expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (TableView, EditForm, AddForm, PhotoView, EditSignal):
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

class EditSignal(tk.Frame):

    def __init__(self, parent, controller, **kw):
        tk.Frame.__init__(self, parent, **kw)

        self.controller = controller
        self.signal = tk.StringVar()
        self.signal_con = tk.StringVar()
        self.instructions = "To use this device, the receiver must be calibrated with the signal generated\n" + \
                        "from the doorbell. To do this, navigate to the terminal (ctrl+alt+t) and type the \n" + \
                        "following command exactly: cd Raspberry-Pi-Door-Entry/src && ./receiver.sh\n" + \
                        "Then, used the doorbell near the receiver, note the signal that is output on the \n" + \
                        "screen and input it into the entries below. If you change your doorbell, \n" + \
                        "you must do the same thing."

        # self.instructions = "To use this device, the receiver must be calibrated with the signal generated\n" + \
        #                 "from the doorbell. To do this, run receiver.sh in the src folder.\n" + \
        #                 "Then, used the doorbell near the receiver, note the signal that is output on the \n" + \
        #                 "screen and input it into the entries below. If you change your doorbell, \n" + \
        #                 "you must do the same thing."

        self.widgets()

    def widgets(self):
        tk.Label(self, text="Doorbell Signal", font=(
            "Arial", 20, "bold"), padx=20).grid(columnspan=2)
        tk.Label(self, text=self.instructions).grid(columnspan=2)
        tk.Label(self, text="Signal:").grid(columnspan=2)
        tk.Entry(self, textvariable=self.signal).grid(columnspan=2, sticky="nsew")
        tk.Label(self, text="Confirm signal:").grid(columnspan=2)
        tk.Entry(self, textvariable=self.signal_con).grid(columnspan=2, sticky="nsew")
        self.submit = tk.Button(self, text="Submit", command=self.check)
        self.go_back = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame(
            "TableView"))
        if self.controller.signal:
            self.go_back.grid(row=6, column=0)
            self.submit.grid(row=6, column=1)
        else:
            self.submit.grid(columnspan=2)

    def check(self):
        signal = self.signal.get()
        signal_con = self.signal_con.get()

        if len(signal) == 0 or len(signal_con) == 0:
            messagebox.showwarning("Angry", "Please enter signals")
        else:
            if self.signal.get() == self.signal_con.get():
                self.write_signal()
            else:
                messagebox.showwarning("No", "Signals must match")

    def write_signal(self):
        with open(os.path.realpath("../signal.txt"), "w") as file:
            file.write(str(self.signal.get()))

        messagebox.showinfo("Nice", "Signal registered successfully!")
        self.controller.show_frame("TableView")

        self.signal.set("")
        self.signal_con.set("")
        if not self.go_back.winfo_ismapped():
            self.submit.grid_forget()
            self.go_back.grid(row=6, column=0)
            self.submit.grid(row=6, column=1)


class TableView(tk.Frame):

    def __init__(self, parent, controller, **kw):
        tk.Frame.__init__(self, parent, **kw)

        self.controller = controller
        
        buttons = tk.Frame(self)
        buttons.grid(sticky="w")
        tk.Button(buttons, text="Register another user",
                  command=lambda: self.controller.show_frame("Register")).grid(
                      row=0, column=0, sticky="w")
        tk.Button(buttons, text="Edit doorbell signal", command=lambda: self.controller.show_frame(
            "EditSignal")).grid(row=0, column=1, sticky="w")
        tk.Button(buttons, text="Need help? Click me", command=self.help).grid(row=0, column=2, sticky="w")

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
                            (self.controller.results[self.rbuttons.get_int_var()][0],))

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
            f"Are you sure you want to associate photos: \n\n\
                    {image_names}\nwith record: \n\n{self.controller.results[record_num]}")

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

            messagebox.showinfo("Nice", "Photos added successfully!")

    def encode(self):
        choice = messagebox.askquestion(
            "Ok", "Are you sure you'd like to update encodings with current data?")

        if choice == "yes":
            info = tk.Label(self, text="Encoding faces...")
            info.grid()
            self.controller.update()
            encode_faces.encode()
            messagebox.showinfo("Nice", "Faces encoded successfully!")
            info.destroy()

    def help(self):
        message=\
            "ADD RECORD: This is the first button you want to use. This allows you to add the details of someone " + \
            "that you want to be recognised at the door.\nDELETE RECORD: This button can only be used when you " + \
            "select a record using the circular buttons at the side of them, and deletes the record you picked\n" + \
            "EDIT RECORD: This button allows you to edit the details of any record you picked with the cirular " + \
            "buttons.\nADD PHOTOS: This button brings you to your files and allows you to add images of the " + \
            "selected person to their record. This is needed if you want them to be recognised, and ideally, " + \
            "you should try to add 10 clear images of the person at different views and angles.\nVIEW PHOTOS: " + \
            "This button allows you to view and delete the photos that you added to the selected record.\n" + \
            "ENCODE DATA: This is a very important button. Whenever you add photos to any record, you must press " + \
            "this button sometime after or the images added will not be used when a photo is taken at the doorbell. " + \
            "Don't worry if this takes some time, as this is normal.\nREGISTER ANOTHER USER: This allows you to " + \
            "add another login so someone else can use the database and receive emails."            
        messagebox.showinfo("Help", message)


class Form(tk.Frame):

    def __init__(self, parent, controller, **kw):
        tk.Frame.__init__(self, parent, **kw)

        self.controller = controller

        self.title = tk.StringVar()
        self.id = tk.StringVar()
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.email = tk.StringVar()
        self.phone_num = tk.StringVar()

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
        tk.Label(self, text="Phone Number:").grid(columnspan=2)
        tk.Entry(self, textvariable=self.phone_num).grid(
            columnspan=2, sticky="nsew")
        tk.Button(self, text="Cancel", command=self.cancel).grid(
            row=12, column=0)

    def cancel(self):
        choice = messagebox.askquestion(
            "Cancel", "Are you sure you'd like to cancel?", icon="warning")

        if choice == "yes":
            self.controller.show_frame("TableView")
    
    def validate(self):
        message = ""

        if not self.first_name.get():
            message += "Please fill in a first name\n"
        if not self.last_name.get():
            message += "Please fill in a surname\n"
        if not self.email.get():
            message += "Please fill in an email\n"
        else:
            if not self.controller.is_valid(self.email.get()):
                message += "Please enter a valid email\n"
        if not self.phone_num.get():
            message += "Please fill in a phone number\n"
        else:
            if len(self.phone_num.get()) != 11 or not self.phone_num.get().isnumeric():
                message += "Please enter an 11 digit phone number"

        return message


class AddForm(Form):

    def __init__(self, parent, controller, **kw):
        Form.__init__(self, parent, controller, **kw)

        self.controller = controller

        self.title.set("ADD RECORD")

        tk.Button(self, text="Add", command=self.check).grid(
            row=12, column=1)

    def check(self):
        message = self.validate()
        if not message:
            self.add_record()
        else:
            messagebox.showerror("Bad", message)

    def add_record(self):
        choice = messagebox.askquestion(
            "Choice", "Are you sure you'd like to add a record with these details?\n" + \
                    "PLEASE NOTE: You must add photos of this person for them to be recognised.")
        if choice == "yes":
            with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

                cur = db.cursor()

                cur.execute("PRAGMA foreign_keys = ON;")

                db.commit()

                cur.execute("""INSERT INTO people (first_name, last_name, email, phone_num)
                                VALUES (?, ?, ?, ?)""", (self.first_name.get(), self.last_name.get(), 
                                                        self.email.get(), self.phone_num.get()))

                db.commit()

            messagebox.showinfo("Success", "Record added successfully!")

            self.controller.update_details()
            self.controller.frames["TableView"].refresh()
            self.controller.show_frame("TableView")
            self.first_name.set("")
            self.last_name.set("")
            self.email.set("")
            self.phone_num.set("")

    def update_id(self):
        try:
            self.id.set(self.controller.results[-1][0] + 1)
        except IndexError:
            self.id.set(1)


class EditForm(Form):

    def __init__(self, parent, controller, **kw):
        Form.__init__(self, parent, controller, **kw)

        self.controller = controller

        self.title.set("ENTER CHANGES")

        tk.Button(self, text="Confirm Changes",
                  command=self.check).grid(row=12, column=1)

    def update(self):
        record_num = self.controller.frames["TableView"].rbuttons.get_int_var()
        record = self.controller.results[record_num]
        for detail, field in zip(record, (self.id, self.first_name, 
                                self.last_name, self.email, self.phone_num)):
            field.set(detail)

    def check(self):
        message = self.validate()
        if message:
            messagebox.showerror("Again", message)
        else:
            self.edit()

    def edit(self):
        choice = messagebox.askquestion(
            "Confirm", "Are you sure you'd like to confirm these changes?", icon="warning")
        if choice == "yes":
            with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

                cur = db.cursor()

                cur.execute("""UPDATE people
                                SET first_name = ?,
                                    last_name = ?,
                                    email = ?,
                                    phone_num = ?
                                WHERE person_id = ?""",
                            (self.first_name.get(), self.last_name.get(), self.email.get(), 
                            self.phone_num.get(), self.id.get()))

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

        #add headings
        for column, heading in enumerate(["Unique ID", "Forename", "Surname", "Email Address", "Phone Number"]):
            tk.Label(self, text=heading, font=("Arial", 20, "bold"), padx=25).grid(
                row=0, column=column, padx=1, pady=1, sticky="nsew")

        #add information
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


        tk.Button(self, text="Add Record",
                  command=lambda: [controller.frames["AddForm"].update_id(), 
                    controller.show_frame("AddForm")]).grid(row=0, column=0, padx=5)

        for column, text in enumerate(["Delete Record", "Edit Record", "Add Photos", "View Photos"], start=1):
            tk.Label(self, text=text, bg="gray40",
                     fg="gray25", padx=10, pady=4).grid(row=0, column=column, padx=5)
                    
        tk.Button(self, text="Encode data",
            command=self.parent.encode).grid(row=0, column=5, padx=5)

    def highlight_button(self):
        for column, text in enumerate([("Delete Record", self.parent.del_record),
                                       ("Edit Record", lambda: [self.controller.frames["EditForm"].update(
                                       ), self.controller.show_frame("EditForm")]),
                                       ("Add Photos", self.parent.add_photos),
                                       ("View Photos",
                                        lambda: [self.controller.frames["PhotoView"].update(),
                                                 self.controller.show_frame("PhotoView")])], start=1):
            tk.Button(self, text=text[0], command=text[1]).grid(
                row=0, column=column)

        self.isDark = False


if __name__ == "__main__":
    app = App()
    app.mainloop()
