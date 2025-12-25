from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "secret_key_123" # আপনার সিকিউরিটি কী

# ডাটাবেস সেটআপ
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'social.db')
db = SQLAlchemy(app)

# ইউজার টেবিল
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# পোস্ট টেবিল
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)

# ডাটাবেস তৈরি করা
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'user' in session:
        posts = Post.query.all()
        return render_template('index.html', posts=posts, user=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        user = User.query.filter_by(username=uname).first()
        
        if user and check_password_hash(user.password, pword):
            session['user'] = uname
            return redirect(url_for('home'))
        return "ভুল পাসওয়ার্ড বা ইউজারনেম!"
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    uname = request.form['username']
    pword = generate_password_hash(request.form['password'])
    new_user = User(username=uname, password=pword)
    db.session.add(new_user)
    db.session.commit()
    return "রেজিস্ট্রেশন সফল! এখন লগইন করুন।"

@app.route('/post', methods=['POST'])
def post():
    if 'user' in session:
        text = request.form['content']
        new_post = Post(content=text, author=session['user'])
        db.session.add(new_post)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)