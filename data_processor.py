import pandas as pd
import telegram
import asyncio
from dotenv import load_dotenv
import os
from db_functions import DatabaseConnection
from send_telegram_message import *

class DataProcessor:

    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.total_goals = None
        self.home_goals = None
        self.away_goals = None
       
    def additional_goals_statistics(self):
                
        connection = DatabaseConnection.connect()      
        cursor = connection.cursor()
        message_home_team = ''
        message_away_team = ''
        type_goal=[0.5, 1.5, 2.5]
        df_scored_home_team = pd.DataFrame()
        df_scored_away_team = pd.DataFrame()
        df_conceded_home_team = pd.DataFrame()
        df_conceded_away_team = pd.DataFrame()
        
        for goal in type_goal:
            object_db_funcitions_home_team_scored = DatabaseConnection.query_goals_scored(cursor, self.home_team, goal)
            df_scored_home_team = pd.concat([df_scored_home_team, object_db_funcitions_home_team_scored])
            
            object_db_funcitions_away_team_scored = DatabaseConnection.query_goals_scored(cursor, self.away_team, goal)
            df_scored_away_team = pd.concat([df_scored_away_team, object_db_funcitions_away_team_scored])
            
            object_db_funcitions_home_team_conceded = DatabaseConnection.query_goals_scored(cursor, self.home_team, goal)
            df_conceded_home_team = pd.concat([df_conceded_home_team, object_db_funcitions_home_team_conceded])
            
            object_db_funcitions_away_team_conceded = DatabaseConnection.query_goals_scored(cursor, self.away_team, goal)
            df_conceded_away_team = pd.concat([df_conceded_away_team, object_db_funcitions_away_team_conceded])        
                     
        message_home_team = f'{self.home_team} tem estatística de gols marcados como mandante:\n' 
        for index, row in df_scored_home_team.iterrows():
            message_home_team += f'{row["type_goal"]}: {row["home"]}%\n'
        message_home_team += f'\n{self.home_team} tem estatística de gols sofridos como mandante:\n'
        for index, row in df_conceded_home_team.iterrows():
            message_home_team += f'{row["type_goal"]}: {row["home"]}%\n'
        
        message_away_team = f'{self.away_team} tem estatística de gols marcados como visitante:\n' 
        for index, row in df_scored_away_team.iterrows():
            message_away_team += f'{row["type_goal"]}: {row["away"]}%\n'
        message_away_team += f'{self.away_team} tem estatística de gols sofridos como visitante:\n' 
        for index, row in df_conceded_away_team.iterrows():
            message_away_team += f'{row["type_goal"]}: {row["away"]}%\n'  
                       
        if message_home_team:
            asyncio.run(send_message_with_retry(message_home_team))
        if message_away_team:
            asyncio.run(send_message_with_retry(message_away_team))
              
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

        type_goals_list=[]
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
                type_goals_above = row['goals']
                home_vs_away = row['home_vs_away']                                  
                message_goals_above += f"Gols acima de {type_goals_above}: {home_vs_away}% 🎯\n"
                goals_above_added.add(type_goals_above)
                if type_goals_above == 1.5:
                    type_goals_list.append(type_goals_above)
             
        if not df_filtered_goals_below.empty:
            message_goals_below = f"⚽Oportunidade para {self.home_team} vs {self.away_team} ⚽:\n\n"
            goals_below_added = set()
            for index, row in df_filtered_goals_below.iterrows():
                type_goals_below = row['goals']
                home_vs_away = 100 - row['home_vs_away']                               
                message_goals_below += f"Gols abaixo de {type_goals_below}: {home_vs_away}% 🎯\n"  
                goals_below_added.add(type_goals_below)
                if type_goals_below == 3.5:
                    type_goals_below = type_goals_below * -1
                    type_goals_list.append(type_goals_below) 
                
        message += message_goals_above
        message += message_goals_below
        
        if message:
            asyncio.run(send_message_with_retry(message))
            for type in type_goals_list:
                self.additional_goals_statistics()
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
            asyncio.run(send_message_with_retry(message))

        cursor.close()
        connection.close()
    
    