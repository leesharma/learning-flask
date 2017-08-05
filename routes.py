import os
from flask import Flask, render_template, request
from models import db, User

from forms import SignupForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                  'postgresql://localhost/learningflask')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = os.environ.get('SECRET_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST' and form.validate():
        newuser = User(form.first_name.data,
                       form.last_name.data,
                       form.email.data,
                       form.password.data)
        db.session.add(newuser)
        db.session.commit()
        return 'Success!'
    return render_template('signup.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)
