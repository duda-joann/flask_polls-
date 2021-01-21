from flask_wtf import FlaskForm
from wtforms import (
                    StringField,
                    SubmitField,
                    FileField)
from wtforms.validators import InputRequired


class QuestionForm(FlaskForm):
    """ New question form"""
    question = StringField(
                          'question',
                          validators=[InputRequired(message='Missing question')
                                      ])
    cover = FileField('cover', validators=[InputRequired(message = 'Missing photo')])
    option1 = StringField(
                        'option1',
                         validators=[InputRequired(message='Missing option')
                                     ])
    option2 = StringField(
                          'option2',
                          validators=[InputRequired(message='Missing option')
                                      ])
    option3 = StringField(
                        'option3',
                         validators=[InputRequired(message='Missing option')])
    option4 = StringField(
                        'option4',
                        validators=[InputRequired(message='Missing option')
                                    ])

    submit_button = SubmitField('Add')
