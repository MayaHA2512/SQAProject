from flask import Flask, render_template, request, redirect, url_for, flash
from models import BlogPost, db, Author
from statistics import median, mean
import logging


class BlogApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object('config')  # Load configuration from config.py
        self.app.secret_key = "yrewrwerwjroweirj"  # Needed for flash messages
        self.user = None
        self.logger = logging.getLogger('__logger__')

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()  # Create tables if they don’t exist

        self.setup_routes()

    def encrypt_password(self, password):
        pass

    def setup_routes(self):
        @self.app.route("/", methods=["GET", "POST"])
        def index():
            if request.method == "POST":
                username = request.form["username"]
                password = request.form["password"]

                if username == "foo_user":  # Example check
                    self.user = username
                    return render_template("login.html")
                else:
                    self.logger.info('User does not exist')
                    flash('Failed to get stats: no posts available', "danger")
                    return render_template("login.html")
            return render_template("login.html")

        @self.app.route("/login")
        def login():
            return render_template("login.html")

        @self.app.route("/register", methods=["GET", "POST"])
        def register():
            if request.method == "POST":
                username = request.form["username"]
                password = request.form["password"]
                author = Author(name=username, password=password)
                db.session.add(author)
                db.session.commit()
                return render_template("index.html")
            return render_template("register.html")

        @self.app.route("/create", methods=["GET"])
        def create_post_page():
            return render_template("create.html")

        @self.app.route("/create", methods=["POST"])
        def create_post_action():
            post = BlogPost(
                title=request.form["title"],
                content=request.form["content"],
                author=request.form["author"],
            )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("index"))

        @self.app.route("/post/<int:post_id>")
        def post(post_id):
            post = BlogPost.query.get_or_404(post_id)
            return render_template("post.html", post=post)

        @self.app.route("/edit/<int:post_id>", methods=["GET"])
        def edit_page(post_id):
            post = BlogPost.query.get_or_404(post_id)
            return render_template("edit.html", post=post)

        @self.app.route("/edit/<int:post_id>", methods=["POST"])
        def edit_action(post_id):
            post = BlogPost.query.get_or_404(post_id)
            post.title = request.form["title"]
            post.content = request.form["content"]
            db.session.commit()
            return redirect(url_for("post", post_id=post.id))

        @self.app.route("/delete/<int:post_id>", methods=["POST"])
        def delete_action(post_id):
            post = BlogPost.query.get_or_404(post_id)
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for("index"))

        @self.app.route("/stats")
        def stats():
            post_lengths = BlogPost.get_post_lengths()
            if post_lengths:
                return render_template(
                    "stats.html",
                    average_length=mean(post_lengths),
                    median_length=median(post_lengths),
                    max_length=max(post_lengths),
                    min_length=min(post_lengths),
                    total_length=sum(post_lengths),
                )
            else:
                self.logger.info('Failed to get stats: no posts available')
                flash('Failed to get stats: no posts available', "danger")
                return render_template("index.html")

    def run(self, debug=True):
        self.app.run(debug=debug)


if __name__ == "__main__":
    blog_app = BlogApp()
    blog_app.run()