from passlib.hash import pbkdf2_sha256

from flask import (render_template,
                   flash,
                   redirect,
                   request,
                   url_for
                   )
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
from polls.models.vote import Vote
from polls.forms.registration import (
                    RegistrationForm,
                    )
from polls.forms.login import LoginForm
from polls.forms.question import QuestionForm
from polls.db import db


app = create_app()
login_manager = LoginManager(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


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


@app.route('/polls/<int:id>', methods=['POST', 'GET'])
def detail_view(id: int) -> Response:
    poll = Question.query.filter_by(id = id).first()
    if request.method == 'POST':
        vote = request.form.get('result')
        if not vote:
            flash('Please vote!')
            return redirect(url_for(f'/polls/{id}'))
        if vote:
            vote = Vote(vote=vote,
                        question_id = id)
            db.session.add(vote)
            db.session.commit()
            flash(f"You voted  successfully!")

    result = Options.query.filter_by(question_id=id).all()
    return render_template('poll.html', poll_data = poll, stats = result)


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


@app.route('/update-poll/<int:id>')
def update_poll(id):
    poll = Question.query.filter_by(id = id).first()
    form = QuestionForm(
                        question=poll.question,
                        option1=poll.options[0],
                        option2=poll.options[1],
                        option3=poll.options[2],
                        option4=poll.options[3],
                        )
    if form.validate_on_submit():
        question = form.data['question']
        option1 = form.data['option1']
        option2 = form.data['option2']
        option3 = form.data['option3']
        option4 = form.data['option4']
        poll = Question(
                question=question,
                options=[Options(choice=option1),
                         Options(choice=option2),
                         Options(choice=option3),
                         Options(choice=option4)]
            )
        db.session.add(poll)
        db.session.commit()

        flash('Your poll is update now')
        return redirect(url_for(f'polls/{id}'))
    return render_template('update_poll.html', poll_data = poll, form = form)


@app.route('/delete/<int:id>')
def delete_poll(id):
    poll = Question.query.get_or_404(id)
    db.session.delete(poll)
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/logout/', methods = ['GET'])
@login_required
def logout() -> Response:
    logout_user()
    flash('You are logout successfully')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)