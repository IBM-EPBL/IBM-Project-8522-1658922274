from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

db.init_app(app)

app.secret_key='asdsdfsdfs13sdf_df%&'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

with app.app_context():
    db.create_all()

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        fullname = firstname + " " + lastname
        user =User.query.filter_by(username=username).first()
        if user:
            return render_template('register.html',error=True)
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('register.html',email_error=True)
        user = User(username=username, email=email, password=password, fullname=fullname)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user is not None:
            session['username'] = username
            return redirect(url_for('index',id=user.id))
        else:
            return render_template('login.html',error = True)

    return render_template('login.html')

@app.route('/dashboard')
def index():
    user = session.get('username')
    return render_template('index.html',username=user)


if __name__ == '__main__':
    app.run(debug=True)