from flask import Flask, render_template, request, redirect, url_for
from models import BlogPost, db

app = Flask(__name__)
app.config.from_object('config')  # Load configuration from config.py and particularly the DBMS URI

with app.app_context():
    db.init_app(app)  # It connects the SQLAlchemy db object with the Flask app and the DBMS engine
    db.create_all()  # Create the database tables for all the models

posts = [
    {
        "id": "1",
        "title": "Getting Started with Flask",
        "content": "Flask is a lightweight web framework in Python, perfect for beginners and professionals alike.",
        "author": "Alice",
        "created_at": "2024-12-10"
    },
    {
        "id": "2",
        "title": "Flask vs Django: Which to Choose?",
        "content": "While Flask is lightweight and flexible, Django provides a robust full-stack framework. Choose based on your project needs.",
        "author": "Bob",
        "created_at": "2024-12-09"
    },
    {
        "id": "3",
        "title": "Building a Blog App with Flask",
        "content": "Learn how to create a simple blog application using Flask, complete with dynamic routing and templates.",
        "author": "Charlie",
        "created_at": "2024-12-08"
    }
]

@app.route("/")
def index():
    return render_template("index.html", posts=BlogPost.query.all())

@app.route("/create", methods=["GET"])
def create_post_page():
    return render_template("create.html")

@app.route("/create", methods=["POST"])
def create_post_action():
    post = BlogPost(
        title=request.form["title"],
        content=request.form["content"],
        author=request.form["author"],
    )
    db.session.add(post)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/post/<int:post_id>")
def post(post_id):
    post_to_display={}
    for post in posts:
        if(post["id"] == str(post_id)):
            post_to_display=post
            break  
    return render_template("post.html", post=post_to_display)
