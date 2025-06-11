import bcrypt
from database.db_connection import use_database
from utils.helpers import email_exists, generate_user_id, serialize_user

## CREATE USER
def create_user(name, email, password, role):
    if not all([name, email, password, role]):
        return False, "All fields are required"

    if email_exists(email):
        return False, "Email already registered"

    with use_database() as cursor:
        cursor.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
        while cursor.fetchone():
            user_id = generate_user_id()

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        cursor.execute(
            """
            INSERT INTO users (id, name, email, password_hash, role)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, name, email, hashed_pw, role)
        )

    return True, "User created successfully"

## UPDATE USER
def update_user(user_id, name=None, email=None, role=None):
    updates = []
    params = []

    if name:
        updates.append("name = %s")
        params.append(name)
    if email:
        updates.append("email = %s")
        params.append(email)
    if role:
        updates.append("role = %s")
        params.append(role)

    if not updates:
        return False, "No fields to update"

    updates.append("updated_at = NOW()")
    params.append(user_id)

    query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s AND deleted_at IS NULL"

    with use_database() as cursor:
        cursor.execute(query, tuple(params))

    return True, "User updated successfully"

## DELETE USER
def delete_user(user_id):
    with use_database() as cursor:
        cursor.execute(
            """
            UPDATE users
            SET deleted_at = NOW(), updated_at = NOW()
            WHERE id = %s AND deleted_at IS NULL
            """,
            (user_id,)
        )
        if cursor.rowcount == 0:
            return False, "User not found or already deleted"

    return True, "User deleted successfully"

## RESTORE USER
def restore_user(user_id):
    with use_database() as cursor:
        cursor.execute(
            """
            UPDATE users
            SET deleted_at = NULL, updated_at = NOW()
            WHERE id = %s AND deleted_at IS NOT NULL
            """,
            (user_id,)
        )
        if cursor.rowcount == 0:
            return False, "User not found or already active"

    return True, "User restored successfully"

## USER DETAILS
def get_user(user_id):
    with use_database() as cursor:
        cursor.execute(
            "SELECT id, name, email, role FROM users WHERE id = %s AND deleted_at IS NULL",
            (user_id,)
        )
        return cursor.fetchone()

## LIST USERS
def list_users():
    with use_database() as cursor:
        cursor.execute(
            "SELECT id, name, email, role, created_at, updated_at, deleted_at FROM users WHERE deleted_at IS NULL"
        )
        rows = cursor.fetchall()
    return [serialize_user(row) for row in rows]

## LIST ALL USER
def list_all_users():
    with use_database() as cursor:
        cursor.execute(
            "SELECT id, name, email, role, created_at, updated_at, deleted_at FROM users"
        )
        rows = cursor.fetchall()
    return [serialize_user(row) for row in rows]