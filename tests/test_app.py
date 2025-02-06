import pytest
from app import BlogApp  # Assuming BlogApp is your class
import random

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
    # Register first
    client.post("/", data={"username": "testuser1", "password": "testpassword1"})

    # Test login with the new user
    response = client.post("/", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert b"Create Post" in response.data  # After login, the index page should show "Create Post"

def test_create_post(client):
    """Test if a user can create a blog post."""
    # Register and log in first
    client.post("/register", data={"username": "testuser", "password": "testpassword"})
    client.post("/", data={"username": "testuser", "password": "testpassword"})

    # Test creating a new post
    response = client.post("/create", data={"title": "Test Post", "content": "This is a test post.", "author": "testuser"})
    assert response.status_code == 302  # Redirect to index page after creation
    assert b"Create Post" in response.data  # Ensure the page redirects back to index



