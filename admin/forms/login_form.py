# coding: utf-8

from wtforms import fields, form, validators

from models.users import Users
from admin import session


class LoginForm(form.Form):
    email = fields.StringField("Email", [validators.email(), validators.required()])
    password = fields.PasswordField("Password", [validators.required()])

    def validate_email(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError("Invalid user")

        if not user.is_manager:
            raise validators.ValidationError("Access denied")

    def validate_password(self, field):
        user = self.get_user()

        if user.password != self.password.data:
            raise validators.ValidationError("Invalid password")

    def get_user(self):
        return session.query(Users).filter_by(email=self.email.data).first()
