from flask import Blueprint, g, request, jsonify
from middlewares.auth_middleware import token_required
from services.auth_service import login_user, register_user
from services.user_service import get_user

auth_bp = Blueprint("auth", __name__)

## LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    result = login_user(email, password)

    if result == "blocked":
        return jsonify({"error": "User blocked"}), 403

    if not result:
        return jsonify({"error": "Invalid credentials"}), 401

    token, name, role = result
    return jsonify({
        "access_token": token,
        "name": name,
        "role": role
    })

## PUBLIC USER REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"error": "Name, email, and password are required"}), 400

    success, message = register_user(name, email, password)
    if not success:
        return jsonify({"error": message}), 400

    return jsonify({"message": message}), 201

## USER DETAILS
@auth_bp.route("/me", methods=["GET"])
@token_required
def me():
    user = get_user(g.user["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)
