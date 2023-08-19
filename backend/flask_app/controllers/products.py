from flask import Flask, render_template, request, redirect, session

from flask_app.models.user import User
from flask_app.models.product import Product
from flask_app import app

@app.route('/products')
def all_products():
    if 'user_id' in session:
        all_products = Product.get_all_products()
        return render_template("dashboard.html", all_products=all_products)
    return redirect('/')

@app.route('/products/create')
def create_product():
    if 'user_id' in session:
        return render_template("product_create.html")
    return redirect('/')

@app.route('/products/create', methods=['POST'])
def create_product_submit():
    if not Product.add_product(request.form):
        return redirect('/products/create')
    return redirect('/products')

@app.route('/products/view/<int:id>')
def view_product(id):
    if 'user_id' in session:
        product = Product.get_product_by_id(id)
        return render_template('product_view.html', product=product)
    return redirect('/')

@app.route('/products/<string:search>')
def view_search_results(search):
    if 'user_id' in session:
        product_category_search_results = Product.get_all_products_by_category(search)
        product_description_search_results = Product.get_all_products_by_description_like(search)
        search_term=search
        return render_template('product_search.html', search_term=search_term, product_category_search_results=product_category_search_results, product_description_search_results=product_description_search_results)
    return redirect('/')

@app.route('/products/delete/<int:id>')
def delete_product(id):
    if 'user_id' in session:
        product=Product.get_product_by_id(id)
        if session['user_id'] == product.creator.id:
            product.delete_product(id)
        return redirect('/products')
    return redirect('/')

@app.route('/products/edit/<int:id>')
def edit_product(id):
    if 'user_id' in session:
        product=Product.get_product_by_id(id)
        if session['user_id'] == product.creator.id:
            return render_template('product_edit.html', product=product)
        return redirect('/products')
    return redirect('/')

@app.route('/products/edit', methods=['PUT'])
def edit_product_submit():
    print(request.form)
    if Product.edit_product(request.form):
        return redirect('/products')
    return redirect(f'/product/edit/{request.form["id"]}')