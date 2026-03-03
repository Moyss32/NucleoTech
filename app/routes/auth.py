from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import db, bcrypt
from app.models.models import User

auth = Blueprint('auth', __name__)

@auth.route('/api/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({'message': 'Já está logado'}), 400
    
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed_password)
    
    # Check if user is the first one, make them admin
    if User.query.count() == 0:
        user.is_admin = True
        
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

@auth.route('/api/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'message': 'Já está logado'}), 400
    
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user, remember=data.get('remember', False))
        return jsonify({
            'message': 'Login realizado com sucesso!',
            'user': user.to_dict()
        }), 200
    else:
        return jsonify({'message': 'Email ou senha incorretos'}), 401

@auth.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso!'}), 200

@auth.route('/api/current_user')
def get_current_user():
    if current_user.is_authenticated:
        return jsonify(current_user.to_dict()), 200
    return jsonify({'message': 'Não autenticado'}), 401
