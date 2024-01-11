from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    roll = db.Column(db.String(60), default=False)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"Category('{self.name}')"


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    image = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), default='active')

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"


class UserToProduct(db.Model):
    __tablename__ = 'user_to_product'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    size = db.Column(db.String(10), nullable=False)
