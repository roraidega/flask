from flask import Flask, render_template, request, redirect, flash, jsonify, abort, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
import hashlib
import os

from werkzeug.utils import secure_filename

from api_bp.api import api_bp
from models import User, Products, Category, db, UserToProduct
from adminview import admin

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vbuvarova@gmail.com'
app.config['MAIL_PASSWORD'] = 'yijb aabj shcd fczb'
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('mail')
app.register_blueprint(api_bp, url_prefix="/api")
db.init_app(app)
admin.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/test')
@login_required
def test():
    categories = db.session.query(Category.name).all()
    return render_template('create_product.html', categories=categories)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Update the add_product route
@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    category = request.form.get('category')

    user_id = session.get('data')['id']
    category_id = db.session.query(Category.id).filter(Category.name == category).first()[0]

    # Check if the post request has the file part
    if 'image' in request.files:
        file = request.files['image']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename != '' and allowed_file(file.filename):
            # Securely save the file with a unique name
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f'static/images/{filename}'
        else:
            # Handle the case where the file is not allowed or not provided
            image_path = 'static/images/default_product.jpg'
    else:
        # Set a default image path if no file is provided
        image_path = 'static/images/default_product.jpg'

    new_product = Products(
        name=name,
        user_id=user_id,
        category_id=category_id,
        image=image_path,
        price=price
    )

    db.session.add(new_product)
    db.session.commit()

    return redirect('/catalog')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        roll = request.form.get('roll')

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if db.session.query(User.email).filter(User.email == email).first():
            flash(f'Пользователь с почтой {email} уже зарегистрирован', 'error')
            return redirect('/register')

        new_user = User(email=email, password=password_hash, roll=roll)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация успешно завершена. Теперь вы можете войти.', 'success')
        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and hashlib.sha256(password.encode()).hexdigest() == user.password:
            login_user(user)
            session['data'] = {'id': db.session.query(User.id).filter(User.email == email).first()[0],
                               'roll': db.session.query(User.roll).filter(User.email == email).first()[0]}
            return redirect('/')

        flash('Ошибка входа. Пожалуйста, проверьте введенные данные.', 'error')
        return redirect('/login')

    return render_template('login.html')


@app.route('/profile')
@login_required
def profile():
    user = {'email': current_user.email}
    products = db.session.query(Products.id, Products.name, Products.price, UserToProduct.size).join(
        UserToProduct).filter(
        UserToProduct.user_id == session.get('data')['id']).all()
    print(1)
    print(products)
    print(1)
    return render_template('profile.html', user=user, products=products)


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    try:
        user_id = session.get('data')['id']

        # Assuming you have a model named Products with a 'status' column
        product = Products.query.filter_by(id=product_id).first()
        if product:
            product.status = 'active'
            user_to_product = UserToProduct.query.filter_by(user_id=user_id, product_id=product_id).first()
            if user_to_product:
                db.session.delete(user_to_product)
                db.session.commit()
                return redirect('/cart')
            else:
                return "Product not found in the user's cart"
        else:
            return "Product not found"

    except Exception as e:
        print(f"Error: {str(e)}")
        return "An error occurred while removing the product from the cart"


@app.route('/remove_product/<product_id>', methods=['POST'])
@login_required
def remove_product(product_id):
    user_id = session.get('data')['id']
    product = Products.query.filter_by(id=product_id, user_id=user_id).first()

    if product:
        db.session.delete(product)
        db.session.commit()
        return redirect('/cart')

    pass


@app.route('/cart')
@login_required
def cart():
    if session.get('data')['roll'] == 'user':
        products = db.session.query(Products, UserToProduct.size).join(UserToProduct).filter(
            UserToProduct.user_id == session.get('data')['id']
        ).filter(Products.status == 'add_cart').all()

        total_price = round(sum(product[0].price for product in products), 2)

        return render_template('cart.html', products=products, total_price=total_price)

    else:
        seller_products = db.session.query(Products).join(User).filter(User.id == session.get('data')['id']).all()
        print(seller_products)
        return render_template('cart.html', seller_products=seller_products)


@app.route('/logout')
def logout():
    session.pop('data', None)
    logout_user()
    return redirect('/')


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        if current_user.is_authenticated:
            email = current_user.email

        msg = Message("Вам поступило новое обращение на сайте", sender='vbuvarova@gmail.com',
                      recipients=['vbuvarova@gmail.com'])
        msg.body = f'Email: {email}\nТелефон: {phone}\nСообщение: {message}'
        mail.send(msg)
        return redirect('/')

    return render_template('contact.html')


@app.route('/catalog')
def catalog():
    category = request.args.get('category')
    if category:
        products = Products.query.filter(
            Products.category.has(name=category)
        ).all()
    else:
        products = Products.query.filter(Products.status == 'active').all()

    return render_template('catalog.html', products=products)


@app.route('/search_products')
def search_products():
    search_string = request.args.get('search', '').strip().lower()

    filtered_products = Products.query.filter(Products.name.ilike(f"%{search_string}%")).all()

    products_data = [{'name': product.name, 'image': product.image, 'price': product.price} for product in
                     filtered_products]
    return jsonify(products_data)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    try:
        size = request.form.get('size')
        user_id = session.get('data')['id']

        # Assuming you want to update the status of the product with the given product_id
        product = Products.query.filter_by(id=product_id).first()
        if product:
            product.status = "add_cart"
            db.session.add(UserToProduct(user_id=user_id, product_id=product_id, size=size))
            db.session.commit()
            flash("Товар успешно добавлен в корзину")
            return redirect('/catalog')
        else:
            flash("Товар не найден")
            return redirect('/catalog')

    except Exception as e:
        print(f"Error: {str(e)}")
        flash("Произошла ошибка при добавлении товара в корзину")
        return redirect('/catalog')


@app.route('/item/<int:product_id>', methods=['GET', 'POST'])
def show_item(product_id: int):
    if request.method == 'POST':
        item = Products.query.get_or_404(product_id)
        item.image = item.image.replace('static/', '')
        return render_template('item.html', item=item, product_id=product_id)
    else:
        abort(404, "Данную страницу можно посетить только после посещения каталога")


@app.route('/buy')
@login_required
def buy():
    try:
        user_id = session.get('data')['id']

        # Get the product IDs associated with the user
        product_ids = db.session.query(Products.id).join(UserToProduct).filter(
            UserToProduct.user_id == user_id).all()

        # Update the status of the products to "куплено" (purchased)
        for product_id in product_ids:
            product = Products.query.get(product_id[0])  # Assuming Products has a primary key
            if product:
                product.status = 'buy'

        db.session.commit()

        return redirect('/profile')

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
