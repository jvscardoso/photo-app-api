import pytest
from unittest.mock import patch, MagicMock
from services import photo_service

@patch("app.services.photo_service.use_database")
def test_create_photo_success(mock_db):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
        "id": 12345678, "url": "http://example.com/photo.jpg", "alt": "Example photo", 
        "photographer": "John", "photographer_id": 1, "created_at": "2024-01-01"
    }
    mock_db.return_value.__enter__.return_value = mock_cursor

    current_user = {"name": "John", "user_id": 1}
    data = {"url": "http://example.com/photo.jpg", "alt": "Example photo"}
    
    result = photo_service.create_photo(data, current_user)
    
    assert result["url"] == data["url"]
    assert result["photographer"] == "John"
    assert result["likes"] == 0

@patch("app.services.photo_service.use_database")
def test_list_all_photos_returns_serialized_list(mock_db):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {"id": 1, "url": "url1", "alt": "alt1", "likes": 3, "liked_by_user": True},
        {"id": 2, "url": "url2", "alt": "alt2", "likes": 1, "liked_by_user": False},
    ]
    mock_db.return_value.__enter__.return_value = mock_cursor

    result = photo_service.list_all_photos(current_user_id=1)
    
    assert isinstance(result, list)
    assert result[0]["liked_by_user"] is True
    assert result[1]["liked_by_user"] is False

@patch("app.services.photo_service.use_database")
def test_list_photos_by_user_filters_and_serializes(mock_db):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {"id": 1, "url": "url1", "alt": "alt1", "likes": 2, "liked_by_user": True},
    ]
    mock_db.return_value.__enter__.return_value = mock_cursor

    result = photo_service.list_photos_by_user(photographer_id=1, current_user_id=2)
    
    assert len(result) == 1
    assert result[0]["liked_by_user"] is True

@patch("app.services.photo_service.use_database")
def test_delete_photo_success(mock_db):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
        "id": 1, "photographer_id": 1, "deleted_at": None
    }
    mock_db.return_value.__enter__.return_value = mock_cursor

    result = photo_service.delete_photo(photo_id=1, current_user_id=1)
    
    assert result is True

@patch("app.services.photo_service.use_database")
def test_delete_photo_denied_for_non_owner(mock_db):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_db.return_value.__enter__.return_value = mock_cursor

    result = photo_service.delete_photo(photo_id=1, current_user_id=2)
    
    assert result is False
