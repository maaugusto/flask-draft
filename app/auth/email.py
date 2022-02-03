from flask import render_template, url_for
from app.email import send_email


def send_password_reset_email(user):
    temp = user.get_reset_password_signed_params()
    pieces = temp.split('?')
    url_end = "?" + pieces[1]
    send_email('Reset password',
               sender='example@email.com',
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, url_end=url_end),
               html_body=render_template('email/reset_password.html', user=user, url_end=url_end))
