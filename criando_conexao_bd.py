import mysql.connector
from dotenv import load_dotenv
import os

class conexao_bd:
    
    def conectando():
        load_dotenv()
        conexao = mysql.connector.connect(
        host = os.getenv('host'),
        user = os.getenv('user'),
        password = os.getenv('password'),
        database = os.getenv('database'),
        )
        return conexao
    
    