import random
from database.db_connection import use_database
from utils.helpers import serialize_photo
from datetime import datetime

## Get a random photo to show to an unanthenticated user
def get_random_photo():
    with use_database() as cursor:
        cursor.execute("""
            SELECT 
                p.*, 
                COUNT(pl.id) AS likes
            FROM photos p
            LEFT JOIN photo_likes pl ON pl.photo_id = p.id
            WHERE p.deleted_at IS NULL
            GROUP BY p.id
        """)
        rows = cursor.fetchall()
        if not rows:
            return None
        return serialize_photo(random.choice(rows))

## Lists all photos to an authenticated user
def list_all_photos(current_user_id, limit=10):
    with use_database() as cursor:
        cursor.execute("""
            SELECT 
                p.*, 
                COUNT(pl.id) AS likes,
                COALESCE((MAX((pl.user_id = %s)::int) = 1), false) AS liked_by_user
            FROM photos p
            LEFT JOIN photo_likes pl ON pl.photo_id = p.id
            WHERE p.deleted_at IS NULL
            GROUP BY p.id
            ORDER BY p.created_at DESC
            LIMIT %s
        """, (current_user_id, limit))
        rows = cursor.fetchall()

    return [serialize_photo(row) for row in rows]

## Create a new photo
def create_photo(photo_data, current_user):
    photo_id = random.randint(10_000_000, 99_999_999)

    with use_database() as cursor:
        cursor.execute(
            """
            INSERT INTO photos (
                id, url, src_original, src_medium, alt,
                width, height, avg_color,
                photographer, photographer_id, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """,
            (
                photo_id,
                photo_data.get("url"),
                photo_data.get("url"),
                photo_data.get("url"),
                photo_data.get("alt"),
                photo_data.get("width"),
                photo_data.get("height"),
                photo_data.get("avg_color"),
                current_user["name"],
                current_user["user_id"]
            )
        )

        cursor.execute("SELECT * FROM photos WHERE id = %s", (photo_id,))
        row = cursor.fetchone()

    return serialize_photo({**row, "likes": 0}) if row else None

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
def list_photos_by_user(photographer_id, current_user_id, limit=10):
    with use_database() as cursor:
        cursor.execute("""
            SELECT 
                p.*, 
                COUNT(pl.id) AS likes,
                CASE WHEN upl.id IS NOT NULL THEN TRUE ELSE FALSE END AS liked_by_user
            FROM photos p
            LEFT JOIN photo_likes pl ON pl.photo_id = p.id
            LEFT JOIN photo_likes upl ON upl.photo_id = p.id AND upl.user_id = %s
            WHERE p.photographer_id = %s AND p.deleted_at IS NULL
            GROUP BY p.id, liked_by_user
            ORDER BY p.created_at DESC
            LIMIT %s
        """, (current_user_id, photographer_id, limit))
        rows = cursor.fetchall()

    return [serialize_photo(row) for row in rows]
