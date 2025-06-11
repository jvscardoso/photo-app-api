import os
import bcrypt
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432)) 
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

users = [
    {
        "name": "Jimmy Admin",
        "email": "admin@clever.io",
        "password": "admin123",
        "role": "admin",
        "id": 5600235773
    },
    {
        "name": "Nick nick",
        "email": "nick@clever.io",
        "password": "nick123",
        "role": "user",
        "id": 5525093725
    },
    {
        "name": "Lukas  Faust",
        "email": "lukas@clever.io",
        "password": "user123",
        "role": "user",
        "id": 54872664
    }
]

sql_with_id = text("""
    INSERT INTO users (id, name, email, password_hash, role)
    VALUES (:id, :name, :email, :password_hash, :role)
    ON CONFLICT (email) DO NOTHING
""")

sql_without_id = text("""
    INSERT INTO users (name, email, password_hash, role)
    VALUES (:name, :email, :password_hash, :role)
    ON CONFLICT (email) DO NOTHING
""")

with engine.connect() as conn:
    for user in users:
        password_hash = bcrypt.hashpw(user["password"].encode("utf-8"), bcrypt.gensalt()).decode()
        if "id" in user:
            conn.execute(sql_with_id, {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "password_hash": password_hash,
                "role": user["role"]
            })
        else:
            conn.execute(sql_without_id, {
                "name": user["name"],
                "email": user["email"],
                "password_hash": password_hash,
                "role": user["role"]
            })
    conn.commit()

print("Users migration completed")