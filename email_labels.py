import smtplib
from email.mime.text import MIMEText
from typing import List
from openai_secret_manager import get_secret


def send_email(to_email: str, subject: str, message: str) -> None:
    """
    Send an email.

    Args:
        to_email (str): The email address of the recipient.
        subject (str): The subject line of the email.
        message (str): The message to be sent in the email.

    Returns:
        None
    """
    secrets = get_secret("google")

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(secrets['email'], secrets['password'])

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = secrets['email']
    msg['To'] = to_email

    smtp_server.sendmail(secrets['email'], [to_email], msg.as_string())
    smtp_server.quit()
