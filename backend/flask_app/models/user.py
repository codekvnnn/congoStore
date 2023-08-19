from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash, session, jsonify

import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&+=])(?=.*[a-z]).{8,}$')

class User:
    db = "congo_schema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.address = data['address']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        if cls.validate_user_registration_data(data):
            data = cls.parse_registration_data(data)
            query = """INSERT INTO users (first_name, last_name, address, email, password)
                    VALUES (%(first_name)s, %(last_name)s, %(address)s, %(email)s, %(password)s);"""   
            user_id = connectToMySQL(cls.db).query_db(query, data)
            session['user_id'] = user_id
            session['user_name'] = f"{data['first_name']} {data['last_name']}"
            return True
        return False
 
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(user) for user in results] if results else results
    
    @classmethod
    def get_user_by_id(cls, id):
        query = """SELECT * FROM users
                   WHERE id=%(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        return cls(results[0]) if results else results
    
    @classmethod
    def get_user_by_email(cls, email):
        query = """SELECT * FROM users
                   WHERE email=%(email)s;"""
        results = connectToMySQL(cls.db).query_db(query, {'email': email.lower().strip()})
        return cls(results[0]) if results else results
    
    @classmethod
    def update_user(cls, data):
        if cls.validate_user_update_data(data):
            data = cls.parse_update_data(data)
            query = """UPDATE users
                    SET first_name=%(first_name)s, last_name=%(last_name)s, address=%(address)s, email=%(email)s
                    WHERE id=%(id)s;"""
            connectToMySQL(cls.db).query_db(query, data)
            session['user_name'] = f"{data['first_name']} {data['last_name']}"
            return True
        return False
    
    @classmethod
    def delete_user(cls, user_id):
        query = """DELETE FROM users
                   WHERE id=%(id)s;"""
        return connectToMySQL(cls.db).query_db(query, {'id':user_id})

    @staticmethod
    def validate_user_registration_data(data):
        is_valid = True
        if not data['first_name'].replace(' ','').isalpha(): # and len(data['first_name']):
            flash('First name cannot contain numbers')
            is_valid = False
        if len(data['first_name']) < 3:
            flash('First name must be at least 3 characters long')
            is_valid = False
        if not data['last_name'].replace(' ','').isalpha(): # and len(data['last_name']):
            flash('Last name cannot contain numbers')  
            is_valid = False      
        if len(data['last_name']) < 3:
            flash('Last name must be at least 3 characters long')
            is_valid = False
        if len(data['address']) < 10:
            flash('Address must be at least 10 characters long')
            is_valid = False
        if not EMAIL_REGEX.match(data['email'].lower().strip()):
            flash('Invalid email address.')
            is_valid = False
        if User.get_user_by_email(data['email']):
            flash('Email address already registered')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters long')
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash('Password Requires one captial, one digit, and one of the following symbols : !@#$%^&+=')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('The paswords do not macth')
            is_valid = False
        return is_valid
    
    @staticmethod
    def parse_registration_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name'].strip()
        parsed_data['last_name'] = data['last_name'].strip()
        parsed_data['address'] = data['address'].strip()
        parsed_data['email'] = data['email'].lower().strip()
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data
    
    @staticmethod
    def validate_user_update_data(data):
        is_valid = True
        if not data['first_name'].replace(' ','').isalpha():
            flash('First name cannot contain numbers')
            is_valid = False
        if len(data['first_name']) < 3:
            flash('First name must be 3 characters long')
            is_valid = False
        if not data['last_name'].replace(' ','').isalpha():
            flash('Last name cannot contain numbers')  
            is_valid = False      
        if len(data['last_name']) < 3:
            flash('Last name must be 3 characters long')
            is_valid = False
        if len(data['address']) < 10:
            flash('Address must be at least 10 characters long')
            is_valid = False
        if not EMAIL_REGEX.match(data['email'].lower().strip()):
            flash('Invalid email address.')
            is_valid = False
        user = User.get_user_by_email(data['email'])
        if user and user.id != session['user_id']:
            flash('Email address already registered')
            is_valid = False
        return is_valid

    @staticmethod
    def parse_update_data(data, update_id=False):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name'].strip()
        parsed_data['last_name'] = data['last_name'].strip()
        parsed_data['address'] = data['address'].strip()
        parsed_data['email'] = data['email'].lower().strip()
        parsed_data['id'] = session['user_id']
        return parsed_data

    @staticmethod
    def login_user(data):
        user = User.get_user_by_email(data['email'])
        if user and bcrypt.check_password_hash(user.password, data['password']):
            session['user_id'] = user.id
            session['user_name'] = f"{user.first_name} {user.last_name}"
            return True
        flash('Login failed. Please try again.')
        return False
    

    # API Specific Class methods

    @classmethod
    def create_user_api(cls, data):
        if cls.validate_user_registration_data(data):
            data = cls.parse_registration_data(data)
            query = """INSERT INTO users (first_name, last_name, address, email, password)
                    VALUES (%(first_name)s, %(last_name)s, %(address)s, %(email)s, %(password)s);"""   
            user_id = connectToMySQL(cls.db).query_db(query, data)
            return User.get_user_by_id_api(user_id)
        return False

    @classmethod
    def get_user_by_id_api(cls, id):
        results = cls.get_user_by_id(id)
        return User.serialize_user(results)


    # API Specific static methods

    @staticmethod
    def login_user_api(data):
        user = User.get_user_by_email(data['email'])
        if user and bcrypt.check_password_hash(user.password, data['password']):
            return User.serialize_user(user)
        errors = {
            'email' : ["Invalid Credentials"],
            'password' : ["Invalid Credentials"]
        }
        return jsonify(message="Invalid email or password", errors=errors)

    @staticmethod
    def validate_user_registration_data_api(data):
        is_valid = True
        errors = {}
        if not data['first_name'].replace(' ','').isalpha():
            if 'first_name' not in errors:
                errors['first_name'] = []
            errors['first_name'].append('First name cannot contain numbers')
            is_valid = False
        if len(data['first_name']) < 3:
            if 'first_name' not in errors:
                errors['first_name'] = []
            errors['first_name'].append('First name must be at least 3 characters long')
            is_valid = False
        if not data['last_name'].replace(' ','').isalpha(): # and len(data['last_name']):
            if 'last_name' not in errors:
                errors['last_name'] = []
            errors['last_name'].append('Last name cannot contain numbers')  
            is_valid = False      
        if len(data['last_name']) < 3:
            if 'last_name' not in errors:
                errors['last_name'] = []
            errors['last_name'].append('Last name must be at least 3 characters long')
            is_valid = False
        if len(data['address']) < 10:
            errors['address'] = []
            errors['address'].append('Address must be at least 10 characters long')
            is_valid = False
        if not EMAIL_REGEX.match(data['email'].lower().strip()):
            if 'email' not in errors:
                errors['email'] = []
            errors['email'].append('Invalid email address.')
            is_valid = False
        if User.get_user_by_email(data['email']):
            if 'email' not in errors:
                errors['email'] = []
            errors['email'].append('Email address already registered')
            is_valid = False
        if len(data['password']) < 8:
            if 'password' not in errors:
                errors['password'] = []
            errors['password'].append('Password must be at least 8 characters long')
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            if 'password' not in errors:
                errors['password'] = []
            errors['password'].append('Password requires one captial, one digit, and one of the following symbols : !@#$%^&+=')
            is_valid = False
        if data['password'] != data['confirm_password']:
            if 'password' not in errors:
                errors['password'] = []
            errors['password'].append('The paswords do not macth')
            is_valid = False
        return is_valid, errors
    
    @staticmethod
    def serialize_user(user):
        user_dict = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': user.address,
            'email': user.email,
            'password' : user.password,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
        return user_dict