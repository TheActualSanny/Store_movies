from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'register'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Movies(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(40), nullable=False)
    director = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    
    def __str__(self):
        return f'Title of the movie: {self.movie_title}; The director: {self.director}; The release date: {self.release_date}; The rating: {self.rating}'

class Accounts(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __str__(self):
        return f'Username: {self.username}; Creation date: {self.creation_date}'

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Accounts.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = username
            return redirect(url_for('user'))
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/user')
def user():
    if 'user' in session:
        subjects = ['Python', 'Calculus', 'DB']
        return render_template('user.html', subjects=subjects)
    return redirect(url_for('login'))

@app.route('/<name>/<age>')
def userage(name, age):
    return f'Hello {name}, your age is {age}'

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        releasedate = request.form['releasedate']
        rating = request.form['rating']
        movie = Movies(movie_title=title, director=director, release_date=releasedate, rating=rating)
        db.session.add(movie)
        db.session.commit()
        flash('Movie successfully added.', 'success')
        return redirect(url_for('movies'))
    return render_template('movies.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        return sign_up()
    return render_template('register.html')

def sign_up():
    username = request.form['username']
    password = request.form['password']
    
    
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    
    if not re.match(password_regex, password):
        flash('Password must be at least 8 characters long, contain at least one special character, one number, and one uppercase letter.', 'error')
        return redirect(url_for('register'))
    
    if Accounts.query.filter_by(username=username).first():
        flash('Username already exists', 'error')
        return redirect(url_for('register'))
    
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = Accounts(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    flash('Registration successful! Please log in.', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
