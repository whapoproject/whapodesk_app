# database.py
import os

class Database:
    def __init__(self, filename):
        self.filename = filename

    def read_data(self):
        if not os.path.exists(self.filename):
            return ""
        with open(self.filename, 'r') as file:
            return file.read()

    def save_data(self, data):
        with open(self.filename, 'w') as file:
            file.write(data)

    def append_data(self, data):
        with open(self.filename, 'a') as file:
            file.write(data)
