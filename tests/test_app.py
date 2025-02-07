import pytest
from app import BlogApp
import random
from models import Author, BlogPost, db
from unittest.mock import patch
from statistics import mean, median

# --- Fixtures ---
@pytest.fixture
def app():
    """Fixture to set up the Flask application."""
    # Initialize the app with __name__ so it's recognized properly
    app = BlogApp()  # Since BlogApp already initializes the Flask app
    app.app.testing = True  # Enable testing mode
    yield app.app  # Yield the actual Flask app instance for testing

@pytest.fixture
def client(app):
    """Fixture to set up the test client."""
    with app.test_client() as client:
        yield client

# --- Tests ---
def test_index_route(client):
    """Test if the index page loads correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Login" in response.data

def test_create_post_page(client):
    """Test if the create post page loads correctly."""
    response = client.get("/create")
    assert response.status_code == 200
    assert b"Create Post" in response.data

def test_register(client):
    """Test if the registration page works and creates a user."""
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data

    # Test registering a new user
    response = client.post("/register", data={"username": random.randint(0, 214912410), "password": "testpassword1"})
    assert response.status_code == 200
    assert b"Login" in response.data  # After registration, it should redirect to login page

def test_login(client):
    """Test if the login page works and the user can log in."""
    # Test login with the new user
    response = client.post("/", data={"username": "testing1", "password": "testing1"})
    assert response.status_code == 200
    assert b"Blog Posts" in response.data  # After login, the index page should show "Create Post"


def test_create_post(client):
    """Test creating a post after login."""

    # Now login with the new user's credentials
    response = client.post("/", data={"username": "testing1", "password": "testing1"})
    assert response.status_code == 200  # Check successful login

    # Fetch the user from the database to avoid the 'str' issue
    user = Author.query.filter_by(name="testuser1").first()
    if not user:
        # Create a new test user
        user = Author(name="testuser1", password="testpassword1")  # Ensure this password is encrypted if needed
        db.session.add(user)
        db.session.commit()

    # Create a post with the User instance as the author
    response = client.post("/create", data={
        "title": "foo",
        "content": "fe",
        "author": user.name  # Pass author_id, not the author object itself
    })
    # TODO: Add logic to wipe these after the test
    # Check if the post was created and the page redirected as expected
    assert response.status_code == 200  # Should be a redirect after creating the post
    assert b"Post Created" in response.data  # Verify success message or page content


def test_post_by_user(client, app):
    with app.app_context():
        user = Author.query.filter_by(name="testing1").first()
        if not user:
            user = Author(name="testing1", password="testing1")
            db.session.add(user)
            db.session.commit()

        response = client.post("/", data={"username": "testing1", "password": "testing1"})
        assert response.status_code == 200
        assert b"Create Post" in response.data

def test_logout(client):
    """Test if the login page works and the user can log in."""
    # Test login with the new user
    response = client.post("/", data={"username": "testing1", "password": "testing1"})
    assert response.status_code == 200
    response = client.get("/logout")
    assert response.status_code == 302
    assert b"You should be redirected" in response.data

def test_stats_with_posts(client):
    """Test the /stats route when posts are available."""
    # Mock the return value of BlogPost.get_post_lengths()
    post_lengths = [100, 200, 300]

    with patch("app.BlogPost.get_post_lengths", return_value=post_lengths):
        response = client.get("/stats")
        assert response.status_code == 200
        assert b"Stats" in response.data
        assert str(mean(post_lengths)).encode() in response.data
        assert str(median(post_lengths)).encode() in response.data
        assert str(max(post_lengths)).encode() in response.data
        assert str(min(post_lengths)).encode() in response.data


def test_stats_no_posts(client):
    """Test the /stats route when no posts are available."""
    with patch("app.BlogPost.get_post_lengths", return_value=[]):
        response = client.get("/stats")
        assert response.status_code == 200
        assert b"Failed to get stats: no posts available" in response.data




