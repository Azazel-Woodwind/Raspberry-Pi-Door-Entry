import pickle
import sqlite3
import cv2
import face_recognition
from PIL import Image
import os


def load_image(blob):

    """ Writes image file"""

    with open(os.path.realpath("../temp_images/image.jpg"), "wb") as file:
        file.write(blob)


def encode():

    """Encodes faces"""

    print("[INFO] locating images...")

    #fetches image BLOBs and their IDs from database
    with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

        cursor = db.cursor()

        cursor.execute("SELECT image, person_id FROM images")

        result = cursor.fetchall() 

    #arrays to store encodings and names
    known_faces = []
    known_names = [] 

    count = 0 #keeps count of image number

    #loops through records
    for data in result: 
        count += 1
        load_image(data[0]) #writes image to file

        # load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(os.path.realpath("../temp_images/image.jpg")) 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #detect (x,y) coordinates of boxes 
        #corresponding to each face
        box = face_recognition.face_locations(
            image, model="hog")
        #compute encodings for each face found
        encoding = face_recognition.face_encodings(image, box)
        #check if encoding exists by trying to add to array
        #if not, user notified of which image, loops to next image
        try:
            known_faces.append(encoding[0])
        except:
            print(f"NO FACE FOUND IN IMAGE {count}")
            continue

        #find name corresponding to image
        with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

            cursor = db.cursor()

            cursor.execute(
                "SELECT first_name FROM people WHERE person_id = ?", (data[1], ))

            name = cursor.fetchall()

        #add name to array in same position
        known_names.append(name[0][0])

    #create pickle file with encodings
    print("[INFO] serialising images...")
    data = {"encodings": known_faces, "names": known_names}
    pickle.dump(data, open(os.path.realpath("../encodings/encodings.p"), "wb"))


if __name__ == "__main__":
    encode()
