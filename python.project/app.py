from flask import Flask, render_template, request, redirect, url_for, session
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os
from models import db, User, Product

# Initialize the Flask application
app = Flask(__name__)

# Configure the secret key for session management
app.config['SECRET_KEY'] = 'your_secret_key'

# Configure the database URI to use SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Initialize Flask-Migrate with your app and db
migrate = Migrate(app, db)

# Add mishapen produce to the database (just for testing purposes)
def add_mishapen_produce():
    # Check if there are already products in the database
    if Product.query.count() == 0:  # Only add if no products are present
        mishapen_produce = [
            {
                'name': 'Curved Carrot',
                'description': 'A carrot with an unusual curve, making it perfect for quirky salads.',
                'price': 2.99,
                'image_url': 'static/images/curved_carrot.jpg'
            },
            {
                'name': 'Lopsided Potato',
                'description': 'This potato grew slightly lopsided, but it’s still delicious and perfect for mashing.',
                'price': 1.99,
                'image_url': 'static/images/lopsided_potato.jpg'
            },
            {
                'name': 'Misshapen Apple',
                'description': 'A perfectly good apple that grew a bit wonky – perfect for apple pies!',
                'price': 3.49,
                'image_url': 'static/images/misshapen_apple.jpg'
            },
            {
                'name': 'Giant Tomato',
                'description': 'This tomato grew larger than expected, making it perfect for salads and sandwiches.',
                'price': 4.99,
                'image_url': 'static/images/giant_tomato.jpg'
            },
            {
                'name': 'Twisted Cucumber',
                'description': 'A cucumber with a unique twist, adding fun to any salad or sandwich.',
                'price': 2.49,
                'image_url': 'static/images/twisted_cucumber.jpg'
            }
        ]

        for produce in mishapen_produce:
            # Check if the product already exists in the database
            if not Product.query.filter_by(name=produce['name']).first():
                new_product = Product(
                    name=produce['name'],
                    description=produce['description'],
                    price=produce['price'],
                    image_url=produce['image_url']
                )
                db.session.add(new_product)

        db.session.commit()  # Commit all the products to the database

# Route for the home page, displaying all products
@app.route('/')
def home():
    products = Product.query.all()  # Retrieve all products from the database
    return render_template('home.html', products=products)  # Render home page with products

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # Handle form submission
        username = request.form['username']  # Get the username from the form
        password = request.form['password']  # Get the password from the form
        hashed_password = generate_password_hash(password, method='sha256')  # Hash the password
        new_user = User(username=username, password=hashed_password)  # Create new user object
        db.session.add(new_user)  # Add new user to the database
        db.session.commit()  # Commit changes
        return redirect(url_for('login'))  # Redirect to login page after registration
    return render_template('register.html')  # Render registration page

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Handle form submission
        username = request.form['username']  # Get the username from the form
        password = request.form['password']  # Get the password from the form
        user = User.query.filter_by(username=username).first()  # Fetch user from the database
        if user and check_password_hash(user.password, password):  # Verify password
            session['user_id'] = user.id  # Store user ID in session
            return redirect(url_for('home'))  # Redirect to home page on successful login
    return render_template('login.html')  # Render login page

# Route for user logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    return redirect(url_for('home'))  # Redirect to home page

# Route for adding product to the cart
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)  # Get product by ID
    cart = session.get('cart', [])  # Get cart from session or initialize as empty list
    cart.append(product.id)  # Add product ID to cart
    session['cart'] = cart  # Update session with new cart
    return redirect(url_for('product_page', product_id=product_id))  # Redirect back to product page


# Route for displaying product details
@app.route('/product/<int:product_id>')
def product_page(product_id):
    product = Product.query.get_or_404(product_id)  # Get product by ID from the database
    return render_template('product_page.html', product=product)  # Render product details page

# Run the Flask application
if __name__ == '__main__':
    with app.app_context():  # Ensure the app context is active
        db.create_all()  # Create database tables if they do not exist
        add_mishapen_produce()  # Add sample products (only if none exist)
    app.run(debug=True)  # Run the Flask app in debug mode

