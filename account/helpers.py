from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_confirmation_email(user):
    context = {
        "small_text": """
        Thank you for creating an account.
        Please verify your email
        """,
        "email": user.email,
        "activation_code": user.activation_code,
    }
    msg_html = render_to_string("email.html", context)
    plain_message = strip_tags(msg_html)
    subject = "Account activation"
    to_emails = user.email
    mail.send_mail(
        subject,
        plain_message,
        "nurkamilaturathankyzy@gmail.com",
        [to_emails],
        html_message=msg_html
    )

def send_resetpassword_link(email, code):
    context = {
        "small_text": "Please, follow this link to reset your password",
        "url": f"http://127.0.0.1:8000/account/reset_password/{code}",
        "code": code
    }
    msg_html = render_to_string("reset_pass.html", context)
    plain_message = strip_tags(msg_html)
    subject = "Reset password"
    to_emails = email
    mail.send_mail(
        subject,
        plain_message,
        "nurkamilaturathankyzy@gmail.com",
        [to_emails],
        html_message=msg_html
    )