from flask import Flask, render_template
app = Flask(__name__)

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
    return render_template("index.html", posts=posts)

@app.route("/post/<int:post_id>")
def post(post_id):
    post_to_display={}
    for post in posts:
        if(post["id"] == str(post_id)):
            post_to_display=post
            break
    print(post)
    print("hi")
    return render_template("post.html", post=post_to_display)
