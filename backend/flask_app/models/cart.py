from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import product
from flask import flash, session

class Cart:
    db = 'congo_schema'

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.isPaid = data['isPaid']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.products = []

    @classmethod
    def add_cart(cls, data):
        if cls.validate_cart_creation_data(data):
            data = {'user_id' : session['user_id'],
                    'name': data['name'],
                    'description': data['description'],
                    'category': data['category'],
                    'quantity': data['quantity'],
                    'price' : data['price'],
                    'img_url' : data['img_url']}
            
            query = """INSERT INTO products (user_id, name, description, category, quantity, price, img_url)
                    VALUES (%(user_id)s, %(name)s, %(description)s, %(category)s, %(quantity)s, %(price)s, %(img_url)s);"""   
            connectToMySQL(cls.db).query_db(query, data)
            return True
        return False