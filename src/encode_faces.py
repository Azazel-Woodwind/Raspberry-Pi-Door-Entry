import pickle
import sqlite3
import cv2
import face_recognition
from PIL import Image
import os


def load_image(blob):
    with open(os.path.realpath("../temp_images/image.jpg"), "wb") as file:
        file.write(blob)


def encode():

    print("[INFO] locating images...")

    with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

        cursor = db.cursor()

        cursor.execute("SELECT image, person_id FROM images")

        result = cursor.fetchall()

    known_faces = []
    known_names = []

    count = 1

    for data in result:
        load_image(data[0])

        image = cv2.imread(os.path.realpath("../temp_images/image.jpg"))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        box = face_recognition.face_locations(
            image, model="hog")
        encoding = face_recognition.face_encodings(image, box)
        try:
            known_faces.append(encoding[0])
        except:
            print(f"NO FACE FOUND IN PHOTO {count}")
            count += 1
            continue

        with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

            cursor = db.cursor()

            cursor.execute(
                "SELECT first_name FROM people WHERE person_id = ?", (data[1], ))

            name = cursor.fetchall()

        known_names.append(name[0][0])

    print("[INFO] serialising images...")
    data = {"encodings": known_faces, "names": known_names}
    pickle.dump(data, open(os.path.realpath("../encodings/encodings.p"), "wb"))


if __name__ == "__main__":
    encode()
