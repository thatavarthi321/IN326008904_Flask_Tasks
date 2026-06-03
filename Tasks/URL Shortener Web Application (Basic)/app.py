from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string
import validators

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database

db = SQLAlchemy(app)

# Database Model
class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)

# Create random short code

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Home Route
@app.route('/', methods=['GET', 'POST'])
def index():

    short_url = None
    error = None

    if request.method == 'POST':

        original_url = request.form.get('url')

        # URL Validation
        if not validators.url(original_url):
            error = 'Please enter a valid URL!'
            return render_template('index.html', error=error)

        # Generate short code
        short_code = generate_short_code()

        # Save to database
        new_url = URLMap(
            original_url=original_url,
            short_code=short_code
        )

        db.session.add(new_url)
        db.session.commit()

        short_url = request.host_url + short_code

    return render_template('index.html', short_url=short_url, error=error)

# Redirect Route
@app.route('/<short_code>')
def redirect_to_url(short_code):

    url = URLMap.query.filter_by(short_code=short_code).first()

    if url:
        return redirect(url.original_url)

    return 'URL Not Found!'

# History Page
@app.route('/history')
def history():

    urls = URLMap.query.all()

    return render_template('history.html', urls=urls)

# Run App
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
