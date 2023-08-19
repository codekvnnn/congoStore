from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import product
from flask_app.models import cart
from flask import flash, session

class Cart_Product:
    db = 'congo_schema'

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.product_id = data['product_id']
        self.quantity_to_purchase = data['quantity_to_purchase']