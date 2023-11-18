import pandas as pd
import telegram
import asyncio
from dotenv import load_dotenv
import os
from database_connection import DatabaseConnection
from send_telegram_message import send_message

class DataProcessor:

    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.total_goals = None
        self.home_goals = None
        self.away_goals = None
               
    def goal_statistics(self):
        connection = DatabaseConnection.connect()
        cursor = connection.cursor()

        query_home_team = "SELECT * FROM goals WHERE name LIKE %s"
        cursor.execute(query_home_team, (f'%{self.home_team}%',))
        result_home_team = cursor.fetchall()

        query_away_team = "SELECT * FROM goals WHERE name LIKE %s"
        cursor.execute(query_away_team, (f'%{self.away_team}%',))
        result_away_team = cursor.fetchall()

        print('Goal Statistics:')
        print(self.home_team)
        for item in result_home_team:
            print(item)

        print()
        print(self.away_team)
        for item in result_away_team:
            print(item)
        print()

        cursor.close()
        connection.close()
        
    def corners_statistics(self):
        connection = DatabaseConnection.connect()
        cursor = connection.cursor()

        query_home_team = "SELECT * FROM corners WHERE name LIKE %s"
        cursor.execute(query_home_team, (f'%{self.home_team}%',))
        result_home_team = cursor.fetchall()

        query_away_team = "SELECT * FROM corners WHERE name LIKE %s"
        cursor.execute(query_away_team, (f'%{self.away_team}%',))
        result_away_team = cursor.fetchall()

        print('Corners Statistics:')
        print(self.home_team)
        for item in result_home_team:
            print(item)

        print()
        print(self.away_team)
        for item in result_away_team:
            print(item)

        cursor.close()
        connection.close()
    
    def filtered_goal_statistics(self):
        connection = DatabaseConnection.connect()      
        cursor = connection.cursor()

        query_home_team = "SELECT * FROM goals WHERE name LIKE %s"
        cursor.execute(query_home_team, (f'%{self.home_team.lower()}%',))
        result_home_team = cursor.fetchall()

        query_away_team = "SELECT * FROM goals WHERE name LIKE %s"
        cursor.execute(query_away_team, (f'%{self.away_team.lower()}%',))
        result_away_team = cursor.fetchall()

        final_data = []

        for tuple_away_team, tuple_home_team in zip(result_away_team, result_home_team):
            key = tuple_away_team[1]
            total = (tuple_away_team[3] + tuple_home_team[3]) / 2
            home_vs_away = (tuple_away_team[4] + tuple_home_team[5]) / 2
            final_data.append((key, total, home_vs_away))

        df = pd.DataFrame(final_data, columns=['goals', 'total', 'home_vs_away'])
        df_filtered_goals_above = df[(df['total'] >= 75) & (df['home_vs_away'] >= 75)]
        df_filtered_goals_below = df[(df['total'] <= 25) & (df['home_vs_away'] <= 25)]

        message = ''
        message_goals_above = ''
        message_goals_below = ''
        
        if not df_filtered_goals_above.empty:
            message_goals_above = f"⚽Oportunidade para {self.home_team} vs {self.away_team} ⚽:\n\n"
            goals_above_added = set()
            for index, row in df_filtered_goals_above.iterrows():
                goals = row['goals']
                home_vs_away = row['home_vs_away']                                  
                message_goals_above += f"Gols acima de {goals}: {home_vs_away}% 🎯\n"
                goals_above_added.add(goals)
            
        if not df_filtered_goals_below.empty:
            message_goals_below = f"⚽Oportunidade para {self.home_team} vs {self.away_team} ⚽:\n\n"
            goals_below_added = set()
            for index, row in df_filtered_goals_below.iterrows():
                goals = row['goals']
                home_vs_away = 100 - row['home_vs_away']                               
                message_goals_below += f"Gols abaixo de {goals}: {home_vs_away}% 🎯\n"  
                goals_below_added.add(goals) 
            
        message += message_goals_above
        message += message_goals_below
        
        if message:
            asyncio.run(send_message(message)) 
            
        cursor.close()
        connection.close()
   
    def filtered_corners_statistics(self):
        connection = DatabaseConnection.connect()
        cursor = connection.cursor()

        query_home_team = f"SELECT * FROM corners WHERE name = '{self.home_team}'"
        cursor.execute(query_home_team)
        result_home_team = cursor.fetchall()

        query_away_team = f"SELECT * FROM corners WHERE name = '{self.away_team}'"
        cursor.execute(query_away_team)
        result_away_team = cursor.fetchall()

        final_data = []

        for tuple_away_team, tuple_home_team in zip(result_away_team, result_home_team):
            key = tuple_away_team[1]
            total = (float(tuple_away_team[3]) + float(tuple_home_team[3])) / 2
            home_vs_away = (float(tuple_away_team[4]) + float(tuple_home_team[5])) / 2
            final_data.append((key, total, home_vs_away))

        df = pd.DataFrame(final_data, columns=['corners', 'total', 'home_vs_away'])
        df_filtered_corners_above = df[(df['total'] >= 75) & (df['home_vs_away'] >= 75)]
        df_filtered_corners_below = df[(df['total'] <= 25) & (df['home_vs_away'] <= 25)]

        message = ''
        message_corners_above = ''
        message_corners_below = ''

        if not df_filtered_corners_above.empty:
            message_corners_above = f"⚽Oportunidades para {self.home_team} vs {self.away_team} ⚽:\n\n"
            for index, row in df_filtered_corners_above.iterrows():
                corners = row['corners']
                home_vs_away = row['home_vs_away']
                message_corners_above += f"Escanteios acima de {corners}: {home_vs_away}% 🎌\n"

        if not df_filtered_corners_below.empty:
            message_corners_below = f"⚽Oportunidades para {self.home_team} vs {self.away_team} ⚽:\n\n"
            for index, row in df_filtered_corners_below.iterrows():
                corners = row['corners']
                home_vs_away = 100 - row['home_vs_away']
                message_corners_below += f"Escanteios abaixo de {corners}: {home_vs_away}% 🎌\n"

        message += message_corners_above
        message += message_corners_below

        if message:
            asyncio.run(send_message(message))

        cursor.close()
        connection.close()
    
    def additional_goals_statistics(self):
                
        connection = DatabaseConnection.connect()      
        cursor = connection.cursor()

        query_scored_home_team = "SELECT * FROM test_scored WHERE name LIKE %s"
        cursor.execute(query_scored_home_team, (f'%{self.home_team.lower()}%',))
        result_scored_home_team = cursor.fetchall()

        query_scored_away_team = "SELECT * FROM test_scored WHERE name LIKE %s"
        cursor.execute(query_scored_away_team, (f'%{self.away_team.lower()}%',))
        result_scored_away_team = cursor.fetchall()
        
        query_conceded_home_team = "SELECT * FROM test_conceded WHERE name LIKE %s"
        cursor.execute(query_conceded_home_team, (f'%{self.home_team.lower()}%',))
        result_conceded_home_team = cursor.fetchall()

        query_conceded_away_team = "SELECT * FROM test_conceded WHERE name LIKE %s"
        cursor.execute(query_conceded_away_team, (f'%{self.away_team.lower()}%',))
        result_conceded_away_team = cursor.fetchall()
        
        df_scored_home_team = pd.DataFrame(result_scored_home_team, columns=['id', 'type', 'name', 'total', 'home', 'away', 'country', 'league'])
        df_scored_away_team = pd.DataFrame(result_scored_away_team, columns=['id', 'type', 'name', 'total', 'home', 'away', 'country', 'league'])
        
        df_conceded_home_team = pd.DataFrame(result_conceded_home_team, columns=['id', 'type', 'name', 'total', 'home', 'away', 'country', 'league'])
        df_conceded_away_team = pd.DataFrame(result_conceded_away_team, columns=['id', 'type', 'name', 'total', 'home', 'away', 'country', 'league'])
        
        message_home_team = f'{self.home_team} tem estatística de gols marcados como mandante:\n {df_scored_home_team['type'].to_string(index=False)}: {df_scored_home_team['home'].to_string(index=False)}%\n'
        message_home_team += f'{self.home_team} tem estatística de gols sofridos como mandante:\n {df_conceded_home_team['type'].to_string(index=False)}: {df_conceded_home_team['home'].to_string(index=False)}%\n'
        
        message_away_team = f'{self.away_team} tem estatística de gols marcados como visitante:\n {df_scored_away_team['type'].to_string(index=False)}: {df_scored_home_team['home'].to_string(index=False)}%\n'
        message_away_team += f'{self.away_team} tem estatística de gols sofridos como visitante:\n {df_conceded_away_team['type'].to_string(index=False)}: {df_conceded_home_team['away'].to_string(index=False)}%\n'
        asyncio.run(send_message(message_home_team))
        asyncio.run(send_message(message_away_team))
              
        cursor.close()
        connection.close()