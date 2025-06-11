from functools import wraps
from flask import request, jsonify, g
import jwt
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Bearer token is required"}), 401

        try:
            token = auth_header.split(" ")[1]
            decoded = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=["HS256"])
            g.user = {
                "user_id": decoded.get("sub"),
                "role": decoded.get("role")
            }

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return jsonify({"error": "Deu erro caraio"}), 401

        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        user = getattr(g, 'user', None)
        if not user or user.get("role") != "admin":
            return jsonify({"error": "Access limited to admins"}), 403

        return f(*args, **kwargs)
    return decorated
