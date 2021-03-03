from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def allowed_file(filename: str):
    """ checking if loaded by resource file is with an extension png, jpg, jpeg  or gif """
    return '.' in filename and \
           filename.split('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif']


def check_confirmed(func):
    @wraps(func)
    def function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('user.unconfirmed'))
        return function(*args, **kwargs)

    return func

