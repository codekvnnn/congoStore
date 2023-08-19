from flask import Flask, render_template, request, redirect, session

from flask_app.models.cart import Cart
from flask_app.models.user import User
from flask_app.models.product import Product
from flask_app.models.review import Review
from flask_app import app