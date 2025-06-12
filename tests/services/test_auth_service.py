import bcrypt
import pytest
from unittest.mock import patch
from services import auth_service

def test_login_user_success():
    email = "test@example.com"
    password = "securepassword"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    mock_user = {
        "id": 1,
        "name": "Test User",
        "role": "user",
        "email": email,
        "password_hash": hashed
    }

    with patch("services.auth_service.use_database") as mock_db, \
         patch("services.auth_service.generate_token") as mock_token:
        mock_cursor = mock_db().__enter__().cursor
        mock_cursor.fetchone.return_value = mock_user
        mock_token.return_value = "mocked.jwt.token"

        token, name, role = auth_service.login_user(email, password)

        assert token == "mocked.jwt.token"
        assert name == "Test User"
        assert role == "user"

def test_login_user_wrong_password():
    email = "test@example.com"
    password = "wrongpassword"
    correct_hashed = bcrypt.hashpw("correctpassword".encode(), bcrypt.gensalt()).decode()

    mock_user = {
        "id": 1,
        "name": "Test User",
        "role": "user",
        "email": email,
        "password_hash": correct_hashed
    }

    with patch("services.auth_service.use_database") as mock_db:
        mock_cursor = mock_db().__enter__().cursor
        mock_cursor.fetchone.return_value = mock_user

        result = auth_service.login_user(email, password)
        assert result is None

