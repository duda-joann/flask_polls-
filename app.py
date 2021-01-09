from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   redirect,
                   url_for)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blebleble'

poll_data = {
   'question': 'What do you prefer?',
   'fields': ['Saxon',
              'Budgie',
              'Nazareth',
              'Uriah Heep',
              'Deep Purple'
              ]}

result = {'Saxon': 0,
          'Budgie': 0,
          'Nazareth': 0,
          'Uriah Heep': 0,
          'Deep Purple': 0}


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        vote = request.form
        if not vote:
            flash('Please vote!')
            return redirect(url_for('home'))
        if len(vote) != 1:
            flash('You can only choose one option. Only one!')
        if vote:
            result[vote] += 1
        flash('Thanks for votes!')
    return render_template('main.html', poll_data = poll_data)


if __name__ == '__main__':
    app.run(debug=True)