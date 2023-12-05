import mysql.connector
from pandas import pandas as pd
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
        cursor.execute(team_query, (team_name,))
        result = cursor.fetchall()
        return result
    
    def search_and_select_team_id_by_name(cursor, team_name):
        print(f"Searching for team ID for team name: {team_name}")
        query_select_team_id = f'SELECT team_id FROM team WHERE name = %s'          
        cursor.execute(query_select_team_id, (team_name,))
        result = cursor.fetchone()
        print(f"Result: {result}")            
        return result
    
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
    
    def query_goals(cursor, table, team_name, type):
        query_team_name = 'SELECT team_id, name FROM team WHERE name LIKE %s'
        cursor.execute(query_team_name, (team_name,))
        result_team_name = cursor.fetchall() 
            
        query_type_goal = 'SELECT type_goal_id, type FROM type_goals WHERE type LIKE %s'
        cursor.execute(query_type_goal, (type,))
        result_type_goal = cursor.fetchall()
        
        query = f'SELECT total, home, away FROM {table} WHERE team_id = %s AND type_id = %s'
        cursor.execute(query, (result_team_name[0][0], result_type_goal[0][0]))
        result_goals = cursor.fetchall() 
        
        columns = ['team_id', 'name', 'type_goal_id', 'type_goal', 'total', 'home', 'away']
        data = []

        for team_row, type_goal_row, goals_row in zip(result_team_name, result_type_goal, result_goals):
            row = team_row + type_goal_row + goals_row
            data.append(row)

        df_team_name = pd.DataFrame(data, columns=columns)
        return df_team_name
    
    def query_corners(cursor, team_name, type):
        query_team_name = 'SELECT team_id, name FROM team WHERE name LIKE %s'
        cursor.execute(query_team_name, (team_name,))
        result_team_name = cursor.fetchall() 
            
        query_corners = 'SELECT type_corners_id, type FROM type_corners WHERE type LIKE %s'
        cursor.execute(query_corners, (type,))
        result_type_corners = cursor.fetchall()
        
        query = f'SELECT total, home, away FROM corners WHERE team_id = %s AND type_id = %s'
        cursor.execute(query, (result_team_name[0][0], result_type_corners[0][0]))
        result_corners = cursor.fetchall() 
        
        columns = ['team_id', 'name', 'type_corners_id', 'type_corners', 'total', 'home', 'away']
        data = []

        for team_row, type_corners_row, corners_row in zip(result_team_name, result_type_corners, result_corners):
            row = team_row + type_corners_row + corners_row
            data.append(row)

        df_team_name = pd.DataFrame(data, columns=columns)
        return df_team_name
        