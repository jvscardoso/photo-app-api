from flask import Blueprint, request, jsonify
from middlewares.auth_middleware import token_required, admin_required
from services.user_service import (
    create_user,
    update_user,
    delete_user,
    list_users,
    list_all_users,
    restore_user
)

user_bp = Blueprint("users", __name__)

## CREATE USER
@user_bp.route('/admin/create_user', methods=['POST'])
@token_required
@admin_required
def create_user_route():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    success, message = create_user(name, email, password, role)

    if not success:
        return jsonify({"error": message}), 400

    return jsonify({"message": message}), 201

## UPDATE USER
@user_bp.route('/admin/<int:user_id>', methods=['PUT'])
@token_required
@admin_required
def update_user_route(user_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    role = data.get('role')

    if not any([name, email, role]):
        return jsonify({"error": "At least one field (name, email, role) must be provided"}), 400

    success, message = update_user(user_id, name, email, role)
    if not success:
        return jsonify({"error": message}), 400

    return jsonify({"message": message}), 200

## DELETE USER
@user_bp.route('/admin/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user_route(user_id):
    success, message = delete_user(user_id)
    if not success:
        return jsonify({"error": message}), 400

    return jsonify({"message": message}), 200

## LIST USERS
@user_bp.route('/', methods=['GET'])
@token_required
@admin_required
def list_users_route():
    users = list_users()
    return jsonify(users), 200

## LIST ALL USERS
@user_bp.route('/all', methods=['GET'])
@token_required
@admin_required
def list_all_users_route():
    users = list_all_users()
    return jsonify(users), 200

## RESTORE USER
@user_bp.route('/admin/<int:user_id>/restore', methods=['PATCH'])
@token_required
@admin_required
def restore_user_route(user_id):
    success, message = restore_user(user_id)
    if not success:
        return jsonify({"error": message}), 400

    return jsonify({"message": message}), 200
