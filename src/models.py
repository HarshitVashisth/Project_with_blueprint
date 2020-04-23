from src import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    posts = db.relationship('BlogPost', backref='author')

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    text= db.Column(db.Text())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
