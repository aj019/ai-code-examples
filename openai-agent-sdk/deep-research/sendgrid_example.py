from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

sg = SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))


def send_email(subject, body):
    message = Mail(
        from_email=os.getenv('SENDGRID_FROM_EMAIL'),
        to_emails=os.getenv('SENDGRID_TO_EMAIL'),
        subject=subject,
        html_content=body
    )
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

send_email("Test Email", "This is a test email")
