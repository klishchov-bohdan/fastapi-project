import smtplib
from email.message import EmailMessage
from celery import Celery

from app.config import SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT, REDIS_SERVER, REDIS_PORT


celery = Celery('tasks', broker=f'redis://{REDIS_SERVER}:{REDIS_PORT}')


def get_email_template(receiver: str, code: int):
    email = EmailMessage()
    email['Subject'] = 'Verification code'
    email['From'] = SMTP_USER
    email['To'] = receiver
    email.set_content(f'Привет. Твой код подтверждения - {code}'.encode('utf8'), maintype='html', subtype='html')
    return email


@celery.task
def send_email_verification_code(receiver: str, code: int):
    email = get_email_template(receiver, code)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
