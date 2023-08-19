from flask import Flask, render_template, request, redirect, session

from flask_app.models.user import User
from flask_app.models.product import Product
from flask_app.models.review import Review
from flask_app import app

@app.route('/reviews/<int:product_id>/create', methods=['POST'])
def create_review_submit(product_id):
    if 'user_id' in session:
        Review.add_review(request.form, product_id)
        return redirect('/products/view/{product_id}')
    return redirect('/')