from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# User model to store user credentials and authentication details
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    username = db.Column(db.String(150), unique=True, nullable=False)  # Username must be unique
    password = db.Column(db.String(150), nullable=False)  # Hashed password storage

# Product model to store product details
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each product
    name = db.Column(db.String(150), nullable=False)  # Name of the product
    description = db.Column(db.String(300))  # Optional product description
    price = db.Column(db.Float, nullable=False)  # Price of the product
    image_url = db.Column(db.String(150), nullable=False)  # URL for product image

