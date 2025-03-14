import os, smtplib, json
from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv()

# Email details
MY_EMAIL = os.environ.get("MY_MAIL")
MY_PASSWORD = os.environ.get("MY_EMAIL_PASSWORD")

MAIL_SERVER = os.environ.get("MAIL_SERVER")



def send_email(data: dict):
    message = json.loads(data)
    mp3_fid = message["mp3_fid"]
    sender_address = os.environ.get("GMAIL_ADDRESS")
    sender_password = os.environ.get("GMAIL_PASSWORD")
    receiver_address = message["username"]

    msg = EmailMessage()
    msg.set_content(f"mp3 file_id: {mp3_fid} is now ready!")
    msg["Subject"] = "MP3 Download"
    msg["From"] = sender_address
    msg["To"] = receiver_address

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sender_address, sender_password)
    session.send_message(msg, sender_address, receiver_address)
    session.quit()
    print("Mail Sent")