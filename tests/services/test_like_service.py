from services.like_service import toggle_like
from unittest.mock import patch

def test_toggle_like_add_like():
    photo_id = 123
    user_id = 456

    with patch("services.like_service.use_database") as mock_db:
        mock_cursor = mock_db().__enter__().cursor
        mock_cursor.fetchone.return_value = None 

        result = toggle_like(photo_id, user_id)

        mock_cursor.execute.assert_any_call(
            "INSERT INTO photo_likes (user_id, photo_id) VALUES (%s, %s)",
            (user_id, photo_id)
        )
        assert result == {"liked": True}

def test_toggle_like_remove_like():
    photo_id = 123
    user_id = 456

    with patch("services.like_service.use_database") as mock_db:
        mock_cursor = mock_db().__enter__().cursor
        mock_cursor.fetchone.return_value = {"id": 999} 

        result = toggle_like(photo_id, user_id)

        mock_cursor.execute.assert_any_call(
            "DELETE FROM photo_likes WHERE id = %s",
            (999,)
        )
        assert result == {"liked": False}

import psycopg2

def test_toggle_like_integrity_error():
    photo_id = 123
    user_id = 456

    with patch("services.like_service.use_database") as mock_db:
        mock_cursor = mock_db().__enter__().cursor
        mock_cursor.fetchone.return_value = None
        mock_cursor.execute.side_effect = psycopg2.IntegrityError("duplicate key")

        try:
            toggle_like(photo_id, user_id)
        except psycopg2.IntegrityError as e:
            assert "duplicate key" in str(e)
