from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.String(100), db.ForeignKey('author.name'), nullable=False)  # Foreign Key

    def __str__(self):
        return f'"{self.title}" by {self.author} ({self.created_at:%Y-%m-%d})'

    @staticmethod
    def get_post_lengths():
        # An example of how to use raw SQL inside a model
        sql = text("SELECT length(title) + length(content) FROM blog_post")
        return db.session.execute(sql).scalars().all()  # Returns just the integers


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100), nullable=False) # TODO: encrypt this maybe using ferret
    name = db.Column(db.String(100), nullable=False, unique=True)
    posts = db.relationship('BlogPost', backref='author', lazy=True)  # One-to-Many relationship

    def __str__(self):
        return self.name
