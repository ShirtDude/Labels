import openai_secret_manager
from openai_secret_manager import get_secret
import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, message):
    # Get secrets
    secrets = get_secret("google")

    # Set up SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(secrets['email'], secrets['password'])

    # Create message
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = secrets['email']
    msg['To'] = to_email

    # Send message
    smtp_server.sendmail(secrets['email'], [to_email], msg.as_string())
    smtp_server.quit()
