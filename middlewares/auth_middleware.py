from functools import wraps
from flask import request, jsonify, g
import jwt
import os

## Verifies if user is authenticated
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Unauthenticated"}), 401

        try:
            token = auth_header.split(" ")[1]
            decoded = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=["HS256"])
            g.user = {
                "user_id": decoded.get("sub"),
                "role": decoded.get("role"),
                "name": decoded.get("name"),
            }

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return jsonify({"error": "Unauthenticated"}), 401

        return f(*args, **kwargs)
    return decorated

## Verifies if user role is admin
def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        user = getattr(g, 'user', None)
        if not user or user.get("role") != "admin":
            return jsonify({"error": "User does not have the right role"}), 403

        return f(*args, **kwargs)
    return decorated

## Get current user info
def with_current_user(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        current_user = g.get("user")
        if not current_user:
            return jsonify({"error": "Current user not found"}), 401
        return f(current_user, *args, **kwargs)
    return wrapper
