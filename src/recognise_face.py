import face_recognition
import pickle
import cv2
import os


def recog():

    print("[INFO] loading encodings...")
    #fetch data from pickle file
    data = pickle.load(
        open(os.path.realpath("../encodings/encodings.p"), "rb"))
    print("[INFO] recognising faces")

    #load OpenCV's Haar Cascade
    detector = cv2.CascadeClassifier("../haarcascade_frontalface_default.xml")

    #load image taken from pi and convert it 
    #(1) to grayscale for the detection method
    #and (2) to RGB for face recognition    
    image = cv2.imread("../temp_images/photo.jpg")
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #detect faces in the grayscale image
    rects = detector.detectMultiScale(grey, scaleFactor = 1.1, 
        minNeighbors=5, minSize=(30,30))

    #reformat the coordinates for face recognition
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    #compute encodings for each face
    encodings = face_recognition.face_encodings(image, boxes)

    #declares default name as none as
    #a face may not be found at all
    name = None

    #in the case of multiple faces detected
    #loop through each encoding and its corresponding 
    #bounding box
    for encoding, locations in zip(encodings, boxes):

        #returns array of booleans: True if the encoding
        #found in image is similar to the encoding in the 
        #repository or False if they are too different
        matches = face_recognition.compare_faces(
            data["encodings"], encoding, tolerance=0.5)

        #default name now becomes "unknown" as a face is found
        #but the name is not known
        name = "Unknown"

        #dictionary used to count number of times each 
        #face was matched
        names = {}

        #if at least one match has been found
        if True in matches:
            #find indexes of all matched faces
            ids = [i for (i, b) in enumerate(matches) if b]

            #loop through indexes and maintain count
            #for each recognised face
            for i in ids:
                name = data["names"][i]
                names[name] = names.get(name, 0) + 1

            #determine name with most amount of counts
            name = max(names, key=names.get)

        #initialise coordinates of box
        top = locations[0]
        right = locations[1]
        bottom = locations[2]
        left = locations[3]

        #draw box and add name
        cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 3)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

    #write the new image to a temp image file to be used later
    cv2.imwrite(os.path.realpath("../temp_images/photo.jpg"), image)

    #return name to be used in email
    return name
