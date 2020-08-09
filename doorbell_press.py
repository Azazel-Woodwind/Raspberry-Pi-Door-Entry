import recognise_face
import email_sender

def main():
    name = recognise_face.recog()
    email_sender.send(name)

if __name__ == "__main__":
    main()