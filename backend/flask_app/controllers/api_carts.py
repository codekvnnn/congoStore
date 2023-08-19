from flask import Flask, render_template, request, redirect, session, jsonify, Response, flash, json
from flask_app.models.cart import Cart
from flask_app import app
from flask_cors import CORS

CORS(app, resources={r"/api/carts/*": {"origins": "http://localhost:5173"}})