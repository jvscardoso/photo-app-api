import random
from database.db_connection import use_database
from utils.helpers import serialize_photo
from datetime import datetime

## Get a random photo to show to an unanthenticated user
def get_random_photo():
    with use_database() as cursor:
        cursor.execute("SELECT * FROM photos WHERE deleted_at IS NULL")
        rows = cursor.fetchall()
        if not rows:
            return None
        return serialize_photo(random.choice(rows))

## Lists all photos to an authenticated user
def list_all_photos(limit=10):
    with use_database() as cursor:
        cursor.execute("""
            SELECT * FROM photos
            LIMIT %s
        """, (limit,))
        rows = cursor.fetchall()
        
    return [serialize_photo(row) for row in rows]

## Create a new photo
def create_photo(photo_data, current_user):
    photo_id = random.randint(10_000_000, 99_999_999)

    with use_database() as cursor:
        cursor.execute(
            """
            INSERT INTO photos (
                id, url, alt, photographer, photographer_id, created_at
            ) VALUES (%s, %s, %s, %s, %s, NOW())
            """,
            (
                photo_id,
                photo_data.get("url"),
                photo_data.get("alt"),
                current_user["name"],
                current_user["user_id"]
            )
        )

        cursor.execute("SELECT * FROM photos WHERE id = %s", (photo_id,))
        row = cursor.fetchone()

    return serialize_photo(row) if row else None

## Delete a photo  
def delete_photo(photo_id, current_user_id):
    with use_database() as cursor:
        ## Prevents that a user deletes a photo that he does not own
        cursor.execute("""
            SELECT * FROM photos
            WHERE id = %s AND photographer_id = %s AND deleted_at IS NULL
        """, (photo_id, current_user_id))
        photo = cursor.fetchone()

        if not photo:
            return False 

        cursor.execute("""
            UPDATE photos
            SET deleted_at = %s
            WHERE id = %s
        """, (datetime.utcnow(), photo_id))
        
    return True

## Filtered list
def list_photos_by_user(user_id, limit=10):
    with use_database() as cursor:
        cursor.execute("""
            SELECT * FROM photos 
            WHERE photographer_id = %s AND deleted_at IS NULL
            ORDER BY created_at DESC
            LIMIT %s
        """, (user_id, limit))
        rows = cursor.fetchall()

    return [serialize_photo(row) for row in rows]