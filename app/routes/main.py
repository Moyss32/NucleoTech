from flask import Blueprint, render_template, send_from_directory
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/produtos')
def products():
    return render_template('products.html')

@main.route('/produto/<int:product_id>')
def product_detail(product_id):
    return render_template('product_detail.html', product_id=product_id)

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/cadastro')
def register():
    return render_template('register.html')

@main.route('/perfil')
def profile():
    return render_template('profile.html')

@main.route('/admin')
def admin():
    return render_template('admin.html')
