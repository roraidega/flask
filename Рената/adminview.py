from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import User, Products, Category, db

admin = Admin(name='Admin Panel', template_mode='bootstrap3')

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Products, db.session))
admin.add_view(ModelView(Category, db.session))
