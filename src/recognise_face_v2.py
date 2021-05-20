import face_recognition
import pickle
import cv2
import os


def recog():

    print("[INFO] loading encodings...")
    data = pickle.load(
        open(os.path.realpath("../encodings/encodings.p"), "rb"))
    print("[INFO] recognising faces")

    image = cv2.imread("../temp_images/photo.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(
        image, model="hog")
    encodings = face_recognition.face_encodings(image, boxes)

    name = None

    for encoding, locations in zip(encodings, boxes):
        matches = face_recognition.compare_faces(
            data["encodings"], encoding, tolerance=0.5)
        name = "Unknown"
        names = {}

        if True in matches:
            ids = [i for (i, b) in enumerate(matches) if b]
            for i in ids:
                name = data["names"][i]
                names[name] = names.get(name, 0) + 1

            name = max(names, key=names.get)

        top = locations[0]
        right = locations[1]
        bottom = locations[2]
        left = locations[3]

        cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 3)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

    cv2.imwrite(os.path.realpath("../temp_images/photo.jpg"), image)

    return name
