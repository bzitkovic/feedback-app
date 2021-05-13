from email import message
from enum import unique
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import selectinload
from sendMail import sendMailFeedback, sendMailRegister

app = Flask(__name__)

ENV = 'dev'
LOGIN = False
USER = ''

if(ENV == 'dev'):
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:0000@localhost/class_grading'
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = ''
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Professor(db.Model):
    __tablename = 'professor'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), unique = True)

    def __init__(self, name):
        self.name = name

class User(db.Model):
    __tablename = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key = True)
    professor = db.Column(db.String(150))
    subject = db.Column(db.String(150))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, professor, subject, rating, comments):
        self.professor = professor
        self.subject = subject
        self.rating = rating
        self.comments = comments

@app.route('/registerPage')
def redirectRegister():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']

        if(username == '' or password == ''):
            return render_template('login.html', message='Please enter required fields')

        user = User(username, password)

        db.session.add(user)
        db.session.commit()

        sendMailRegister(username)

        return render_template('login.html', message='You have successfully been registered!')

@app.route('/login', methods=['POST'])
def login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']

        if(username == '' or password == ''):
            return render_template('login.html', message='Please enter required fields')

        user = User(username, password)
        dbUser = User.query.filter_by(username=user.username).first()

        if(dbUser != None):
            if(user.password == dbUser.password):
                LOGIN = True
                USER = user.username    

                professors = Professor.query.all()
                subjects = Subject.query.all()

                return render_template('index.html', message=f'Welcome { USER }', professors=professors, subjects=subjects)
            else:
                return render_template('login.html', message='Wrong login credentials')

        else:   
            return render_template('login.html', message='Wrong login credentials')

@app.route('/')
def index():
    if(LOGIN == False):
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if(request.method == 'POST'):
        professor = request.form['professor'] 
        subject = request.form['subject'] 
        rating = request.form['rating'] 
        comments = request.form['comments'] 
        
        if(professor == '' or subject == ''):
            return render_template('index.html', message='Please enter required fields')

        data = Feedback(professor, subject, rating, comments)
        db.session.add(data)
        db.session.commit()

        sendMailFeedback(professor, subject, rating, comments)

        return render_template('success.html')

if __name__ == '__main__':
    app.run()