from flask import Flask, request, session, jsonify, Response, json
from flask_app.models.product import Product
from flask_app import app
from flask_cors import CORS

CORS(app, supports_credentials=True, resources={r"/api/products/*": {"origins": "http://localhost:5173"}})

@app.route('/api/products/create', methods=['POST'])
def create_product_submit_api():
    data = request.get_json()
    isValid, errors = Product.validate_product_creation_data_api(data)
    if isValid:
        new_product = Product.add_product_api(data)
        return jsonify(message="Product created succesfully", product=new_product), 201
    return jsonify(message="Invalid data", errors=errors), 400

@app.route('/api/products')
def all_products_api():
    all_products = Product.get_all_products()
    serialized_products = Product.serialize_products(all_products)
    return serialized_products

@app.route('/api/products/view/<int:id>')
def view_product_api(id):   
    product = Product.get_product_by_id(id)
    return Product.serialize_product(product)

@app.route('/api/products/category/<string:search_term>')
def search_product_category_api(search_term):
    all_products = Product.get_all_products_by_category(search_term)
    return Product.serialize_products(all_products)

@app.route('/api/products/description/<string:search_term>')
def search_product_description_api(search_term):
    all_products = Product.get_all_products_by_description_like(search_term)
    return Product.serialize_products(all_products)

@app.route('/api/products/user/<int:user_id>')
def all_user_products(user_id):
    all_products = Product.get_all_products_by_user_id(user_id)
    return Product.serialize_products(all_products)

@app.route('/api/products/delete/<int:id>')
def delete_product_api(id):
    product=Product.get_product_by_id(id)
    # if user_id is sent via post request on delete can be added back in 
    # if data['user_id'] == product.creator.id:
    product.delete_product(id)
    return jsonify(message="Product deleted successfully")
    # return jsonify(message="Unauthorized to delete this product"), 403

@app.route('/api/products/edit/<int:id>')
def edit_product_api(id):
    product=Product.get_product_by_id(id)
    # if user_id is sent via post request on view can be added back in  
    # if data['user_id'] == product.creator.id:
    return Product.serialize_product(product)
    # return jsonify(message="Unauthorized to edit this product"), 403

@app.route('/api/products/edit', methods=['PUT'])
def edit_product_submit_api():
    data = request.get_json()
    isProduct, errors = Product.validate_product_creation_data_api(data)
    if isProduct: 
        Product.edit_product_api(data)
        return jsonify(message="Product edited successfully")
    return jsonify(message="Error", errors=errors)