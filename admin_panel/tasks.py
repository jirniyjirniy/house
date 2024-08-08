from celery import shared_task, current_task
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import get_template, render_to_string
from weasyprint import HTML

from House24.celery import app


@app.task(bind=True)
def send_invitation(self, to='somebody@gmail.com', ):
    html_template = 'admin_panel/invitation_email.html'
    html_message = render_to_string(html_template)
    message = EmailMessage('Приглашение в House24', html_message, 'dhushchyn@gmail.com', [to])
    message.content_subtype = 'html'  # this is required because there is no plain text email message
    message.send()


@app.task(bind=True)
def send_receipt(self, html_to_pdf, base_url, to='somebody@gmail.com'):
    pdf_file = HTML(string=html_to_pdf, base_url=base_url).write_pdf()

    html_template = 'admin_panel/receipt_email.html'
    html_message = render_to_string(html_template)
    message = EmailMessage('Электронная квитанция House24', html_message, 'dhushchyn@gmail.com', [to])

    message.attach('квитанция.pdf', pdf_file, 'application/pdf')

    message.content_subtype = 'html'  # this is required because there is no plain text email message
    message.send()


@app.task(bind=True)
def notification_password_changed(self, to='somebody@gmail.com'):
    html_template = 'admin_panel/email_notification_password_changed.html'
    html_message = render_to_string(html_template)
    message = EmailMessage('Смена пароля в House24', html_message, 'dhushchyn@gmail.com', [to])
    message.content_subtype = 'html'  # this is required because there is no plain text email message
    message.send()

