import os
from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place

from forms import SignupForm, LoginForm, AddressForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                  'postgresql://localhost/learningflask')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = os.environ.get('SECRET_KEY')


## ROUTES ##

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))

    form = SignupForm()

    if request.method == 'POST' and form.validate():
        newuser = User(form.first_name.data,
                       form.last_name.data,
                       form.email.data,
                       form.password.data)
        db.session.add(newuser)
        db.session.commit()

        session['email'] = newuser.email
        return redirect(url_for('home'))
    return render_template('signup.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))

    form = LoginForm()

    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            session['email'] = form.email.data
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login')) # triggers GET request
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'email' not in session:
        return redirect(url_for('login'))

    form = AddressForm()

    places = []
    my_coordinates = (42.650435, -73.758516)

    if request.method == 'POST' and form.validate():
        # get the address
        address = form.address.data

        # query for places around it
        p = Place()
        my_coordinates = p.address_to_latlng(address)
        places = p.query(address)

        # return the results
        return render_template('home.html', form=form,
                                            my_coordinates=my_coordinates,
                                            places=places)
    return render_template('home.html', form=form,
                                        my_coordinates=my_coordinates,
                                        places=places)


## INIT ##

if __name__ == '__main__':
    app.run(debug=True)
