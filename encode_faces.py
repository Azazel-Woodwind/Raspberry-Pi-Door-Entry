import pickle
import sqlite3
import cv2
import face_recognition
from PIL import Image

def load_image(blob):
    with open("image.jpg", "wb") as file:
        file.write(blob)

def encode():

    print("[INFO] locating images...")

    with sqlite3.connect("test.db") as db:

        cursor = db.cursor()

        cursor.execute("SELECT image, person_id FROM images")

        result = cursor.fetchall()

    known_faces = []
    known_names = []

    for data in result:
        load_image(data[0])

        image = cv2.imread("image.jpg")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        box = face_recognition.face_locations(
            image, model="hog")
        encoding = face_recognition.face_encodings(image, box)
        known_faces.append(encoding[0])

        with sqlite3.connect("test.db") as db:

            cursor = db.cursor()

            cursor.execute("SELECT first_name FROM people WHERE person_id = ?", (data[1], ))

            name = cursor.fetchall()

        known_names.append(name[0][0])

    print("[INFO] serialising images...")
    data = {"encodings": known_faces, "names": known_names}
    pickle.dump(data, open("encodings.p", "wb"))

if __name__ == "__main__":
    encode()