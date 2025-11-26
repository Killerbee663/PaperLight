from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os


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

            message = Mail(
                from_email=self.from_email,
                to_emails=self.to_emails,
                subject=self.subject,
                html_content=f"<pre>{msg_body}</pre>",
            )

            sg = SendGridAPIClient(self.api_key)
            sg.send(message)
        except Exception as e:
            self.handleError(record)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    api_key = os.environ.get("SENDGRID_API_KEY")
    if not api_key:
        current_app.logger.error("SENDGRID_API_KEY not configured - cannot send email")
        return
    
    try:
        message = Mail(
            from_email=sender,
            to_emails=recipients,
            subject=subject,
            html_content=html_body
        )
        message.add_content(text_body, 'text/plain')

        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        current_app.logger.info(f"Email sent successfully: {response.status_code}")
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {e}")
