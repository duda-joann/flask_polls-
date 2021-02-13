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
                                )
from polls.models.users import Users


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

    def validate(self):
        initial_validation = super(RegistrationForm, self).validate()
        if not initial_validation:
            return False
        user = Users.query.filter_by(mail=self.mail.data).first()
        if user:
            self.mail.errors.append("Email already registered")
            return False
        return True


