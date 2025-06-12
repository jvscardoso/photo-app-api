import pytest
import bcrypt
from services.user_service import create_user, get_user, delete_user
from utils.helpers import email_exists
from database.db_connection import use_database

import uuid
test_email = f"test_{uuid.uuid4()}@example.com"

@pytest.fixture
def created_user():
    success, message = create_user("Test User", test_email, "password123", "user")
    assert success, f"Erro ao criar usuário: {message}"

    with use_database() as cursor:
        cursor.execute("SELECT id FROM users WHERE email = %s", (test_email,))
        user = cursor.fetchone()
        return user["id"]

def test_create_user():
    email = f"test_create_{uuid.uuid4()}@example.com"
    success, message = create_user("Test Create", email, "123456", "user")
    assert success is True
    assert message == "User created successfully"

def test_create_user_with_existing_email(created_user):
    success, message = create_user("Test Duplicate", test_email, "123456", "user")
    assert success is False
    assert message == "Email already registered"

def test_get_user(created_user):
    user = get_user(created_user)
    assert user is not None
    assert user["email"] == test_email
    assert user["name"] == "Test User"

def test_delete_user(created_user):
    success, message = delete_user(created_user)
    assert success is True
    assert message == "User deleted successfully"

    user = get_user(created_user)
    assert user is None
