import smtplib
import imghdr
from email.message import EmailMessage
from datetime import datetime
import sqlite3


def send(name):

    SENDER = "onsokunosonikkuda@gmail.com"
    PASS = "UpToTheTimes"

    with sqlite3.connect("logins.db") as db:

        cursor = db.cursor()

        cursor.execute("SELECT email WHERE receive = ?", (1, ))

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
        msg.set_content(f"Here is the photo of {name} we just took:")

    with open("photo.jpg", "rb") as file:
        data = file.read()
        file_type = imghdr.what(file.name)
        filename = file.name

    msg.add_attachment(data, maintype="image",
                       subtype=file_type, filename=filename)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        # with smtplib.SMTP("localhost", 1025) as smtp:
        smtp.login(SENDER, PASS)
        for email in result:
            msg["To"] = email[0]
            smtp.send_message(msg)
