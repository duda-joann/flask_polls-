from flask_wtf import FlaskForm
from wtforms import (
                    StringField,
                    PasswordField,
                    SubmitField
                    )
from wtforms.validators import (
                                InputRequired,
                                Length,
                                EqualTo,
                                ValidationError
                                )
from polls.models.admin import Admin


class RegistrationForm(FlaskForm):
    """ Registration Form """

    username = StringField(
        'username_label',
        validators=[InputRequired(
                    message="Username required"),
                    Length(min=6, max=30,
                    message="Username must be between 6 and 30 characters"
                           )]
    )
    mail = StringField(
        'mail_label',
        validators=[InputRequired(message='mail required')]
    )
    password = PasswordField(
            'password_label',
            validators=[InputRequired(message="Password required"),
            Length(min=6, max=30, message="Password must be between 6 and 30 characters"
                   )])
    confirm_password = PasswordField(
                                'confirm_passd_label',
                                validators=[InputRequired(message="Password required"),
                                EqualTo('password', message="Passwords have to match")]
    )
    submit_button = SubmitField('Create')

    def validate_username(self, username) -> None:
        user_object = Admin.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists. Please, chose different username.")