import smtplib
import imghdr
from email.message import EmailMessage
from datetime import datetime
import sqlite3
import os
import recognise_face
import recognise_face_v2


def send():

    with sqlite3.connect(os.path.realpath("../databases/logins.db")) as db:

        cursor = db.cursor()

        cursor.execute("SELECT * FROM sender")

        result = cursor.fetchall()

    SENDER = result[0][0]
    PASS = result[0][1]

    #name = recognise_face.recog()
    name = recognise_face_v2.recog()

    with sqlite3.connect(os.path.realpath("../databases/logins.db")) as db:

        cursor = db.cursor()

        cursor.execute("SELECT email FROM details WHERE receive = ?", (1, ))

        result = cursor.fetchall()

    msg = EmailMessage()
    msg["From"] = SENDER
    if name is None:
        msg["Subject"] = f"{str(datetime.now())[:-7]} - NO FACE RECOGNISED AT DOOR"
        msg.set_content(
            "The camera did not recognise a face, but here is the photo it took:")
    elif name == "Unknown":
        msg["Subject"] = f"{str(datetime.now())[:-7]} - UNKNOWN FACE RECOGNISED AT DOOR"
        msg.set_content("Unknown face at the door:")
    else:
        msg["Subject"] = f"{str(datetime.now())[:-7]} - {name} is at the door!"

        with sqlite3.connect(os.path.realpath("../databases/authorised_persons.db")) as db:

            cursor = db.cursor()

            cursor.execute(
                "SELECT * FROM people WHERE first_name = ?", (name, ))

            details = cursor.fetchall()

        msg.set_content(
            f"First Name: {details[0][1]}\nLast Name: {details[0][2]}\nEmail Address: {details[0][3]}\nHere is the photo we took:")

    with open(os.path.realpath("../temp_images/photo.jpg"), "rb") as file:
        data = file.read()
        file_type = imghdr.what(file.name)
        filename = file.name

    msg.add_attachment(data, maintype="image",
                       subtype=file_type, filename=filename)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        # with smtplib.SMTP("localhost", 1025) as smtp:
        smtp.login(SENDER, PASS)
        recipients = [email[0] for email in result]
        msg["To"] = ",".join(recipients)
        smtp.send_message(msg)


if __name__ == "__main__":
    send()
