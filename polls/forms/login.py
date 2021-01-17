from flask_wtf import FlaskForm
from wtforms import (
                    StringField,
                    PasswordField,
                    SubmitField)
from wtforms.validators import InputRequired
from .validation import invalid_credentials


class LoginForm(FlaskForm):
    """ Login Form """

    username = StringField(
        'username_label',
        validators=[InputRequired(message="Username required")
                    ]
    )
    password = PasswordField(
        'password_label',
        validators=[InputRequired(message="Password required"),
                    invalid_credentials
                    ]
    )
    submit_button = SubmitField('Login')