from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

import random
import string
import validators

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ---------------- USER MODEL ----------------

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True)

    password = db.Column(db.String(20))

# ---------------- URL MODEL ----------------

class URLMap(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    original_url = db.Column(db.String(500))

    short_code = db.Column(db.String(10), unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# ---------------- LOGIN LOADER ----------------

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

# ---------------- SHORT CODE ----------------

def generate_short_code():

    characters = string.ascii_letters + string.digits

    return ''.join(random.choice(characters) for _ in range(6))

# ---------------- SIGNUP ----------------

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    error = None

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        # Username length validation
        if len(username) < 5 or len(username) > 9:

            error = 'Username must be between 5 to 9 characters long'

            return render_template('signup.html', error=error)

        # Existing username check
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:

            error = 'This username already exists'

            return render_template('signup.html', error=error)

        # Save user
        new_user = User(username=username, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('signup.html')

# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:

            login_user(user)

            return redirect('/')

        else:

            error = 'Invalid Username or Password'

    return render_template('login.html', error=error)

# ---------------- LOGOUT ----------------

@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect('/login')

# ---------------- HOME ----------------

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():

    short_url = None
    error = None

    if request.method == 'POST':

        original_url = request.form.get('url')

        # URL validation
        if not validators.url(original_url):

            error = 'Please enter a valid URL'

            return render_template(
                'home.html',
                error=error
            )

        short_code = generate_short_code()

        new_url = URLMap(
            original_url=original_url,
            short_code=short_code,
            user_id=current_user.id
        )

        db.session.add(new_url)
        db.session.commit()

        short_url = request.host_url + short_code

    return render_template(
        'home.html',
        short_url=short_url,
        error=error
    )

# ---------------- REDIRECT ----------------

@app.route('/<short_code>')
def redirect_url(short_code):

    url = URLMap.query.filter_by(short_code=short_code).first()

    if url:

        return redirect(url.original_url)

    return 'URL Not Found'

# ---------------- HISTORY ----------------

@app.route('/history')
@login_required
def history():

    urls = URLMap.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template('history.html', urls=urls)

# ---------------- RUN ----------------

if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(debug=True)