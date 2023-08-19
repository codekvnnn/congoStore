from flask import Flask, render_template, request, redirect, session, jsonify, Response, flash, json
from flask_app.models.review import Review
from flask_app import app
from flask_cors import CORS

CORS(app, supports_credentials=True, resources={r"/api/reviews/*": {"origins": "http://localhost:5173"}})

@app.route('/api/reviews/<int:product_id>/create', methods=['POST'])
def create_review_submit_api(product_id):
    data = request.get_json()
    isValid, errors = Review.validate_review_creation_data_api(data, product_id) 
    if isValid:
        Review.add_review_api(data, product_id)
        return jsonify(message="Review added successfully")
    return jsonify(message="Invalid data", errors=errors)