import requests
import json
from datetime import datetime, timedelta
from data_processor import DataProcessor
import asyncio
from dotenv import load_dotenv
import os
from send_telegram_message import send_message

list_country_id = [['Brazil', 'Serie B', 72],['Spain', 'Segunda Division', 141]]

# list_country_id = [['Belgium','Pro League', 144],['Greece','Greek Super League', 197],['Scotland','SPL', 179], ['Italy', 'Serie A', 135], ['Italy', 'Serie B', 136],
#                 ['England', 'Premier League', 39], ['England', 'Championship', 40], ['England', 'League One', 41],  
#                 ['Spain', 'La Liga', 140], ['Spain', 'Segunda Division', 141], ['Germany', 'Bundesliga', 78],['Germany','2. Bundesliga', 79], ['France', 'Ligue 1', 61], ['France', 'Ligue 2', 62],
#                 ['Europa','UEFA Champions League', 2],['Europa','UEFA Europa League', 3],['Europa','Europa Conference League', 848],['Netherlands', 'Eredivisie', 88], ['Netherlands', 'Eerste Divisie', 89], 
#                 ['Portugal', 'Primeira Liga', 94], ['Turkey', 'Super Lig', 203], ['Brazil', 'Serie A', 71], ['Brazil', 'Serie B', 72], 
#                 ['Denmark', 'Superliga', 119], ['USA', 'Major League Soccer', 253], ['Norway', 'Eliteserien', 103], ['Australia', 'A-League', 188],['Austria', 'Bundesliga', 218],
#                 ['Sweden', 'Allsvenskan', 113], ['Switzerland', 'Super League', 207],  ['Mexico', 'Liga MX', 262], ['Poland', 'Ekstraklasa', 106],['Argentina','Primera Division', 128]]

current_date = datetime.now()
next_date = current_date + timedelta(days=1)
formatted_next_date_for_api_search = next_date.strftime("%Y-%m-%d")
date_for_telegram_posting = next_date.strftime("%d-%m")
message_for_next_day_games = f'🤑🤑⚽ GAMES DAY {date_for_telegram_posting} ⚽🤑🤑'

def search_next_day_games():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    team_names = []
    final_team_list = []
    RapidAPI = os.getenv('RapidAPI')
    
    for country_list in list_country_id:
        query_params = {"date": "2023-11-17", "league": country_list[2], "season": "2023"}
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
    
    for home_team, away_team in team_names:       
        
        data_processor_obj = DataProcessor(home_team, away_team)
        data_processor_obj.filtered_goal_statistics()
        # data_processor_obj.filtered_corners_statistics()     

if __name__ == "__main__":
    asyncio.run(send_message(message_for_next_day_games))
    search_next_day_games()

 

