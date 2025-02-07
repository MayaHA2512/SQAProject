# SQA Project

**Project Overview**
This is a Flask web application that enables users to upload, delete, and edit posts. It serves as a solid foundation for various types of websites, such as recipe platforms, news sites, and educational portals, where users can both explore content created by others and contribute their own.

**Table of contents**

- [Installation](#Installation)
- [Configuration](#Configuration)
- [Usage](#Usage)
- [Testing](#Testing)
- [Contributing](#Contributing)
- [Contributions](#Contributions)
- [Features](#Features)
- [Challenges and Solutions](#ChallengesandSolutions)
- [Evidence for Marking Criteria](#EvidenceforMarkingCriteria)
- [DB Configuration](#DBConfiguration)



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

   
## Contributions

This project was completed individually by [Your Name]. All aspects of the application, including feature implementation, testing, security enhancements, and CI/CD setup, were handled independently.

## Features

- **User Authentication**: Users can register, log in, and log out.
- **CRUD Operations**: Users can create, edit, and delete blog posts.
- **Role-Based Access Control**: Only the author can edit or delete their own posts.

## Challenges and Solutions

Throughout the development process, I faced a few key challenges that required careful consideration and problem-solving.

## User Authentication and Authorization:

1. - Challenge: Implementing secure user authentication was a critical requirement. Ensuring that passwords were stored securely and users could only access and modify their own posts posed a challenge.
   - Solution: I used Fernet encryption for securely hashing user passwords, ensuring they were stored in an encrypted format in the database. For authorization, I implemented role-based access control (RBAC) to restrict post-editing and deletion to the respective authors only.
  
2. - Challenge: Comprehensive testing, especially for edge cases, was a challenge because it required thinking about potential user behavior and error scenarios. Writing tests for scenarios like invalid logins and incorrect post submissions needed careful consideration.
   - Solution: I wrote a comprehensive suite of unit and integration tests, ensuring edge cases were tested (e.g., invalid user credentials or unauthorized post modifications). This helped achieve high code coverage and ensure the application’s stability.
  
## Evidence for Marking Criteria

**User Authentication**

User Authentication (Login & Registration)

The authentication system allows users to register, log in, and access blog posts. Here's an overview of how the authentication flow works:

1. User Registration:
   Users can create a new account by providing a username and password.
   The password is securely encrypted using Fernet encryption before being stored in the database. This           ensures that even if the database is compromised, passwords remain safe.

   Code Implementation:
   In the registration route (/register), the application accepts a POST request where the user's username and    password are submitted. We do a check to ensure that the username doesn't already exist in the database
   The password is then encrypted using the encrypt_password method:
   encrypted_password = self.encrypt_password(password)
   The encrypted password is stored in the database under the Author model.
   
   UI:
   ![Untitled 2](https://github.com/user-attachments/assets/f5442de1-9f2c-459d-9233-466b373ee625)
   
   ![Untitled4535](https://github.com/user-attachments/assets/60f2746f-05f5-45eb-9b66-401d87a692cc)

   but if the account already exists:
   
   ![Untitledrewrerw](https://github.com/user-attachments/assets/fecdfaf2-d4e0-4f6c-a523-7a84ecf317e4)

   Code Snippet:
   ```python

   @self.app.route("/register", methods=["GET", "POST"])
        def register():
            if request.method == "POST":
                username = request.form["username"]
                password = request.form["password"]

                # Check if the username already exists in the database
                existing_author = Author.query.filter_by(name=username).first()
                if existing_author:
                    flash('Username already exists. Please choose a different one.', 'danger')
                    return render_template("register.html")

                # Encrypt the password before storing it
                encrypted_password = self.encrypt_password(password)

                # Create a new author and add to the database
                author = Author(name=username, password=encrypted_password)
                db.session.add(author)
                db.session.commit()

                # Redirect to login page after successful registration
                flash('Registration successful! You can now log in.', 'success')
                return render_template("login.html")

            return render_template("register.html")

   ````

2. User Login:
   Process Overview:
   - To login, users enter their username and password.
   - The entered password is decrypted and compared with the stored encrypted password.
   - If the credentials are correct, the user is granted access to the homepage and can see the posts.
   
   Code Implementation:
   - In the login route (/login), the application accepts the POST request and checks the credentials by calling the check_credentials method:
     ```python
     author = self.check_credentials(username, password)
     ```
   - Inside check_credentials, the provided password is decrypted using the decrypt_password method:
     ```python
     decrypted_password = self.decrypt_password(author.password)
     ```
   -  The login is successful if the decrypted password matches the entered password.

  UI:

  Successful
  ![Untitledfeiofwejifewoi](https://github.com/user-attachments/assets/fc3f2f9e-86c7-4803-84e2-d37509d2c8cb)

  ![Untitledrwerwerwr](https://github.com/user-attachments/assets/aa99b846-2b66-49cc-8f0a-b0d36c822f86)

  Unsuccessful login:
  
  ![Untitlederowerjweor](https://github.com/user-attachments/assets/4df90082-2f58-43d0-85c5-d6da2b589500)

  
Code snippet:

   ```python
    @self.app.route("/", methods=["GET", "POST"])
           def login():
               if request.method == "POST":
                   username = request.form["username"]
                   password = request.form["password"]
                   author = self.check_credentials(username, password)
                   self.user = author
                   if author:
                       return render_template('index.html', posts=self.posts(), user=self.user)
                   else:
                       self.logger.info('User does not exist')
                       flash('Something went wrong: either username or password are incorrect', "danger")
                       return render_template("login.html")
               return render_template("login.html")
   
   ```

**Role Baaed Access control (RBAC)**

In this project, RBAC is implemented to control who can edit and delete posts.

- Authors can edit or delete only their posts.
- Readers (regular users) cannot edit or delete any posts.

You can see if I am logged in as 'mayaisalegend2', I cannot delete a post by testing1:

![Untitleddqiodjqdi](https://github.com/user-attachments/assets/366df65f-3764-4649-927d-9673563ddd23)

![Untitleddqiodqjdqw](https://github.com/user-attachments/assets/7e353096-99bf-47e6-8b91-8220d0671198)





