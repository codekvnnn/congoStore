from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, review

from flask import flash, session
import json

class Product:
    db = 'congo_schema'

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.category = data['category']
        self.quantity = data['quantity']
        self.price = data['price']
        self.img_url = data['img_url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.reviews = []

    @classmethod
    def add_product(cls, data):
        if cls.validate_product_creation_data(data):
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

    @classmethod
    def get_all_products(cls):
        query = """SELECT products.*, users.*,
                   GROUP_CONCAT(reviews.id SEPARATOR ',') AS review_by_ids,
                   GROUP_CONCAT(review_users.id SEPARATOR ',') AS review_by_user_ids,
                   GROUP_CONCAT(review_users.first_name SEPARATOR ',') AS review_by_first_names,
                   GROUP_CONCAT(review_users.last_name SEPARATOR ',') AS review_by_last_names,
                   GROUP_CONCAT(review_users.address SEPARATOR ',') AS review_by_addresses,
                   GROUP_CONCAT(review_users.email SEPARATOR ',') AS review_by_emails,
                   GROUP_CONCAT(review_users.password SEPARATOR ',') AS review_by_passwords,
                   GROUP_CONCAT(review_users.created_at SEPARATOR ',') AS review_by_user_created_ats,
                   GROUP_CONCAT(review_users.updated_at SEPARATOR ',') AS review_by_user_updated_ats,
                   GROUP_CONCAT(reviews.content SEPARATOR ',') AS review_by_contents,
                   GROUP_CONCAT(reviews.rating SEPARATOR ',') AS review_by_ratings,
                   GROUP_CONCAT(reviews.product_id SEPARATOR ',') AS review_by_product_ids,
                   GROUP_CONCAT(reviews.created_at SEPARATOR ',') AS review_by_created_ats,
                   GROUP_CONCAT(reviews.updated_at SEPARATOR ',') AS review_by_updated_ats
                   FROM products
                   LEFT JOIN users ON products.user_id = users.id
                   LEFT JOIN reviews ON products.id = reviews.product_id
                   LEFT JOIN users AS review_users ON reviews.user_id = review_users.id
                   GROUP BY products.id;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_products = []
        for result in results:
            one_product = cls(result)
            one_product_creator_info = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'address': result['address'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']
            }
            one_product.creator = user.User(one_product_creator_info)

            review_by_ids = result['review_by_ids'].split(',') if result['review_by_ids'] else ''
            review_by_user_ids = result['review_by_user_ids'].split(',') if result['review_by_user_ids'] else ''
            review_by_first_names = result['review_by_first_names'].split(',') if result['review_by_first_names'] else ''
            review_by_last_names = result['review_by_last_names'].split(',') if result['review_by_last_names'] else ''
            review_by_addresses = result['review_by_addresses'].split(',') if result['review_by_addresses'] else ''
            review_by_emails = result['review_by_emails'].split(',') if result['review_by_emails'] else ''
            review_by_passwords = result['review_by_passwords'].split(',') if result['review_by_passwords'] else ''
            review_by_user_created_ats = result['review_by_user_created_ats'].split(',') if result['review_by_user_created_ats'] else ''
            review_by_user_updated_ats = result['review_by_user_updated_ats'].split(',') if result['review_by_user_updated_ats'] else ''
            review_by_product_ids = result['review_by_product_ids'].split(',') if result['review_by_product_ids'] else ''
            review_by_contents = result['review_by_contents'].split(',') if result['review_by_contents'] else ''
            review_by_ratings = result['review_by_ratings'].split(',') if result['review_by_ratings'] else ''
            review_by_created_ats = result['review_by_created_ats'].split(',') if result['review_by_created_ats'] else ''
            review_by_updated_ats = result['review_by_updated_ats'].split(',') if result['review_by_updated_ats'] else ''

            for i in range(len(review_by_ids)):
                review_creator_data = {
                'id': int(review_by_user_ids[i]),
                'first_name' : review_by_first_names[i],
                'last_name' : review_by_last_names[i],
                'address' : review_by_addresses[i],
                'email' : review_by_emails[i],
                'password': review_by_passwords[i],
                'created_at': review_by_user_created_ats[i],
                'updated_at': review_by_user_updated_ats[i]
                }
                one_product_review_by_info = {
                    'id': int(review_by_ids[i]),
                    'product_id': int(review_by_product_ids[i]),
                    'user_id': int(review_by_user_ids[i]),
                    'content': review_by_contents[i],
                    'rating': review_by_ratings[i],
                    'created_at': review_by_created_ats[i],
                    'updated_at': review_by_updated_ats[i]
                }
                this_review = review.Review(one_product_review_by_info)
                this_review.creator = user.User(review_creator_data)
                one_product.reviews.append(this_review)

            all_products.append(one_product)

        return all_products
    
    @classmethod
    def get_all_products_by_user_id(cls, user_id):
        query = """SELECT products.*, users.*,
                   GROUP_CONCAT(reviews.id SEPARATOR ',') AS review_by_ids,
                   GROUP_CONCAT(review_users.id SEPARATOR ',') AS review_by_user_ids,
                   GROUP_CONCAT(review_users.first_name SEPARATOR ',') AS review_by_first_names,
                   GROUP_CONCAT(review_users.last_name SEPARATOR ',') AS review_by_last_names,
                   GROUP_CONCAT(review_users.address SEPARATOR ',') AS review_by_addresses,
                   GROUP_CONCAT(review_users.email SEPARATOR ',') AS review_by_emails,
                   GROUP_CONCAT(review_users.password SEPARATOR ',') AS review_by_passwords,
                   GROUP_CONCAT(review_users.created_at SEPARATOR ',') AS review_by_user_created_ats,
                   GROUP_CONCAT(review_users.updated_at SEPARATOR ',') AS review_by_user_updated_ats,
                   GROUP_CONCAT(reviews.content SEPARATOR ',') AS review_by_contents,
                   GROUP_CONCAT(reviews.rating SEPARATOR ',') AS review_by_ratings,
                   GROUP_CONCAT(reviews.product_id SEPARATOR ',') AS review_by_product_ids,
                   GROUP_CONCAT(reviews.created_at SEPARATOR ',') AS review_by_created_ats,
                   GROUP_CONCAT(reviews.updated_at SEPARATOR ',') AS review_by_updated_ats
                   FROM products
                   LEFT JOIN users ON products.user_id = users.id
                   LEFT JOIN reviews ON products.id = reviews.product_id
                   LEFT JOIN users AS review_users ON reviews.user_id = review_users.id
                   WHERE products.user_id = %(id)s
                   GROUP BY products.id;"""
        results = connectToMySQL(cls.db).query_db(query, {'id': user_id})
        all_products = []
        for result in results:
            one_product = cls(result)
            one_product_creator_info = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'address': result['address'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']
            }
            one_product.creator = user.User(one_product_creator_info)

            review_by_ids = result['review_by_ids'].split(',') if result['review_by_ids'] else ''
            review_by_user_ids = result['review_by_user_ids'].split(',') if result['review_by_user_ids'] else ''
            review_by_first_names = result['review_by_first_names'].split(',') if result['review_by_first_names'] else ''
            review_by_last_names = result['review_by_last_names'].split(',') if result['review_by_last_names'] else ''
            review_by_addresses = result['review_by_addresses'].split(',') if result['review_by_addresses'] else ''
            review_by_emails = result['review_by_emails'].split(',') if result['review_by_emails'] else ''
            review_by_passwords = result['review_by_passwords'].split(',') if result['review_by_passwords'] else ''
            review_by_user_created_ats = result['review_by_user_created_ats'].split(',') if result['review_by_user_created_ats'] else ''
            review_by_user_updated_ats = result['review_by_user_updated_ats'].split(',') if result['review_by_user_updated_ats'] else ''
            review_by_product_ids = result['review_by_product_ids'].split(',') if result['review_by_product_ids'] else ''
            review_by_contents = result['review_by_contents'].split(',') if result['review_by_contents'] else ''
            review_by_ratings = result['review_by_ratings'].split(',') if result['review_by_ratings'] else ''
            review_by_created_ats = result['review_by_created_ats'].split(',') if result['review_by_created_ats'] else ''
            review_by_updated_ats = result['review_by_updated_ats'].split(',') if result['review_by_updated_ats'] else ''

            for i in range(len(review_by_ids)):
                review_creator_data = {
                'id': int(review_by_user_ids[i]),
                'first_name' : review_by_first_names[i],
                'last_name' : review_by_last_names[i],
                'address' : review_by_addresses[i],
                'email' : review_by_emails[i],
                'password': review_by_passwords[i],
                'created_at': review_by_user_created_ats[i],
                'updated_at': review_by_user_updated_ats[i]
                }
                one_product_review_by_info = {
                    'id': int(review_by_ids[i]),
                    'product_id': int(review_by_product_ids[i]),
                    'user_id': int(review_by_user_ids[i]),
                    'content': review_by_contents[i],
                    'rating': review_by_ratings[i],
                    'created_at': review_by_created_ats[i],
                    'updated_at': review_by_updated_ats[i]
                }
                this_review = review.Review(one_product_review_by_info)
                this_review.creator = user.User(review_creator_data)
                one_product.reviews.append(this_review)

            all_products.append(one_product)

        return all_products

    @classmethod
    def get_all_products_by_category(cls, category):
        query = """SELECT products.*, users.*,
                   GROUP_CONCAT(reviews.id SEPARATOR ',') AS review_by_ids,
                   GROUP_CONCAT(review_users.id SEPARATOR ',') AS review_by_user_ids,
                   GROUP_CONCAT(review_users.first_name SEPARATOR ',') AS review_by_first_names,
                   GROUP_CONCAT(review_users.last_name SEPARATOR ',') AS review_by_last_names,
                   GROUP_CONCAT(review_users.address SEPARATOR ',') AS review_by_addresses,
                   GROUP_CONCAT(review_users.email SEPARATOR ',') AS review_by_emails,
                   GROUP_CONCAT(review_users.password SEPARATOR ',') AS review_by_passwords,
                   GROUP_CONCAT(review_users.created_at SEPARATOR ',') AS review_by_user_created_ats,
                   GROUP_CONCAT(review_users.updated_at SEPARATOR ',') AS review_by_user_updated_ats,
                   GROUP_CONCAT(reviews.content SEPARATOR ',') AS review_by_contents,
                   GROUP_CONCAT(reviews.rating SEPARATOR ',') AS review_by_ratings,
                   GROUP_CONCAT(reviews.product_id SEPARATOR ',') AS review_by_product_ids,
                   GROUP_CONCAT(reviews.created_at SEPARATOR ',') AS review_by_created_ats,
                   GROUP_CONCAT(reviews.updated_at SEPARATOR ',') AS review_by_updated_ats
                   FROM products
                   LEFT JOIN users ON products.user_id = users.id
                   LEFT JOIN reviews ON products.id = reviews.product_id
                   LEFT JOIN users AS review_users ON reviews.user_id = review_users.id
                   WHERE INSTR(products.category, %(category)s) > 0
                   GROUP BY products.id;"""
        results = connectToMySQL(cls.db).query_db(query, {'category' : category})
        all_products = []
        for result in results:
            one_product = cls(result)
            one_product_creator_info = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'address': result['address'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']
            }
            one_product.creator = user.User(one_product_creator_info)

            review_by_ids = result['review_by_ids'].split(',') if result['review_by_ids'] else ''
            review_by_user_ids = result['review_by_user_ids'].split(',') if result['review_by_user_ids'] else ''
            review_by_first_names = result['review_by_first_names'].split(',') if result['review_by_first_names'] else ''
            review_by_last_names = result['review_by_last_names'].split(',') if result['review_by_last_names'] else ''
            review_by_addresses = result['review_by_addresses'].split(',') if result['review_by_addresses'] else ''
            review_by_emails = result['review_by_emails'].split(',') if result['review_by_emails'] else ''
            review_by_passwords = result['review_by_passwords'].split(',') if result['review_by_passwords'] else ''
            review_by_user_created_ats = result['review_by_user_created_ats'].split(',') if result['review_by_user_created_ats'] else ''
            review_by_user_updated_ats = result['review_by_user_updated_ats'].split(',') if result['review_by_user_updated_ats'] else ''
            review_by_product_ids = result['review_by_product_ids'].split(',') if result['review_by_product_ids'] else ''
            review_by_contents = result['review_by_contents'].split(',') if result['review_by_contents'] else ''
            review_by_ratings = result['review_by_ratings'].split(',') if result['review_by_ratings'] else ''
            review_by_created_ats = result['review_by_created_ats'].split(',') if result['review_by_created_ats'] else ''
            review_by_updated_ats = result['review_by_updated_ats'].split(',') if result['review_by_updated_ats'] else ''

            for i in range(len(review_by_ids)):
                review_creator_data = {
                'id': int(review_by_user_ids[i]),
                'first_name' : review_by_first_names[i],
                'last_name' : review_by_last_names[i],
                'address' : review_by_addresses[i],
                'email' : review_by_emails[i],
                'password': review_by_passwords[i],
                'created_at': review_by_user_created_ats[i],
                'updated_at': review_by_user_updated_ats[i]
                }
                one_product_review_by_info = {
                    'id': int(review_by_ids[i]),
                    'product_id': int(review_by_product_ids[i]),
                    'user_id': int(review_by_user_ids[i]),
                    'content': review_by_contents[i],
                    'rating': review_by_ratings[i],
                    'created_at': review_by_created_ats[i],
                    'updated_at': review_by_updated_ats[i]
                }
                this_review = review.Review(one_product_review_by_info)
                this_review.creator = user.User(review_creator_data)
                one_product.reviews.append(this_review)

            all_products.append(one_product)

        return all_products
    
    @classmethod
    def get_all_products_by_description_like(cls, search_term):
        query = """SELECT products.*, users.*,
                   GROUP_CONCAT(reviews.id SEPARATOR ',') AS review_by_ids,
                   GROUP_CONCAT(review_users.id SEPARATOR ',') AS review_by_user_ids,
                   GROUP_CONCAT(review_users.first_name SEPARATOR ',') AS review_by_first_names,
                   GROUP_CONCAT(review_users.last_name SEPARATOR ',') AS review_by_last_names,
                   GROUP_CONCAT(review_users.address SEPARATOR ',') AS review_by_addresses,
                   GROUP_CONCAT(review_users.email SEPARATOR ',') AS review_by_emails,
                   GROUP_CONCAT(review_users.password SEPARATOR ',') AS review_by_passwords,
                   GROUP_CONCAT(review_users.created_at SEPARATOR ',') AS review_by_user_created_ats,
                   GROUP_CONCAT(review_users.updated_at SEPARATOR ',') AS review_by_user_updated_ats,
                   GROUP_CONCAT(reviews.content SEPARATOR ',') AS review_by_contents,
                   GROUP_CONCAT(reviews.rating SEPARATOR ',') AS review_by_ratings,
                   GROUP_CONCAT(reviews.product_id SEPARATOR ',') AS review_by_product_ids,
                   GROUP_CONCAT(reviews.created_at SEPARATOR ',') AS review_by_created_ats,
                   GROUP_CONCAT(reviews.updated_at SEPARATOR ',') AS review_by_updated_ats
                   FROM products
                   LEFT JOIN users ON products.user_id = users.id
                   LEFT JOIN reviews ON products.id = reviews.product_id
                   LEFT JOIN users AS review_users ON reviews.user_id = review_users.id
                   WHERE INSTR(products.description, %(search_term)s) > 0
                   GROUP BY products.id;"""
        results = connectToMySQL(cls.db).query_db(query, {'search_term' : search_term})
        all_products = []
        for result in results:
            one_product = cls(result)
            one_product_creator_info = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'address': result['address'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']
            }
            one_product.creator = user.User(one_product_creator_info)

            review_by_ids = result['review_by_ids'].split(',') if result['review_by_ids'] else ''
            review_by_user_ids = result['review_by_user_ids'].split(',') if result['review_by_user_ids'] else ''
            review_by_first_names = result['review_by_first_names'].split(',') if result['review_by_first_names'] else ''
            review_by_last_names = result['review_by_last_names'].split(',') if result['review_by_last_names'] else ''
            review_by_addresses = result['review_by_addresses'].split(',') if result['review_by_addresses'] else ''
            review_by_emails = result['review_by_emails'].split(',') if result['review_by_emails'] else ''
            review_by_passwords = result['review_by_passwords'].split(',') if result['review_by_passwords'] else ''
            review_by_user_created_ats = result['review_by_user_created_ats'].split(',') if result['review_by_user_created_ats'] else ''
            review_by_user_updated_ats = result['review_by_user_updated_ats'].split(',') if result['review_by_user_updated_ats'] else ''
            review_by_product_ids = result['review_by_product_ids'].split(',') if result['review_by_product_ids'] else ''
            review_by_contents = result['review_by_contents'].split(',') if result['review_by_contents'] else ''
            review_by_ratings = result['review_by_ratings'].split(',') if result['review_by_ratings'] else ''
            review_by_created_ats = result['review_by_created_ats'].split(',') if result['review_by_created_ats'] else ''
            review_by_updated_ats = result['review_by_updated_ats'].split(',') if result['review_by_updated_ats'] else ''

            for i in range(len(review_by_ids)):
                review_creator_data = {
                'id': int(review_by_user_ids[i]),
                'first_name' : review_by_first_names[i],
                'last_name' : review_by_last_names[i],
                'address' : review_by_addresses[i],
                'email' : review_by_emails[i],
                'password': review_by_passwords[i],
                'created_at': review_by_user_created_ats[i],
                'updated_at': review_by_user_updated_ats[i]
                }
                one_product_review_by_info = {
                    'id': int(review_by_ids[i]),
                    'product_id': int(review_by_product_ids[i]),
                    'user_id': int(review_by_user_ids[i]),
                    'content': review_by_contents[i],
                    'rating': review_by_ratings[i],
                    'created_at': review_by_created_ats[i],
                    'updated_at': review_by_updated_ats[i]
                }
                this_review = review.Review(one_product_review_by_info)
                this_review.creator = user.User(review_creator_data)
                one_product.reviews.append(this_review)

            all_products.append(one_product)

        return all_products
    
    @classmethod
    def get_product_by_id(cls, id):
        query = """SELECT products.*, users.*,
                   GROUP_CONCAT(reviews.id SEPARATOR ',') AS review_by_ids,
                   GROUP_CONCAT(review_users.id SEPARATOR ',') AS review_by_user_ids,
                   GROUP_CONCAT(review_users.first_name SEPARATOR ',') AS review_by_first_names,
                   GROUP_CONCAT(review_users.last_name SEPARATOR ',') AS review_by_last_names,
                   GROUP_CONCAT(review_users.address SEPARATOR ',') AS review_by_addresses,
                   GROUP_CONCAT(review_users.email SEPARATOR ',') AS review_by_emails,
                   GROUP_CONCAT(review_users.password SEPARATOR ',') AS review_by_passwords,
                   GROUP_CONCAT(review_users.created_at SEPARATOR ',') AS review_by_user_created_ats,
                   GROUP_CONCAT(review_users.updated_at SEPARATOR ',') AS review_by_user_updated_ats,
                   GROUP_CONCAT(reviews.content SEPARATOR ',') AS review_by_contents,
                   GROUP_CONCAT(reviews.rating SEPARATOR ',') AS review_by_ratings,
                   GROUP_CONCAT(reviews.product_id SEPARATOR ',') AS review_by_product_ids,
                   GROUP_CONCAT(reviews.created_at SEPARATOR ',') AS review_by_created_ats,
                   GROUP_CONCAT(reviews.updated_at SEPARATOR ',') AS review_by_updated_ats
                   FROM products
                   LEFT JOIN users ON products.user_id = users.id
                   LEFT JOIN reviews ON products.id = reviews.product_id
                   LEFT JOIN users AS review_users ON reviews.user_id = review_users.id
                   WHERE products.id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, {'id':id})
        
        product = cls(results[0])
        one_product_creator_info = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'address': results[0]['address'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }
        product.creator = user.User(one_product_creator_info)

        review_by_ids = results[0]['review_by_ids'].split(',') if results[0]['review_by_ids'] else ''
        review_by_user_ids = results[0]['review_by_user_ids'].split(',') if results[0]['review_by_user_ids'] else ''
        review_by_first_names = results[0]['review_by_first_names'].split(',') if results[0]['review_by_first_names'] else ''
        review_by_last_names = results[0]['review_by_last_names'].split(',') if results[0]['review_by_last_names'] else ''
        review_by_addresses = results[0]['review_by_addresses'].split(',') if results[0]['review_by_addresses'] else ''
        review_by_emails = results[0]['review_by_emails'].split(',') if results[0]['review_by_emails'] else ''
        review_by_passwords = results[0]['review_by_passwords'].split(',') if results[0]['review_by_passwords'] else ''
        review_by_user_created_ats = results[0]['review_by_user_created_ats'].split(',') if results[0]['review_by_user_created_ats'] else ''
        review_by_user_updated_ats = results[0]['review_by_user_updated_ats'].split(',') if results[0]['review_by_user_updated_ats'] else ''
        review_by_contents = results[0]['review_by_contents'].split(',') if results[0]['review_by_contents'] else ''
        review_by_ratings = results[0]['review_by_ratings'].split(',') if results[0]['review_by_ratings'] else ''
        review_by_product_ids = results[0]['review_by_product_ids'].split(',') if results[0]['review_by_product_ids'] else ''
        review_by_created_ats = results[0]['review_by_created_ats'].split(',') if results[0]['review_by_created_ats'] else ''
        review_by_updated_ats = results[0]['review_by_updated_ats'].split(',') if results[0]['review_by_updated_ats'] else ''

        for i in range(len(review_by_ids)):
            review_creator_data = {
                'id': int(review_by_user_ids[i]),
                'first_name' : review_by_first_names[i],
                'last_name' : review_by_last_names[i],
                'address' : review_by_addresses[i],
                'email' : review_by_emails[i],
                'password': review_by_passwords[i],
                'created_at': review_by_user_created_ats[i],
                'updated_at': review_by_user_updated_ats[i]
            }
            one_product_review_by_info = {
                'id': int(review_by_ids[i]),
                'product_id': int(review_by_product_ids[i]),
                'user_id': int(review_by_user_ids[i]),
                'content': review_by_contents[i],
                'rating': review_by_ratings[i],
                'created_at': review_by_created_ats[i],
                'updated_at': review_by_updated_ats[i]
            }
            this_review = review.Review(one_product_review_by_info)
            this_review.creator = user.User(review_creator_data)
            product.reviews.append(this_review)
        return product 
    
    @classmethod
    def edit_product(cls, data):
        if cls.isValid_product_id(data['id']) and cls.validate_product_creation_data(data):
            data = {'user_id' : session['user_id'],
                    'name': data['name'],
                    'description': data['description'],
                    'category': data['category'],
                    'quantity': int(data['quantity']),
                    'price' : float(data['price']),
                    'img_url' : data['img_url'],
                    'id': int(data['id'])}
            
            query = """UPDATE products SET
                       name=%(name)s,
                       description=%(description)s,
                       category=%(category)s,
                       quantity=%(quantity)s,
                       price=%(price)s,
                       img_url=%(img_url)s
                       WHERE id=%(id)s;"""
            connectToMySQL(cls.db).query_db(query, data)
            return True
        return False
    
    @classmethod
    def delete_product(cls, id):
        if session['user_id'] == (Product.get_product_by_id(id)).user_id:
            query = """DELETE FROM reviews
                       WHERE product_id = %(id)s;"""
            connectToMySQL(cls.db).query_db(query,{'id':id})
            query = """DELETE FROM products
                       WHERE id = %(id)s;"""
            return connectToMySQL(cls.db).query_db(query,{'id':id})
        return False
        
    @classmethod
    def isValid_product_id(cls, id):
        data = {'id' : id}
        query = """SELECT * FROM products
                   WHERE id = %(id)s;"""
        if connectToMySQL(cls.db).query_db(query, data):
            return True
        return False
    
    # Static Methods
    @staticmethod
    def is_number(data):
        try:
            float(data)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_product_creation_data(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Name must be at least 3 characters')
            is_valid = False
        if len(data['description']) < 3:
            flash('Description must be at least 3 characters')
            is_valid = False
        if len(data['category']) < 3:
            flash('Category must be at least 3 characters')
            is_valid = False    
        if float(data['price']) < 0.01:
            flash("Price can't be less than 0.01")
            is_valid = False
        if not Product.is_number(data['price']):
            flash('Price must be numeric')
            is_valid = False
        if int(data['quantity']) < 0:
            flash("Quantity can't be less than 0")
            is_valid = False
        return is_valid
    
    
    # API Specific Methods

    @classmethod
    def add_product_api(cls, data):
        if cls.validate_product_creation_data(data):
            data = {'user_id' : data['user_id'],
                    'name': data['name'],
                    'description': data['description'],
                    'category': data['category'],
                    'quantity': data['quantity'],
                    'price' : data['price'],
                    'img_url' : data['img_url']}
            
            query = """INSERT INTO products (user_id, name, description, category, quantity, price, img_url)
                    VALUES (%(user_id)s, %(name)s, %(description)s, %(category)s, %(quantity)s, %(price)s, %(img_url)s);"""   
            user_id = connectToMySQL(cls.db).query_db(query, data)
            return cls.serialize_product(cls.get_product_by_id(user_id))
        return False
    
    @classmethod
    def edit_product_api(cls, data):
        if cls.isValid_product_id(data['id']):
            data = {'name': data['name'],
                    'description': data['description'],
                    'category': data['category'],
                    'quantity': int(data['quantity']),
                    'price' : float(data['price']),
                    'img_url' : data['img_url'],
                    'id': int(data['id'])}
            
            query = """UPDATE products SET
                       name=%(name)s,
                       description=%(description)s,
                       category=%(category)s,
                       quantity=%(quantity)s,
                       price=%(price)s,
                       img_url=%(img_url)s
                       WHERE id=%(id)s;"""
            connectToMySQL(cls.db).query_db(query, data)
            return True
        return False

    # API Specific Static Methods
    
    @staticmethod
    def validate_product_creation_data_api(data):
        is_valid = True
        errors = {}
        if len(data['name']) < 3:
            errors['name'] = []
            errors['name'].append('Name must be at least 3 characters')
            is_valid = False
        if len(data['description']) < 3:
            errors['description'] = []
            errors['description'].append('Description must be at least 3 characters')
            is_valid = False
        if len(data['category']) < 3:
            errors['category'] = []
            errors['category'].append('Category must be at least 3 characters')
            is_valid = False    
        if float(data['price']) < 0.01:
            if 'price' not in errors:
                errors['price'] = []
            errors['price'].append("Price can't be less than 0.01")
            is_valid = False
        if not Product.is_number(data['price']):
            if 'price' not in errors:
                errors['price'] = []
            errors['price'].append('Price must be numeric')
            is_valid = False
        if int(data['quantity']) < 0:
            errors['quantity'] = []
            errors['quantity'].append("Quantity can't be less than 0")
            is_valid = False
        return is_valid, errors
        
    @staticmethod
    def serialize_product(product):
        serialized_product = {
            'id': product.id,
            'user_id': product.user_id,
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'quantity': product.quantity,
            'price': product.price,
            'img_url': product.img_url,
            'created_at': product.created_at,
            'updated_at': product.updated_at,
            'creator': user.User.serialize_user(product.creator),
            'reviews': [review.Review.serialize_review(this_review) for this_review in product.reviews]
        }

        return serialized_product
    
    @staticmethod
    def serialize_products(products):
        serialized_products = []

        for product in products:
            serialized_product = Product.serialize_product(product)
            serialized_products.append(serialized_product)

        return serialized_products
    