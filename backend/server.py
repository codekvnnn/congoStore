from flask_app.controllers import users, products, reviews, carts, api_products, api_users, api_reviews, api_carts

from flask import render_template
from flask_app import app
from datetime import datetime


@app.errorhandler(404)
@app.errorhandler(405)
def handle_page_request_error(e):
    return render_template("error.html")


def datetime_format(value, format='%B %d, %Y'):
    return value.strftime(format)

app.jinja_env.filters['datetimeformat'] = datetime_format


if __name__=='__main__':
    app.run(debug=True)