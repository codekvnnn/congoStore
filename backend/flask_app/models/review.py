from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import product
from flask import flash, session

import re

RATING_REGEX = re.compile(r'^\*{1,5}$')

class Review:
    db = 'congo_schema'

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.product_id = data['product_id']
        self.content = data['content']
        self.rating = data['rating']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def add_review(cls, data, product_id):
        if cls.validate_review_creation_data(data, product_id):
            data = {'user_id' : session['user_id'],
                    'product_id': product_id,
                    'content': data['content'],
                    'rating' : data['rating']
                    }
            
            query = """INSERT INTO reviews (user_id, product_id, content, rating)
                    VALUES (%(user_id)s, %(product_id)s, %(content)s, %(rating)s);"""   
            connectToMySQL(cls.db).query_db(query, data)
            return True
        return False
    
    @staticmethod
    def validate_review_creation_data(data, product_id):
        is_valid = True
        if len(data['content']) < 5:
            flash('Review must be at least 5 characters long')
            is_valid = False
        if not RATING_REGEX.match(data['rating']):
            flash('Rating must be 1 to 5 asteriks')
            is_valid = False
        if not product.Product.get_product_by_id(product_id):
            flash('Invalid Product')
            is_valid = False
        return is_valid
    

    # API Specific Methods

    @classmethod
    def add_review_api(cls, data, product_id):
        if cls.validate_review_creation_data(data, product_id):
            data = {'user_id' : data['user_id'],
                    'product_id': product_id,
                    'content': data['content'],
                    'rating' : data['rating']
                    }
            
            query = """INSERT INTO reviews (user_id, product_id, content, rating)
                    VALUES (%(user_id)s, %(product_id)s, %(content)s, %(rating)s);"""   
            connectToMySQL(cls.db).query_db(query, data)
            return True
        return False

    @staticmethod
    def validate_review_creation_data_api(data, product_id):
        is_valid = True
        errors = {}
        if len(data['content']) < 5:
            errors['content'] = []
            errors['content'].append('Review must be at least 5 characters long')
            is_valid = False
        if not RATING_REGEX.match(data['rating']):
            errors['rating'] = []
            errors['rating'].append('Rating must be 1 to 5 asteriks')
            is_valid = False
        if product.Product.get_product_by_id(product_id).id == None:
            errors['product_id'] = []
            errors['product_id'].append('Invalid Product')
            is_valid = False
        return is_valid, errors
   
    @staticmethod
    def serialize_review(review):
        review_dict = {
            'id': review.id,
            'user_id': review.user_id,
            'product_id': review.product_id,
            'content': review.content,
            'rating' : review.rating,
            'creator' : user.User.serialize_user(review.creator),
            'created_at': review.created_at,
            'updated_at': review.updated_at
        }
        return review_dict
        