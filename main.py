 from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bluebook.db'
db = SQLAlchemy(app)

# পোস্টের জন্য মডেল
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

# নিউজ ফিড রুট
@app.route('/')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

# নতুন পোস্ট সেভ করার রুট
@app.route('/post', methods=['POST'])
def post():
    user = request.form.get('username')
    text = request.form.get('content')
    new_post = Post(username=user, content=text)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)