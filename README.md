# SQA Project

**Project Overview**
This is a Flask web application that enables users to upload, delete, and edit posts. It serves as a solid foundation for various types of websites, such as recipe platforms, news sites, and educational portals, where users can both explore content created by others and contribute their own.

**Table of contents**

- [Installation](#Installation)
- [Configuration](#Configuration)
- [Usage](#Usage)
- [Testing](#Testing)
- [Contributing](#Contributing)




## Installation
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/blogapp.git
   cd blogapp

2. Create a virtual environment
   ```bash
   python -m venv venv

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt



## Configuration

1. Set up the environment variables for configuration:
   ```bash
   export FLASK_APP=app.py
    export FLASK_ENV=development
    export SECRET_KEY='your_secret_key'
    export DATABASE_URI='sqlite:///blogapp.db'

## Usage

1. To run the application locally, use the following command:
   ```bash
   flask run
   
2. Navigate to http://localhost:5000 in your browser
3. To create a new post, log in with valid credentials, and navigate to the "/create" route.

## Testing

1. To run tests, use the following command:
   ```bash
   pytest --cov=app
2. To test using Flask's test client:
   ```bash
   def test_create_post(client):
    response = client.post('/create', data={'title': 'New Post', 'content': 'This is a new post.'})
    assert response.status_code == 302
    assert b'Post Created' in response.data

## Contributing

1. Fork the repository.
2. Create a new branch
3. (git checkout -b feature/xyz).
4. Make your changes.
5. Commit your changes (git commit -am 'Add new feature').
6. Push to the branch (git push origin feature/xyz).
7. Open a pull request to merge your changes into the main branch.

   
