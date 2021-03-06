from wtforms.validators import (
                        ValidationError
)
from models.users import Users
from passlib.hash import pbkdf2_sha256


def invalid_credentials(form, field) -> None:
    """ Username validation  """

    username = form.username.data
    password = field.data

    user_data = Users.query.filter_by(username=username).first()
    if user_data is None:
        raise ValidationError("Incorrect user data")
    elif not pbkdf2_sha256.verify(password, user_data.password):
        raise ValidationError("Incorrect user data")
