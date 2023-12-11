import requests
import json
from datetime import datetime, timedelta
from data_processor import DataProcessor
import asyncio
from dotenv import load_dotenv
import os
from send_telegram_message import *
from db_functions import DatabaseConnection
import pandas as pd

class FunctionsApi:
    
    def __init__(self):
        self.list_country_id_for_search_team_id_api = [['Belgium','Pro League', 144],['Greece','Greek Super League', 197],['Scotland','SPL', 179], ['Italy', 'Serie A', 135], ['Italy', 'Serie B', 136],
                        ['England', 'Premier League', 39], ['England', 'Championship', 40], ['England', 'League One', 41],  ['England', 'League Two', 42],
                        ['Spain', 'La Liga', 140], ['Spain', 'Segunda Division', 141], ['Germany', 'Bundesliga', 78],['Germany','2. Bundesliga', 79], ['France', 'Ligue 1', 61], ['France', 'Ligue 2', 62],
                        ['Netherlands', 'Eredivisie', 88], ['Netherlands', 'Eerste Divisie', 89], 
                        ['Portugal', 'Primeira Liga', 94], ['Turkey', 'Super Lig', 203], ['Brazil', 'Serie A', 71], ['Brazil', 'Serie B', 72], 
                        ['Denmark', 'Superliga', 119], ['USA', 'Major League Soccer', 253], ['Norway', 'Eliteserien', 103], ['Austria', 'Bundesliga', 218], ['Mexico', 'Liga MX', 262], ['Argentina','Primera Division', 128]]
                       
        self.list_country_id_for_search_next_day_games = [['Belgium','Pro League', 144],['Greece','Greek Super League', 197],['Scotland','SPL', 179], ['Italy', 'Serie A', 135], ['Italy', 'Serie B', 136],
                        ['England', 'Premier League', 39], ['England', 'Championship', 40], ['England', 'League One', 41],  ['England', 'League Two', 42],
                        ['Spain', 'La Liga', 140], ['Spain', 'Segunda Division', 141], ['Germany', 'Bundesliga', 78],['Germany','2. Bundesliga', 79], ['France', 'Ligue 1', 61], ['France', 'Ligue 2', 62],
                        ['Netherlands', 'Eredivisie', 88], ['Netherlands', 'Eerste Divisie', 89],['France', 'Coupe de France', 66],['Europa','UEFA Champions League', 2],['Europa','UEFA Europa League', 3],['Europa','Europa Conference League', 848], 
                        ['Portugal', 'Primeira Liga', 94], ['Turkey', 'Super Lig', 203], ['Brazil', 'Serie A', 71], ['Brazil', 'Serie B', 72], 
                        ['Denmark', 'Superliga', 119], ['USA', 'Major League Soccer', 253], ['Norway', 'Eliteserien', 103], ['Austria', 'Bundesliga', 218], ['Mexico', 'Liga MX', 262], ['Argentina','Primera Division', 128]]
        
        self.current_date = datetime.now()
        self.next_date = self.current_date + timedelta(days=1)
        self.formatted_next_date_for_api_search = self.next_date.strftime("%Y-%m-%d")
        self.date_for_telegram_posting = self.next_date.strftime("%d-%m")
        self.message_for_next_day_games = f'🤑🤑⚽ PALPITES PARA O DIA {self.date_for_telegram_posting} ⚽🤑🤑'

    def search_team_id_api(self):
        
        result_dfs = []
        
        for country,league, league_id in self.list_country_id_for_search_team_id_api:
            list_teams=[]
            RapidAPI = os.getenv('RapidAPI')
            url = "https://api-football-v1.p.rapidapi.com/v3/teams"

            querystring = {f"league":league_id,"season":"2023","country":{country}}

            headers = {
                "X-RapidAPI-Key": RapidAPI,
                "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            
            if response.status_code == 200:
                json_data = response.json()
                data = json_data['response']
                for team in data:
                    id = team['team']['id']
                    name = team['team']['name'].rstrip()
                    list_teams.append([id, name])
            else:
                
                print(f"Erro na solicitação: {response.status_code}")
                
            print(league)    
            print(list_teams)
            print()

            connection = DatabaseConnection.connect()
            cursor = connection.cursor()
            
            for team_id_api, team  in list_teams:
                
                result = DatabaseConnection.set_team_id_api(cursor, league_id, team, team_id_api)
                connection.commit()

                if result is not None:
                    result_dfs.append(result)
            cursor.close()
            connection.close()
            
        if result_dfs:
            final_result_df = pd.concat(result_dfs, ignore_index=True)
            final_result_df.to_excel('teams_not_updated.xlsx', index=False)         
            
    def search_next_day_games(self):
        
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        team_names = []
        final_team_list = []
        RapidAPI = os.getenv('RapidAPI')
        
        for country_list in self.list_country_id_for_search_next_day_games:
            query_params = {"date": "2023-12-08", "league": country_list[2], "season": "2023"}
            headers = {
                "X-RapidAPI-Key": RapidAPI,
                "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=query_params)

            if response.status_code == 200:    
                data = response.json()       
            else:
                print(f"Request error. Status code: {response.status_code}")
            
            if "response" in data and data["response"]:
                for game in data["response"]:
                    home_team_name = game["teams"]["home"]["name"].rstrip()
                    away_team_name = game["teams"]["away"]["name"].rstrip()
                    team_names.append([home_team_name, away_team_name])  
            else:
                print(f"No games found for {country_list[0]} {country_list[1]}")  
            
            final_team_list.append([team_names])  
        print(team_names)
        for home_team, away_team in team_names:       
            data_processor_obj = DataProcessor(home_team, away_team)
            data_processor_obj.filtered_goal_statistics()   
            # data_processor_obj.filtered_corners_statistics()

    
    # if __name__ == "__main__":
        # asyncio.run(send_message_with_retry(self.message_for_next_day_games))
        # search_next_day_games()