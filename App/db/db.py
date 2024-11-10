import sqlite3
import os
import json
from typing import Any, Literal


class DatabaseError(Exception): ...


class Database:
    """
    Database client for a SQL database
    Currently uses sqlite3
    """

    def __init__(self, db_name: str):
        self.db_name = db_name

        if not os.path.exists(self.db_name):
            raise DatabaseError(
                "Database does not exist, please initialize the database as per instructions in the README"
            )

    def _connect(self) -> sqlite3.Connection:
        """Establish and return a new connection to the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to connect to database: {e}")

    def execute_query(self, query: str, params: tuple[Any, ...] | None = None) -> None:
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"SQLite error: {e}")
        finally:
            cursor.close()
            conn.close()

    def fetch_query(
        self, query: str, params: tuple[Any, ...] | None = None
    ) -> list[sqlite3.Row]:
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            raise DatabaseError(f"SQLite error: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_all_users(self):
        return self.fetch_query("SELECT * FROM Users")

    def get_user(self, user_id):
        query = "SELECT * FROM Users WHERE id = ?"
        params = (user_id,)
        return self.fetch_query(query, params)

    def insert_user(
        self, name: str, description: str, gestures: list[Literal["left", "right", "up", "down"]], image: bytes, embedding: list[float], 
    ):
        embedding_str = ",".join([str(x) for x in embedding])
        gestures_str = json.dumps(gestures)
        
        query = "INSERT INTO Users (name, description, gestures, face_image, embedding) VALUES (?, ?, ?, ?, ?)"
        params = (name, description,gestures_str, image, embedding_str)
        self.execute_query(query, params)

    def delete_user(self, user_id: int):
        query = "DELETE FROM Users WHERE id = ?"
        params = (user_id,)
        self.execute_query(query, params)

    def get_user_image(self, user_id: int):
        query = "SELECT face_image FROM Users WHERE id = ?"
        params = (user_id,)
        result = self.fetch_query(query, params)

        # Since `id` is unique, get the first (and only) row from the result
        return result[0][0] if result else None

    def get_attempts(self, start_date=None, end_date=None):
        if (start_date and not end_date) or (end_date and not start_date):
            raise DatabaseError(
                "get_attempts: Must supply either no date range or both start date and end date"
            )

        query = """
            SELECT Attempts.id, 
                   Attempts.timestamp,
                   Attempts.status,
                   Attempts.details,
                   Users.name as recognized_user
            FROM Attempts LEFT JOIN Users 
            ON recognized_user = Users.id 
            WHERE 1=1
        """

        params = tuple()

        if start_date and end_date:
            query += " AND DATE(timestamp) BETWEEN ? AND ?"
            params = (start_date, end_date)

        res = [dict(row) for row in self.fetch_query(query, params)]
        return res

    # def insert_log(self, message)
