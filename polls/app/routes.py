import os
from passlib.hash import pbkdf2_sha256
from datetime import datetime

from flask import (render_template,
                   flash,
                   redirect,
                   request,
                   url_for
                   )
from werkzeug.wrappers import Response
from flask_login import (LoginManager,
                         login_user,
                         current_user,
                         login_required,
                         logout_user
                        )
from flask_mail import Mail
from flask_uploads import send_from_directory
from werkzeug.utils import secure_filename

from app import app
from models.users import Users
from models.question import Question
from models.options import Options
from models.vote import Vote
from forms.registration import RegistrationForm
from forms.login import LoginForm
from forms.password_change import PasswordChangeForm
from forms.question import QuestionForm
from forms.contact import ContactForm
from app.db import db
from app.helpers import allowed_file
from app.app import app

mail = Mail(app)
mail.init_app(app)
login_manager = LoginManager(app)

from app.user_token import SendingMails

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.user_loader
def load_user(user):
    return Users.get(user)


@app.route('/', methods=['POST', 'GET'])
def main() -> Response:
    polls = Question.query.all()
    return render_template('main.html', polls=polls)


@app.route('/confirm-email/<token>')
@login_required
def confirm_email(token):
    try:
        email = SendingMails(app, mail).confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')

    user = Users.query.filter_by(mail=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main'))


@app.route('/register/', methods=['GET', 'POST'])
def register() -> Response:

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']
        mail = form.data['mail']
        hashed_pswd = pbkdf2_sha256.hash(password)
        user = Users(
            username=username,
            mail = mail,
            password=hashed_pswd,
            confirmed = False)
        db.session.add(user)
        db.session.commit()

        token = SendingMails(app,mail).generate_confirmation_token(user.mail)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('users/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        SendingMails(app, mail).send_email(user.mail, subject, html)
        flash('A confirmation email has been sent via email. :)', 'success')

        return redirect(url_for('unconfirmed'))

    return render_template('users/register.html', form=form)


@app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('main.home')
    flash('Please confirm your account!', 'warning')
    return render_template('user/unconfirmed.html')


@app.route('/reset-password/', methods = ["GET", "POST"])
def reset_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        confirm_password = form.data['repeat_password']
        if password != confirm_password:
            return redirect(request.url)

        user = Users.query.filter_by(mail=email).first()
        hashed_pswd = pbkdf2_sha256.hash(password)
        if user:
            user.password = hashed_pswd
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('users/change_password.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login() -> Response:
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_object = Users.query.filter_by(
            username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('/'))
    return render_template('users/login.html', form=login_form)


@app.route('/polls/<filename>')
def uploaded(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/results/<id>/<selected_value>/', methods = ['POST', 'GET'])
def click(selected_value, id):
    if selected_value:
        votes = Vote(vote=1,
                     option_id=selected_value)
        db.session.add(votes)
        db.session.commit()
        flash(f"You voted  successfully!")

        results = db.session.query(Options.choice, Vote.vote,)\
            .filter_by(question_id=id).\
            outerjoin(Vote, Options.id == Vote.option_id).all()

        return render_template('polls/results.html', results = results)
    return redirect(url_for('detail_view'))


@app.route('/polls/<int:id>', methods=['POST', 'GET'])
def detail_view(id: int,vote=None) -> Response:
    poll = Question.query.filter_by(id = id).first()
    if request.method == 'POST':
        vote = request.form.get('result')
        return redirect(url_for('click', selected_value=vote, id = id))
    if not vote:
        flash('Please vote!')
        return render_template('polls/poll.html', poll_data = poll)

    return render_template('polls/poll.html', poll_data = poll)


@app.route('/add-new-poll/', methods = ['POST', 'GET'])
def new_poll() -> Response:
    form = QuestionForm()
    if form.validate_on_submit() and 'cover' in request.files:
        if 'cover' not in request.files:
            flash('No file')
            return redirect(request.url)

        cover = request.files['cover']
        if cover and allowed_file(cover.filename):
            filename = secure_filename(cover.filename)
            cover.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        question = form.data['question']
        option1 = form.data['option1']
        option2 = form.data['option2']
        option3 = form.data['option3']
        option4 = form.data['option4']

        question = Question(
                            question = question,
                            cover = secure_filename(cover.filename),
                            options = [Options(choice = option1),
                                       Options(choice = option2),
                                       Options(choice = option3),
                                       Options(choice =option4)]
        )
        db.session.add(question)
        db.session.commit()

        flash('Your poll is added now')
        return redirect(url_for('main'))
    return render_template('polls/newpoll.html', form = form)


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
    return render_template('polls/update_poll.html', poll_data = poll, form = form)


@app.route('/delete/<int:id>')
def delete_poll(id: int) -> Response:
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


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.data['name']
        mail = form.data['mail']
        text = form.data['message']

        html = render_template('message.html', content=text, name=name)
        subject = f'Notification from polls'
        SendingMails(app, mail).send_email(app.config['MAIL_USERNAME'], subject, html)
        flash('Your message was sent to administration. :)', 'success')

    return render_template('contact.html', form = form)

