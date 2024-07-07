# user.py

from database import Database

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserManager:
    def __init__(self, db):
        self.users = []
        self.db = db

        # Load existing user data from the database
        data = self.db.read_data()
        if data:
            for line in data.split('\n'):
                if line:
                    username, password = line.split(',')
                    self.users.append(User(username, password))

    def register(self, username, password):
        # Check if username already exists
        for user in self.users:
            if user.username == username:
                print("Username already exists. Please choose a different one.")
                return False

        # If username is unique, create a new user
        new_user = User(username, password)
        self.users.append(new_user)

        # Save the new user data to the database
        self.db.append_data(f"{username},{password}")

        print("Registration successful. You can now log in.")
        return True

    def authenticate(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False
