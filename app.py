from flask import Flask, request, jsonify, Response
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS
from datetime import datetime
# from customer import Customer, CustomerSchema



# Init app
app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.app_context().push()
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
with app.app_context():
    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    # Init ma
    ma = Marshmallow(app)



### the fakestore api mimics the external supplier ###

external_api_url = 'https://fakestoreapi.com/products'

response_ext_api = requests.get(
    external_api_url)
print(response_ext_api.status_code)

# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
    data = response_ext_api.text
    all_products = json.loads(data)
    return jsonify(all_products)

# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    single_product = requests.get(
        f'{external_api_url}/{id}')
    data = single_product.text
    single_product = json.loads(data)
    return jsonify(single_product)


# Models
# Move models to separate files

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    created_at = db.Column(db.String(100))
    modified_at = db.Column(db.String(100))
    num_orders = db.Column(db.Integer)

    def __init__(self, username, password, email, first_name, last_name, address, phone, created_at, modified_at, num_orders):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.created_at = created_at
        self.modified_at = modified_at
        self.num_orders = num_orders

# Customer Schema
class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name',
                  'address', 'phone', 'created_at', 'modified_at', 'num_orders')

# Init schema
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


# Create a Customer
@app.route('/addcustomer', methods=['POST'])
def add_customer():
    username = request.json['username']
    password = request.json['password']  # add salt and hashing
    email = request.json['email']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    address = request.json['address']
    phone = request.json['phone']
    created_at = datetime.now().strftime("%H:%M:%S")
    modified_at = datetime.now().strftime("%H:%M:%S")
    num_orders = 0

    new_customer = Customer(username, password, email, first_name,
                            last_name, address, phone, created_at, modified_at, num_orders)

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer)

# Get All Customers
@app.route('/customer', methods=['GET'])
def get_customers():
  all_customers = Customer.query.all()
  result = customers_schema.dump(all_customers)
  return jsonify(result)

# Get Single Customer
@app.route('/customer/<id>', methods=['GET'])
def get_customer(id):
  product = Customer.query.get(id)
  return customer_schema.jsonify(product)

# Order items class
# Order details class
# Payment details class
# Revenue/sales class


# Run Server
if __name__ == '__main__':
    app.run(debug=True)