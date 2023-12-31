import pandas as pd
import telegram
import asyncio
from dotenv import load_dotenv
import os
from db_functions import DatabaseConnection
from send_telegram_message import *

class DataProcessor:

    def __init__(self,  home_team_id,  away_team_id):
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
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
            object_db_funcitions_home_team_scored = DatabaseConnection.query_goals(cursor,'goals_scored', self.home_team_id, goal)
            df_scored_home_team = pd.concat([df_scored_home_team, object_db_funcitions_home_team_scored])
            
            object_db_funcitions_away_team_scored = DatabaseConnection.query_goals(cursor,'goals_scored', self.away_team_id, goal)
            df_scored_away_team = pd.concat([df_scored_away_team, object_db_funcitions_away_team_scored])
            
            object_db_funcitions_home_team_conceded = DatabaseConnection.query_goals(cursor, 'goals_conceded', self.home_team_id, goal)
            df_conceded_home_team = pd.concat([df_conceded_home_team, object_db_funcitions_home_team_conceded])
            
            object_db_funcitions_away_team_conceded = DatabaseConnection.query_goals(cursor, 'goals_conceded', self.away_team_id, goal)
            df_conceded_away_team = pd.concat([df_conceded_away_team, object_db_funcitions_away_team_conceded])        
        
        for home_team in df_scored_home_team['name'].astype(str).values:
            pass
        for away_team in df_scored_away_team['name'].astype(str).values:
            pass
               
        message_home_team = f'{home_team} tem estatística de gols marcados como mandante:\n' 
        for index, row in df_scored_home_team.iterrows():
            message_home_team += f'{row["type_goal"]}: {row["home"]}%\n'
        message_home_team += f'{home_team} tem estatística de gols sofridos como mandante:\n'
        for index, row in df_conceded_home_team.iterrows():
            message_home_team += f'{row["type_goal"]}: {row["home"]}%\n'
        
        message_away_team = f'{away_team} tem estatística de gols marcados como visitante:\n' 
        for index, row in df_scored_away_team.iterrows():
            message_away_team += f'{row["type_goal"]}: {row["away"]}%\n'
        message_away_team += f'{away_team} tem estatística de gols sofridos como visitante:\n' 
        for index, row in df_conceded_away_team.iterrows():
            message_away_team += f'{row["type_goal"]}: {row["away"]}%\n'  
                       
        if message_home_team:
            instance_send_telegram_message = TelegramMessenger()
            asyncio.run(instance_send_telegram_message.send_message_with_retry(message_home_team))
        if message_away_team:
            instance_send_telegram_message = TelegramMessenger()
            asyncio.run(instance_send_telegram_message.send_message_with_retry(message_away_team))
              
        cursor.close()
        connection.close()
    
    def filtered_goal_statistics(self):
        connection = DatabaseConnection.connect()      
        cursor = connection.cursor()
        type_goal=[1.5, 2.5, 3.5]
        df_scored_home_team = pd.DataFrame()
        df_scored_away_team = pd.DataFrame()
        df_result = pd.DataFrame()
        message = ''
        message_goals_above = ''
        message_goals_below = ''
        
        for type in type_goal:
            object_db_funcitions_home_team_scored = DatabaseConnection.query_goals(cursor,'goals_scored_conceded', self.home_team_id, type)
            df_scored_home_team = pd.concat([df_scored_home_team, object_db_funcitions_home_team_scored])
            
            object_db_funcitions_away_team_scored = DatabaseConnection.query_goals(cursor,'goals_scored_conceded', self.away_team_id, type)
            df_scored_away_team = pd.concat([df_scored_away_team, object_db_funcitions_away_team_scored])
            
        df_scored_home_team = df_scored_home_team.reset_index(drop=True)
        df_scored_away_team = df_scored_away_team.reset_index(drop=True)
        
        df_result['home_team']= df_scored_home_team['name'] 
        df_result['away_team']= df_scored_away_team['name']
        df_result['type_goal']= df_scored_away_team['type_goal']
        df_result['total']= (df_scored_home_team['total'] + df_scored_away_team['total'])/2
        df_result['average_home_away']= (df_scored_home_team['home']+df_scored_away_team['away'])/2
       
        df_filtered_goals_above = df_result[(df_result['total'] >= 75) & (df_result['average_home_away'] >= 75)]
        df_filtered_goals_below = df_result[(df_result['total'] <= 25) & (df_result['average_home_away'] <= 25)]
        
        print(df_filtered_goals_above)
        print(df_filtered_goals_below)
                                
        if not df_filtered_goals_above.empty:
            for home_team in df_filtered_goals_above['home_team'].astype(str).values:
                for away_team in df_filtered_goals_above['away_team'].astype(str).values:
            
                    message_goals_above = f"⚽Oportunidade para {home_team} vs {away_team} ⚽:\n\n"
                    goals_above_added = set()
                    for index, row in df_filtered_goals_above.iterrows():
                        type_goals_above = row['type_goal']
                        home_vs_away = row['average_home_away']                                  
                        message_goals_above += f"Gols acima de {type_goals_above}: {home_vs_away}% 🎯\n"
                        goals_above_added.add(type_goals_above)       
             
        if not df_filtered_goals_below.empty:
            for home_team in df_filtered_goals_below['home_team'].astype(str).values:
                for away_team in df_filtered_goals_below['away_team'].astype(str).values:
                    
                    message_goals_below = f"⚽Oportunidade para {home_team} vs {away_team} ⚽:\n\n"
                    goals_below_added = set()
                    for index, row in df_filtered_goals_below.iterrows():
                        type_goals_below = row['type_goal']
                        home_vs_away = 100 - row['average_home_away']                               
                        message_goals_below += f"Gols abaixo de {type_goals_below}: {home_vs_away}% 🎯\n"  
                        goals_below_added.add(type_goals_below)     
                
        message += message_goals_above
        message += message_goals_below
        
        if message:
            instance_send_telegram_message = TelegramMessenger()
            asyncio.run(instance_send_telegram_message.send_message_with_retry(message))
            self.additional_goals_statistics()
        cursor.close()
        connection.close()
   
    def filtered_corners_statistics(self):
        connection = DatabaseConnection.connect()
        cursor = connection.cursor()
        type_corners=[7.5, 8.5, 9.5, 10.5, 11.5, 12.5]
        df_corners_home_team = pd.DataFrame()
        df_corners_away_team = pd.DataFrame()
        df_result = pd.DataFrame()
        message = ''
        message_corners_above = ''
        message_corners_below = ''
        
        for type in type_corners:
            object_db_funcitions_home_team_corners = DatabaseConnection.query_corners(cursor, self.home_team_id, type)
            df_corners_home_team = pd.concat([df_corners_home_team, object_db_funcitions_home_team_corners])
            
            object_db_funcitions_away_team_corners = DatabaseConnection.query_corners(cursor, self.away_team_id, type)
            df_corners_away_team = pd.concat([df_corners_away_team, object_db_funcitions_away_team_corners])
        
        df_corners_home_team = df_corners_home_team.reset_index(drop=True)
        df_corners_away_team = df_corners_away_team.reset_index(drop=True)
               
        df_result['home_team']= df_corners_home_team['name'] 
        df_result['away_team']= df_corners_away_team['name']
        df_result['type_corners']= df_corners_away_team['type_corners']
        df_result['total']= (df_corners_home_team['total'] + df_corners_away_team['total'])/2
        df_result['average_home_away']= (df_corners_home_team['home']+ df_corners_away_team['away'])/2     
        
        df_filtered_corners_above = df_result[(df_result['total'] >= 70) & (df_result['average_home_away'] >= 70)]
        df_filtered_corners_below = df_result[(df_result['total'] <= 25) & (df_result['average_home_away'] <= 25)]
        
        print(df_filtered_corners_above) 
        print(df_filtered_corners_below)
          
        if not df_filtered_corners_above.empty:
            for home_team in df_filtered_corners_above['home_team'].astype(str).values:
                for away_team in df_filtered_corners_above['away_team'].astype(str).values:
                    message_corners_above = f"⚽Oportunidades para {home_team} vs {away_team} ⚽:\n\n"
                    for index, row in df_filtered_corners_above.iterrows():
                        corners = row['type_corners']
                        home_vs_away = row['average_home_away']
                        message_corners_above += f"Escanteios acima de {corners}: {home_vs_away}% 🎌\n"

        if not df_filtered_corners_below.empty:
            for home_team in df_filtered_corners_below['home_team'].astype(str).values:
                for away_team in df_filtered_corners_below['away_team'].astype(str).values:
                    message_corners_below = f"⚽Oportunidades para {home_team} vs {away_team} ⚽:\n\n"
                    for index, row in df_filtered_corners_below.iterrows():
                        corners = row['type_corners']
                        home_vs_away = 100 - row['average_home_away']
                        message_corners_below += f"Escanteios abaixo de {corners}: {home_vs_away}% 🎌\n"

        message += message_corners_above
        message += message_corners_below

        if message:
            instance_send_telegram_message = TelegramMessenger()
            asyncio.run(instance_send_telegram_message.send_message_with_retry(message))

        cursor.close()
        connection.close()
    
    