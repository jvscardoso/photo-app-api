import bcrypt
from database.db_connection import use_database
from utils.helpers import email_exists, generate_user_id
from utils.jwt import generate_token

# LOGIN
def login_user(email, password):
    with use_database() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s AND deleted_at IS NULL", (email,))
        user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        token = generate_token(user["id"], user["role"], user["name"])
        return token, user["name"], user["role"]

    return None

# REGISTER 
def register_user(name, email, password):
    if not all([name, email, password]):
        return False, "Name, email, and password are required"

    if email_exists(email):
        return False, "Email already registered"

    user_id = generate_user_id()

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
            (user_id, name, email, hashed_pw, "user")
        )

    return True, "User registered successfully"