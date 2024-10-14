import os
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key'

server = os.getenv('DATABASE_SERVER')
database = os.getenv('DATABASE_NAME')
username = os.getenv('DATABASE_USER')
password = os.getenv('DATABASE_PASSWORD')
driver = '{ODBC Driver 17 for SQL Server}'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/success/<name>')
def success(name):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    comments = Comment.query.all()
    return render_template('forum.html', name=name, comments=comments)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            return redirect(url_for('success', name=username))
        else:
            return "Invalid credentials, please try again."
    else:
        return render_template('login.html')

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    content = request.form['content']
    user_id = session['user_id']

    new_comment = Comment(user_id=user_id, content=content)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('success', name=session['user_id']))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
