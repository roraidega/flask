from flask import Blueprint, jsonify, request

from models import User, Products, Category, UserToProduct, db

api_bp = Blueprint("api", __name__, template_folder="templates", static_folder="static")


@api_bp.route('/products', methods=['GET'])
def products():
    products_data = []

    product_results = db.session.query(Products.name, Category.name, Products.price).join(Category).all()

    for result in product_results:
        product_dict = {
            'product_name': result[0],
            'category_name': result[1],
            'price': result[2]
        }
        products_data.append(product_dict)

    print(products_data)
    return jsonify(products_data)


@api_bp.route('/product', methods=['GET'])
def products_q():
    name = request.args.get('name')
    products_data = []

    product_results = db.session.query(Products.name, Category.name, Products.price).join(Category).filter(
        Products.name == name).all()

    for result in product_results:
        product_dict = {
            'product_name': result[0],
            'category_name': result[1],
            'price': result[2]
        }
        products_data.append(product_dict)

    print(products_data)
    return jsonify(products_data)


@api_bp.route('/users')
def get():
    # Query users with the role 'seller'
    sellers = User.query.filter_by(roll='seller').all()

    sellers_data = []

    for seller in sellers:
        seller_data = {
            'user_id': seller.id,
            'email': seller.email,
            'products': []
        }

        # Query products associated with the seller
        seller_products = db.session.query(Products.name, Products.price).filter_by(user_id=seller.id).all()

        for product in seller_products:
            product_data = {
                'product_name': product.name,
                'price': product.price
            }
            seller_data['products'].append(product_data)

        sellers_data.append(seller_data)

    return jsonify(sellers_data)
