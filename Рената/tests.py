import unittest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import User


class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_products_route(self):
        response = self.app.get('/api/products')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_products_q_route(self):
        response = self.app.get('/api/product?name=ExampleProduct')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_users_route(self):
        response = self.app.get('/api/users')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_register_route(self):
        response = self.app.post('/register',
                                 data={'email': 'test@example.com', 'password': 'password', 'roll': 'user'})

        self.assertEqual(response.status_code, 302)  # Assuming successful registration redirects to '/'
        # Add more assertions based on your registration logic

    def test_login_route(self):
        response = self.app.post('/login', data={'email': 'test@example.com', 'password': 'password'})

        self.assertEqual(response.status_code, 302)  # Assuming successful login redirects to '/'
        # Add more assertions based on your login logic

    def test_test_route(self):
        response = self.app.get('/test')

        self.assertEqual(response.status_code, 302)
        # Add more assertions based on your /test route logic

    def test_add_product_route(self):
        with app.app_context():
            # Create a test user for authentication
            test_user = User(email='test@example.com', password='password', roll='seller')
            db.session.add(test_user)
            db.session.commit()

        # Log in as the test user
        login_response = self.app.post('/login', data={'email': 'test@example.com', 'password': 'password'})

        self.assertEqual(login_response.status_code, 302)  # Assuming successful login redirects to '/'

        # Now, try adding a product
        add_product_response = self.app.post('/add_product',
                                             data={'name': 'TestProduct', 'price': '10', 'category': 'TestCategory'})

        self.assertEqual(add_product_response.status_code,
                         302)  # Assuming successful product addition redirects to '/catalog'
        # Add more assertions based on your /add_product route logic

    def test_catalog_route(self):
        response = self.app.get('/catalog')

        self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        response = self.app.get('/logout')

        self.assertEqual(response.status_code, 302)  # Assuming successful logout redirects to '/'
        # Add more assertions based on your logout logic

    def test_index_route(self):
        response = self.app.get('/')

        self.assertEqual(response.status_code, 200)

    def test_about_route(self):
        response = self.app.get('/about')

        self.assertEqual(response.status_code, 200)


    def test_contact_route(self):
        response = self.app.get('/contact')

        self.assertEqual(response.status_code, 200)

    def test_nonexistent_route(self):
        response = self.app.get('/nonexistent_route')

        self.assertEqual(response.status_code, 404)

    def test_empty_cart_route(self):
        response = self.app.get('/cart')

        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
