from flask import Flask, render_template, request, redirect, session, jsonify, Response, flash, json
from flask_app.models.user import User
from flask_app import app
from flask_cors import CORS

CORS(app, resources={r"/api/users/*": {"origins": "http://localhost:5173"}})

@app.route('/api/users/register', methods=['POST'])
def register_submit_api():
    data = request.get_json()
    if data:
        is_valid, errors = User.validate_user_registration_data_api(data)
        if is_valid:
            return jsonify(message="User created successfully", user=User.create_user_api(data)), 201
        else:
            return jsonify(message="User creation failed", errors=errors), 400
    return jsonify(message="Invalid data"), 400

@app.route('/api/users/login', methods=['POST'])
def login_user_api():
    data = request.get_json()
    if data:
        user = User.login_user_api(data)
        print(user)
        return user
    return jsonify(message="Invalid data"), 400

@app.route('/api/users/<int:user_id>')
def get_user_api(user_id):
    user = User.get_user_by_id(user_id)
    if user:
        return User.serialize_user(user)
    return jsonify(message="User not found"), 404

@app.route('/api/users/logout')
def logout_user_api():
    print(f"Clearing {session['user_id']} from session")
    session.clear()
    return jsonify(message="User logged out")