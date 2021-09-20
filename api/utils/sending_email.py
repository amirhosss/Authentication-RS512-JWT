import smtplib
import os
from email.message import EmailMessage
from dotenv import find_dotenv, load_dotenv


def send_email(email: str, subject: str, content: str):
    path = find_dotenv()
    load_dotenv(path)

    PASSWORD = os.environ.get('EMAIL_PASSWORD')
    EMAIL = os.environ.get('EMAIL')

    msg = EmailMessage()
    msg.set_content(content)

    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(EMAIL, PASSWORD)
    server.sendmail(
        EMAIL,
        email,
        msg.as_string()
    )

    server.quit()
