import mysql.connector
from dotenv import load_dotenv
import os

class DatabaseConnection:
    @staticmethod
    def connect():
        
        load_dotenv()
        connection = mysql.connector.connect(
            host=os.getenv('host'),
            user=os.getenv('user'),
            password=os.getenv('password'),
            database=os.getenv('database'),
        )
        return connection