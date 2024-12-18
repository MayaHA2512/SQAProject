import pytest
from unittest.mock import patch
from app import app as flask_app

# --- Fixtures ---
@pytest.fixture
def app():
    """Fixture to set up the Flask application."""
    flask_app.testing = True
    yield flask_app

@pytest.fixture
def client(app):
    """Fixture to set up the test client."""
    with app.test_client() as client:
        yield client

# --- Tests ---
def test_index_route(client):
    """Test if the index page loads correctly."""
    response = client.get("/")
    assert response.status_code == 201
    assert b"Blog Posts" in response.data

def test_create_post_page(client):
    """Test if the create post page loads correctly."""
    response = client.get("/create")
    assert response.status_code == 200
    assert b"Create Post" in response.data


