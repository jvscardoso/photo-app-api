import bcrypt
from database.db_connection import use_database
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
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    with use_database() as cursor:
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return False, "Email already registered"

        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, hashed_pw, "user")
        )
    return True, "User registered successfully"
