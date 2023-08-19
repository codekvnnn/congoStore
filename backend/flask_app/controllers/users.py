from flask import Flask, render_template, request, redirect, session

from flask_app.models.user import User
from flask_app import app


@app.route('/')
def login_register():
    return render_template('login.html')

@app.route('/users/register', methods=['POST'])
def register_submit():
    if User.create_user(request.form):
        return redirect('/products')
    return redirect('/')

@app.route('/users/profile')
def profile():
    if 'user_id' in session:
        return render_template('profile.html')
    return redirect('/')

@app.route('/users/login', methods=['POST'])
def login_user():
    if User.login_user(request.form):
        return redirect('/products')
    return redirect('/')

@app.route('/users/edit')
def update_user_info():
    if 'user_id' in session:
        return render_template('edit_user.html', user=User.get_user_by_id(session['user_id']))
    return redirect('/')

@app.route('/users/edit', methods=['POST'])
def update_user_info_submit():
    if User.update_user(request.form):    
        return redirect('/user/profile')
    return redirect('/user/edit')

@app.route('/users/logout')
def logout_user():
    session.clear()
    return redirect('/')