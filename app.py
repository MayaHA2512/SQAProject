from flask import Flask, render_template, request, redirect, url_for, flash
from models import BlogPost, db, Author
import config
from statistics import median, mean
import logging
from decryptor import key
from cryptography.fernet import Fernet

class BlogApp(Flask):
    def __init__(self):
        self.app = Flask(__name__)
        self.config = config
        self.app.config.from_object('config')  # Load configuration from config.py
        self.app.secret_key = "yrewrwerwjroweirj"  # Needed for flash messages
        self.user = None
        self.logger = logging.getLogger('__logger__')
        self.fernet_suite = Fernet(key)

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()  # Create tables if they don’t exist

        self.setup_routes()

    def encrypt_password(self, password):
        return self.fernet_suite.encrypt(bytes(password, 'utf-8')) # TODO: Wrap in try except

    def decrypt_password(self, password):
        password = self.fernet_suite.decrypt(password)
        return password.decode('utf-8')

    def check_credentials(self, username, password):
        authors = Author.query.all()
        author = [author for author in authors if author.name == username and self.decrypt_password(author.password) == password]
        if author:
            return author[0]

    def posts(self):
        return BlogPost.query.all()

    def posts_by_user(self):
        return [post for post in self.posts if post.author_id == self.user.name]

    def setup_routes(self):

        @self.app.route("/home")
        def home():
            return render_template("index.html", posts=self.posts())

        @self.app.route("/", methods=["GET", "POST"])
        def login():
            if request.method == "POST":
                username = request.form["username"]
                password = request.form["password"]
                author = self.check_credentials(username, password)
                self.user = author
                if author:
                    return render_template('index.html', posts=self.posts())
                else:
                    self.logger.info('User does not exist')
                    flash('Failed to get stats: no posts available', "danger")
                    return render_template("login.html")
            return render_template("login.html")


        @self.app.route("/register", methods=["GET", "POST"])
        def register():
            if request.method == "POST":
                username = request.form["username"]
                password = request.form["password"]
                encrypted_password = self.encrypt_password(password)
                author = Author(name=username, password=encrypted_password)
                db.session.add(author)
                db.session.commit()
                return render_template("login.html")
            return render_template("register.html")

        @self.app.route("/create", methods=["GET"])
        def create_post_page():
            return render_template("create.html")

        @self.app.route("/create", methods=["POST"])
        def create_post_action():
            form_author = request.form["author"]  # Make sure you pass the author ID, not the name # Fetch the Author object by ID
            author = [author for author in Author.query.all() if author.name == form_author]
            if not author:
                flash("Author not found", "danger")
                return redirect(url_for("create_post_page"))

            post = BlogPost(
                title=request.form["title"],
                content=request.form["content"],
                author=author[0],  # Pass the Author object instead of its ID
            )
            db.session.add(post)
            db.session.commit()
            flash("Post Created", "success")  # Flash a success message
            return render_template('index.html', posts=self.posts())

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
            return render_template('index.html', posts=BlogPost.query.all())

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
                return render_template('index.html', posts=self.posts())

    def run(self, debug=True):
        self.app.run(debug=debug, port=7000)


if __name__ == "__main__":
    blog_app = BlogApp()
    blog_app.run()