import pytest
from app import BlogApp  # Assuming BlogApp is your class
import random
from models import Author, BlogPost

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
    response = client.post("/", data={"username": "testuser3", "password": "testpassword3"})
    assert response.status_code == 200
    assert b"Login" in response.data  # After login, the index page should show "Create Post"


def test_create_post(client):
    """Test creating a post after login."""

    # Now login with the new user's credentials
    response = client.post("/", data={"username": "testuser3", "password": "testpassword3"})
    assert response.status_code == 200  # Check successful login

    # Fetch the user from the database to avoid the 'str' issue
    user = Author.query.filter_by(name="testuser3").first()

    # Create a post with the User instance as the author
    response = client.post("/create", data={
        "title": "foo",
        "content": "fe",
        "author": user.id  # Pass author_id, not the author object itself
    })

    # Check if the post was created and the page redirected as expected
    assert response.status_code == 200  # Should be a redirect after creating the post
    assert b"Post Created" in response.data  # Verify success message or page content





