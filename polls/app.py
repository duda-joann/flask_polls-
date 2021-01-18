from passlib.hash import pbkdf2_sha256

from flask import (render_template,
                   flash,
                   redirect,
                   url_for)
from werkzeug.wrappers import Response
from flask_login import (LoginManager,
                         login_user,
                         login_required,
                         logout_user
)
from polls.main import create_app
from polls.models.admin import Admin
from polls.models.question import Question
from polls.models.options import Options
from polls.forms.registration import (
                    RegistrationForm,
                    )
from polls.forms.login import LoginForm
from polls.forms.question import QuestionForm
from polls.db import db


app = create_app()
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user):
    return Admin.get(user)


@app.route('/register/', methods=['GET', 'POST'])
def register() -> Response:

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']
        mail = form.data['mail']
        hashed_pswd = pbkdf2_sha256.hash(password)
        user = Admin(
            username=username,
            mail = mail,
            password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registered seccusfully! Please login :)', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login() -> Response:

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_object = Admin.query.filter_by(
            username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('/'))
    return render_template('login.html', form=login_form)


@app.route('/', methods=['POST', 'GET'])
def main() -> Response:
    polls = Question.query.all()
    return render_template('main.html', polls=polls)


@app.route('/polls/<int:id>')
def detail_view(id: int) -> Response:
    poll = Question.query.filter_by(id = id).first()
    return render_template('poll.html', poll_data = poll)


@app.route('/add-new-poll/', methods = ['POST', 'GET'])
def new_poll() -> Response:
    form = QuestionForm()
    if form.validate_on_submit():
        question = form.data['question']
        option1 = form.data['option1']
        option2 = form.data['option2']
        option3 = form.data['option3']
        option4 = form.data['option4']
        question = Question(
                            question = question,
                            options = [Options(choice = option1),
                                       Options(choice = option2),
                                       Options(choice = option3),
                                       Options(choice =option4)]
        )
        db.session.add(question)
        db.session.commit()

        flash('Your poll is added now')
        return redirect(url_for('main'))

    return render_template('newpoll.html', form = form)


@app.route('/logout/', methods = ['GET'])
@login_required
def logout() -> Response:
    logout_user()
    flash('You are logout successfully')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
