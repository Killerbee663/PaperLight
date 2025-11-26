from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class SendGridHandler(logging.Handler):
    def __init__(self, api_key, from_email, to_emails, subject):
        logging.Handler.__init__(self)
        self.api_key = api_key
        self.from_email = from_email
        self.to_emails = to_emails if isinstance(to_emails, list) else [to_emails]
        self.subject = subject

    def emit(self, record):
        try:
            msg_body = self.format(record)

            message = mail(
                from_email=self.from_email,
                to_emails=self.to_emails,
                subject=self.subject,
                html_content=f'<pre>{msg_body}</pre>'
            )

            sg = SendGridAPIClient(self.api_key)
            sg.send(message)
        except Exception as e:
            self.handleError(record)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()