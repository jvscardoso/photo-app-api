from database.db_connection import use_database
import random

def serialize_user(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "role": row["role"],
        "created_at": row["created_at"].isoformat(),
        "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
        "deleted_at": row["deleted_at"].isoformat() if row["deleted_at"] else None
    }

def serialize_photo(row):
    return {
        "id": row["id"],
        "width": row["width"],
        "height": row["height"],
        "url": row["url"],
        "photographer": row["photographer"],
        "photographer_url": row["photographer_url"],
        "photographer_id": row["photographer_id"],
        "avg_color": row["avg_color"],
        "alt": row["alt"],
        "likes": row.get("likes", 0),
        "liked_by_user": row.get("liked_by_user", False),
        "src_original": row["src_original"],
        "src_medium": row["src_medium"],
        "created_at": row["created_at"].isoformat(),
    }

def email_exists(email):
    with use_database() as cursor:
        cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
        return cursor.fetchone() is not None

def generate_user_id():
    return random.randint(10**9, 10**10 - 1)  
