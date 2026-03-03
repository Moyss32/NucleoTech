from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.models import Product, Order, User

api = Blueprint('api', __name__)

# Product Routes
@api.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200

@api.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict()), 200

@api.route('/products', methods=['POST'])
@login_required
def create_product():
    if not current_user.is_admin:
        return jsonify({'message': 'Acesso negado'}), 403
    
    data = request.get_json()
    product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        category=data['category'],
        image_url=data.get('image_url'),
        benefits=data.get('benefits'),
        specifications=data.get('specifications')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@api.route('/products/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    if not current_user.is_admin:
        return jsonify({'message': 'Acesso negado'}), 403
    
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.category = data.get('category', product.category)
    product.image_url = data.get('image_url', product.image_url)
    product.benefits = data.get('benefits', product.benefits)
    product.specifications = data.get('specifications', product.specifications)
    
    db.session.commit()
    return jsonify(product.to_dict()), 200

@api.route('/products/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        return jsonify({'message': 'Acesso negado'}), 403
    
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Produto excluído'}), 200

# Order Routes
@api.route('/orders', methods=['POST'])
@login_required
def create_order():
    data = request.get_json()
    order = Order(
        user_id=current_user.id,
        product_id=data['product_id'],
        status='Paid' # Simulating checkout success
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201

@api.route('/orders', methods=['GET'])
@login_required
def get_orders():
    if current_user.is_admin:
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(user_id=current_user.id).all()
    return jsonify([o.to_dict() for o in orders]), 200

# Admin User Control
@api.route('/users', methods=['GET'])
@login_required
def get_users():
    if not current_user.is_admin:
        return jsonify({'message': 'Acesso negado'}), 403
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200
