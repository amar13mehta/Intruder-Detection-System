import smtplib, ssl
import imghdr
from email.message import EmailMessage


def send_mail(image_path):
    pwd = "dsdfqktintxcmlj"
    host = "smtp.gmail.com"
    port = 465
    username = "amar13iam@gmail.com"
    receiver = "amar13iam@gmail.com"

    message = EmailMessage()
    message["subject"] = "Object Detected"
    message.set_content("Please find the attached image of the object detected")
    with open(image_path, "rb") as file:
        image = file.read()
    message.add_attachment(image, maintype="image", subtype=imghdr.what(None, image))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, pwd)
        server.sendmail(username, receiver, message.as_string())
    print("Email Sent")