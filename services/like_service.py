from database.db_connection import use_database
import psycopg2

def toggle_like(photo_id, user_id):
    with use_database() as cursor:
        try:
            cursor.execute(
                "SELECT id FROM photo_likes WHERE user_id = %s AND photo_id = %s",
                (user_id, photo_id)
            )
            existing = cursor.fetchone()

            if existing:
                cursor.execute("DELETE FROM photo_likes WHERE id = %s", (existing["id"],))
                return {"liked": False}
            else:
                cursor.execute(
                    "INSERT INTO photo_likes (user_id, photo_id) VALUES (%s, %s)",
                    (user_id, photo_id)
                )
                return {"liked": True}

        except psycopg2.IntegrityError as e:
            print("Erro de integridade (provável like duplicado):", e)
            raise e

        except Exception as e:
            print("Erro inesperado no toggle_like:", e)
            raise e
