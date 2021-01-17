from flask import (render_template,
                   request,
                   flash,
                   redirect,
                   url_for)
from werkzeug.wrappers import Response
from flask_login import (LoginManager,
                         login_user,
                         login_required,
                         logout_user
)
from passlib.hash import pbkdf2_sha256
from polls.main import create_app
from polls.models import Admin

from polls.forms.registration import (
                    RegistrationForm,
                    )
from polls.forms.login import LoginForm
from polls.db import db


app = create_app()
login_manager = LoginManager(app)

poll_data = {
    'question': 'What do you prefer?',
    'fields': ['Saxon',
               'Budgie',
               'Nazareth',
               'Uriah Heep',
               'Deep Purple'
               ]}

results = {'Saxon': 0,
           'Budgie': 0,
           'Nazareth': 0,
           'Uriah Heep': 0,
           'Deep Purple': 0}


@login_manager.user_loader
def load_user(user):
    return Admin.get(user)


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/login', methods=['GET', 'POST'])
def login() -> Response:

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_object = Admin.query.filter_by(
            username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('/'))

    return render_template('login.html', form=login_form)


@app.route('/', methods=['POST', 'GET'])
def home() -> Response:
    if request.method == 'POST':
        vote = request.form.get('result')
        if not vote:
            flash('Please vote!')
            return redirect(url_for('home'))
        if vote:
            results[vote] += 1
        flash('Thanks for votes!')
    return render_template('main.html', poll_data=poll_data, data=results)


@app.route('/logout', methods = ['GET'])
@login_required
def logout() -> Response:
    logout_user()
    flash('You are logout successfully')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
