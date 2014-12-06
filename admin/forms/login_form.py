# coding: utf-8

from wtforms import fields, form, validators

from models.users import Users
from admin import session


class LoginForm(form.Form):
    email = fields.StringField("Email", [validators.email(), validators.required()])
    password = fields.PasswordField("Password", [validators.required()])

    def validate_email(self, field):
        self.get_user(field.data)

        if self.user is None:
            raise validators.ValidationError(u"Invalid user")

        if not self.user.is_manager:
            raise validators.ValidationError(u"Access denied")

    def validate_password(self, field):
        if not len(self.errors.keys()):
            if self.user and self.user.password != field.data:
                raise validators.ValidationError(u"Invalid password")

    def get_user(self, email='EMPTYEMAIL'):
        if email == 'EMPTYEMAIL':
            self.user = session.query(Users).filter_by(email=self.email).first()
        else:
            self.user = session.query(Users).filter_by(email=email).first()
