from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re
# need to import re for REGEX

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# 2nd need to validate email that email is in a '@' format

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL("family_list").query_db(query, data)

    @classmethod
    def email_exists(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email": email}
        result = connectToMySQL("family_list").query_db(query, data)
        return bool(result)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("family_list").query_db(query,data)
    # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("family_list").query_db(query,data)
        return cls(result[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        # Start of validations
    # Validates that email is in '@' format
        if not EMAIL_REGEX.match(user['email']):
            flash("Enter a valid email address")
            is_valid = False
        elif User.email_exists(user['email']):
            flash("Email already exists. Please choose a different email")
    # Validates that username is at least 2 characters
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters")
            is_valid = False

        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters")
            is_valid = False

    # Validates that password is at least 8 characters
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False

    # Validates that password and confirm password match
        if user['password'] != request.form['confirm_password']:
            flash("Password and Confirm Password must match")
            is_valid = False

        return is_valid
