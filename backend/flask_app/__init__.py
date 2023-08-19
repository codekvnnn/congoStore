from flask import Flask, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'thecongostoresecretkey'

