from flask_wtf import FlaskForm

from wtforms import (
                    StringField,
                    SubmitField,
                    PasswordField
                    )
from wtforms.validators import (
                    InputRequired,
                    Length,
                    EqualTo
                    )


class PasswordChangeForm(FlaskForm):
    """Password change form"""
    email = StringField('email_label',
                        validators=[InputRequired(message='Please provide email')]
                        )
    password = PasswordField('password_label',
                           validators=[Length(min=8)]
                           )
    repeat_password = PasswordField('password_confirm_label',
                                  validators=[EqualTo('password', message='Passwords must match')]
                                  )

    submit_button = SubmitField('Change')