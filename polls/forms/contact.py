from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import (
                    StringField,
                    SubmitField,
                    )


class ContactForm(FlaskForm):

    """Contact form for user"""
    name = StringField('name')
    mail = StringField('mail',
                    validators=[
                        InputRequired(message='Please provide mail'),
                        ])
    message = StringField('text',
                     validators=[
                         InputRequired(message='Please fill a message'),
                         ])
    send = SubmitField('Send')
