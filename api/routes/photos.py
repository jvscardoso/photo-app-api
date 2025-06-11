from flask import Blueprint, jsonify, request
from middlewares.auth_middleware import token_required, with_current_user
from services.photo_service import create_photo, delete_photo, get_random_photo, list_all_photos, list_photos_by_user

photo_bp = Blueprint('photo', __name__)

## LIST ALL PHOTOS
@photo_bp.route('/all-photos', methods=['GET'])
@token_required
def get_all_photos():
    photos = list_all_photos()
    return jsonify(photos), 200

## LIST ONE RANDOM PHOTO
@photo_bp.route('/daily-photo', methods=['GET'])
def get_daily_photo():
    photo = get_random_photo()
    if not photo:
        return jsonify({"error": "No photo found"}), 404
    return jsonify(photo), 200

## CREATES A PHOTO
@photo_bp.route('/new-photo', methods=['POST'])
@token_required
@with_current_user
def create_photo_route(current_user):
    data = request.json
    if not data.get("url") or not data.get("alt"):
        return jsonify({"error": "URL and ALT text are required"}), 400

    try:
        created_photo = create_photo(data, current_user)
        if not created_photo:
            return jsonify({"error": "Failed to retrieve created photo"}), 500
        return jsonify(created_photo), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

## DELETE A PHOTO
@photo_bp.route('/<int:photo_id>', methods=['DELETE'])
@token_required
@with_current_user
def delete_photo_route(current_user, photo_id):
    success = delete_photo(photo_id, current_user["user_id"])

    if not success:
        return jsonify({"error": "Photo not found or permission denied"}), 403

    return jsonify({"message": "Photo deleted successfully"}), 200

## LIST PHOTOS BY USER
@photo_bp.route('/user-photos/<int:user_id>', methods=['GET'])
@token_required
def get_user_photos_route(user_id):
    photos = list_photos_by_user(user_id)
    return jsonify(photos), 200
