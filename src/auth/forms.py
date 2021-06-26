from wtforms import form, fields, validators
from werkzeug.security import check_password_hash
from src import db
from src.auth.models import User


class LoginForm(form.Form):
    email = fields.StringField(
        validators=[validators.required(), validators.length(max=120)])
    password = fields.PasswordField(
        validators=[validators.required(), validators.length(max=255)])

    def validate_login(self):
        user = self.get_user_by_email()

        if user is None:
            self.errors[0] = 'Invalid user'
            return False

        if not user.is_active():
            self.errors[0] = 'Invalid user'
            return False

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
            self.errors[0] = 'Invalid user'
            return False

        return user

    def get_user_by_email(self):
        return db.session.query(User).filter(
            User.email == self.email.data).first()

