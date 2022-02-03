from flask import current_app
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from time import time
from hashlib import sha256


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_signed_params(self, expires_in=600):
        # generate a hash from url:
        payload = self.email +"?expires=" + str(int(time()) + expires_in)
        hashed = sha256(str(payload).encode())

        return payload + "&token=" + hashed.hexdigest()

    @staticmethod
    def verify_reset_password_token(data_to_check, token):
        try:
            hash_to_check = sha256(str(data_to_check).encode())
            if hash_to_check.hexdigest() != token:
                return
        except:
            return
        pieces = data_to_check.split('?')
        email = pieces[0]
        return User.query.filter_by(email=email).first()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
