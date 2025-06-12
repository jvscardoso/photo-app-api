import csv
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432)) 
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "photos.csv")

def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def load_photos():
    conn = connect_db()
    cur = conn.cursor()
    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                cur.execute(
                    """
                    INSERT INTO photos (
                        id, width, height, url,
                        photographer, photographer_url, photographer_id,
                        avg_color,
                        src_original, src_large2x, src_large, src_medium,
                        src_small, src_portrait, src_landscape, src_tiny,
                        alt, created_at, updated_at, deleted_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, DEFAULT, NULL, NULL)
                    """,
                    (
                        row["id"], row["width"], row["height"], row["url"],
                        row["photographer"], row["photographer_url"], row["photographer_id"],
                        row.get("avg_color"),
                        row.get("src.original"), row.get("srclarge2x"), row.get("src.large"),
                        row.get("src.medium"), row.get("src.small"), row.get("src.portrait"),
                        row.get("src.landscape"), row.get("src.tiny"),
                        row.get("alt")
                    )
                )
            except Exception as e:
                print(f"Failed to insert user id {row.get('id')}: {e}")
                conn.rollback()
            else:
                conn.commit()

    cur.close()
    conn.close()
    print("Photos migration completed!")

if __name__ == "__main__":
    load_photos()
