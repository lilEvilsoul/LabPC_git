#!/usr/bin/env python3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import json

data = {}
with open("pass.json") as f:
    data = json.load(f)
# create and setup the parameters of the message
email_msg = MIMEMultipart()
email_msg["From"] = data["user"]
receipents = [input("Ingrese el correo deseado: ")]
email_msg["To"] = ", ".join(receipents)
email_msg["Subject"] = input("Ingrese el asunto: ")

# add in the message body
message = input("Ingrese el mensaje: ")
email_msg.attach(MIMEText(message, "plain"))

# create server
server = smtplib.SMTP("smtp.office365.com:587")
server.starttls()
# Login Credentials for sending the mail
server.login(data["user"], data["pass"])


# send the message via the server.
server.sendmail(email_msg["From"], receipents, email_msg.as_string())
server.quit()
print("successfully sent email to %s:" % (email_msg["To"]))
