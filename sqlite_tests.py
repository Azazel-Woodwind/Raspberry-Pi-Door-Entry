import sqlite3


def create_table():
    with sqlite3.connect("test.db") as db:

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


def add_details_people():

    details = [
        ("Kai", "Strachan", "k.s@email.com"),
        ("Grandma", "Person", "b.b@email.com"),
        ("Nila", "Ten", "n.t@email.com")
    ]

    with sqlite3.connect("test.db") as db:

        cursor = db.cursor()

        cursor.executemany("""INSERT OR IGNORE INTO people (first_name, last_name, email)
                        VALUES (?, ?, ?)""", details)

        db.commit()


def add_details_images():

    path1 = r"/home/azazel/Documents/python_projects/face_recog/known_faces/Kai/IMG_20200220_181225.jpg"
    path2 = r"/home/azazel/Documents/python_projects/face_recog/known_faces/Grandma/IMG_20200726_111438_1.jpg"
    path3 = r"/home/azazel/Documents/python_projects/face_recog/known_faces/Nila/IMG_20200624_190754.jpg"

    image_details = [
        (cvt_to_blob(path1), 1),
        (cvt_to_blob(path2), 2),
        (cvt_to_blob(path3), 3)
    ]

    with sqlite3.connect("test.db") as db:

        cursor = db.cursor()

        cursor.executemany("""INSERT OR IGNORE INTO images (image, person_id)
                            VALUES (?, ?)""", image_details)

        db.commit()


def cvt_to_blob(filename):
    with open(filename, "rb") as file:
        blob = file.read()
    return blob


def refresh():
    with sqlite3.connect("test.db") as db:

        cursor = db.cursor()

        cursor.execute("DROP TABLE people")

        cursor.execute("DROP TABLE images")

        db.commit()

# create_table()

# add_details_people()

# add_details_images()


# with sqlite3.connect("test.db") as db:

#     cursor = db.cursor()

#     cursor.execute("SELECT * FROM people WHERE person_id = 3")

#     results = cursor.fetchall()

#     db.commit()

# refresh()
# create_table()
# add_details_people()
# add_details_images()

with sqlite3.connect("logins.db") as db:

    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS details (
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    receive INTEGER NOT NULL)""")

    db.commit()
