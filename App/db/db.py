import sqlite3
import os
from typing import Any

class DatabaseError(Exception):
    ...

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection: sqlite3.Connection | None = None

        if not os.path.exists(self.db_name):
            raise DatabaseError("Database does not exist, please initialize the database as per instructions in the README")

    def connect(self) -> None:
        """Establish a connection to the SQLite database."""
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(self.db_name)
                self.connection.row_factory = sqlite3.Row
                print("Connection established.")
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to connect to database: {e}")

    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            try:
                self.connection.close()
                print("Connection closed.")
            except sqlite3.Error as e:
                print(f"Failed to close the connection: {e}")
            finally:
                self.connection = None

    def execute_query(self, query: str, params: tuple[Any, ...] | None = None) -> None:
        self.connect()
        if not self.connection:
            raise DatabaseError("Cannot execute query, no database connection")

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.connection.commit()

        except sqlite3.Error as e:
            raise DatabaseError(f"SQLite error: {e}")
        finally:
            if cursor:
                cursor.close()

    def fetch_query(self, query: str, params: tuple[Any, ...]|None = None) -> list[sqlite3.Row]:
        self.connect()
        if not self.connection:
            raise DatabaseError("Cannot execute query, no database connection")

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            raise DatabaseError(f"SQLite error: {e}")
        finally:
            cursor.close()


    def get_all_users(self):
        return self.fetch_query("SELECT * FROM Users")
        
    def insert_user(self, name:str, description:str, image:bytes):
        query = "INSERT INTO Users (name, description, face_image) VALUES (?, ?, ?)"
        params = (name, description, image)
        self.execute_query(query, params)
    
    def delete_user(self, user_id:int):
        query = "DELETE FROM Users WHERE id = ?"
        params = (user_id,)
        self.execute_query(query, params)
