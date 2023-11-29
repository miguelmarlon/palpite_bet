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

    def search_team_by_name(cursor, team_name):
        team_query = "SELECT * FROM team WHERE name LIKE %s"
        cursor.execute(team_query, (f'%{team_name}%',))
        return cursor.fetchall()
    
    def search_and_select_team_id_by_name(cursor, team_name):
        query_select_team_id = f'SELECT team_id FROM team WHERE name = "{team_name}"'          
        cursor.execute(query_select_team_id)            
        return cursor.fetchone()
    
    def create_team_table(cursor, team_name, country, league):
        connection = DatabaseConnection.connect()
        cursor = connection.cursor(buffered=True)
        
        query_country_id = f"SELECT country_id FROM country WHERE name = '{country}' "           
        cursor.execute(query_country_id)            
        country_id = cursor.fetchone()[0]
        
        query_league_id = f"SELECT league_id FROM league WHERE country_id = {country_id} AND name = '{league}'"           
        cursor.execute(query_league_id)            
        league_id = cursor.fetchone()[0]
                    
        query = 'INSERT INTO team (name, league_id) VALUES (%s, %s)'
        values = (team_name, league_id)
        try:
            cursor.execute(query, values)
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            connection.rollback()
        
        connection.commit()
        
        