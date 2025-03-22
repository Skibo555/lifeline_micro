import os, smtplib, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders 
from dotenv import load_dotenv
from smtplib import SMTPException, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError

load_dotenv()

# Email details
# MY_EMAIL = os.environ.get("MY_MAIL")
MY_EMAIL = "yonwatodejulius@gmail.com"
# MY_PASSWORD = os.environ.get("MY_EMAIL_PASSWORD")
MY_PASSWORD = "obuilcpnnyrhmszt"

# MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_SERVER = "smtp.gmail.com"
print(MY_EMAIL, MY_PASSWORD, MAIL_SERVER)


async def send_email(data: dict, body_type='plain'):
    message = MIMEMultipart()
    message["Subject"] = "Blood Request Notification"
    message["From"] = MY_EMAIL
    message["To"] = data["email"]
    body = f"Hello {data['username']},\n\nA blood request has been created near your location. Please check the app for more details."

    part = MIMEText(body, body_type)
    message.attach(part)

    try:
        with smtplib.SMTP_SSL(MAIL_SERVER, 465) as server:
            server.login(MY_EMAIL, MY_PASSWORD)
            server.sendmail(MY_EMAIL, data["email"], message.as_string())
            print("Email sent successfully")
            return "Mail Sent"
        
    except SMTPRecipientsRefused:
        print("❌ Error: Invalid recipient email address")
        return "Invalid recipient email address"
    
    except SMTPSenderRefused:
        print("❌ Error: Sender address refused, check your credentials or SMTP settings")
        return "Sender address refused"

    except SMTPDataError:
        print("❌ Error: Issue with email content, it might be flagged as spam")
        return "Email content issue"

    except SMTPException as ex:
        print(f"❌ General SMTP Error: {ex}")
        return f"SMTP Error: {ex}"

    except Exception as ex:
        print(f"❌ Unexpected Error, you may need to check your internet connection: {ex}")
        return f"Unexpected Error: {ex}"
    
