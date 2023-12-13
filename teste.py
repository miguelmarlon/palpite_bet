from scraping_team_goals_total import Goals
from scraping_corners import Corners
from scraping_team_goals import TeamGoals
from data_processor import DataProcessor
import requests
from db_functions import DatabaseConnection
from dotenv import load_dotenv
import os
import pandas as pd
from functions_api import FunctionsApi

corner_quantities = ['7.5', '8.5','9.5', '10.5', '11.5', '12.5']
country_list = [['Italy', 'Serie A',135 ]]
goal_total_quantities = ['Over 1.5']

country_list = [['Italy', 'Serie A',135 ], ['Italy', 'Serie B',136 ], ['England', 'Premier League',39 ], ['England', 'Championship',40 ], ['England', 'League One',41], ['England', 'League Two', 42 ], 
                ['Spain', 'La Liga',140 ], ['Spain', 'Segunda Division',141 ] ,['Germany','Bundesliga',78 ],['Germany','Bundesliga 2',79],['France', 'Ligue 1',61 ],['France', 'Ligue 2',62 ],
                ['Scotland','SPL',179], ['Netherlands', 'Eredivisie',88 ], ['Netherlands', 'Eerste Divisie',89],['Portugal','Portugese Liga NOS', 94],['Turkey','Turkish Super Lig', 203],['Greece','Greek Super League',197],['Belgium','Pro League',144], ['Brazil','Serie A',71],['Brazil','Serie B',72],
                ['Austria','Bundesliga',218], ['Argentina','Primera Division',128],['Denmark', 'Superliga',119], ['USA','US MLS',253],['Norway','Norwegian Eliteserien',103],['Mexico','Liga MX',262]]


# connection = DatabaseConnection.connect()
# cursor = connection.cursor()

# # functions_api_instance = FunctionsApi()
# # functions_api_instance.search_games()

# cursor.close()
# connection.close()

# for goals_quantity in goal_total_quantities:
#     for country, league, api_league_id in country_list:
#         goals_instance = Goals(country, league, goals_quantity, api_league_id)
#         data = goals_instance.create_goals_scored_conceded_table()
        
# for corner_quantity in corner_quantities:
#     for country, league, api_league_id in country_list:        
#         corners_instance = Corners(country, league, corner_quantity)
#         data= corners_instance.update_corners_table()

# for goals_quantity in goal_total_quantities:
#     for country, league, api_league_id in country_list:
#         goals_instance = TeamGoals(country, league, goals_quantity, api_league_id)
#         data = goals_instance.create_goals_scored_table()
#         data = goals_instance.create_goals_conceded_table()

# data_processor_instance = DataProcessor('Bayern Munich', 'Dortmund')       
# data_processor_instance.filtered_corners_statistics() 


# RapidAPI = os.getenv('RapidAPI')
# url = "https://api-football-v1.p.rapidapi.com/v3/teams"

# querystring = {"league":"39","season":"2023","country":"England"}

# headers = {
# 	"X-RapidAPI-Key": RapidAPI,
# 	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)
# list_teams=[]
# result_dfs = []

# if response.status_code == 200:
#     json_data = response.json()
#     data = json_data['response']
#     for team in data:
#         id = team['team']['id']
#         name = team['team']['name'].rstrip()
#         list_teams.append([id, name])
# else:
    
#     print(f"Erro na solicitação: {response.status_code}")
    
# print(list_teams)

# connection = DatabaseConnection.connect()
# cursor = connection.cursor()
# for team_id_api, team  in list_teams:

#     result = DatabaseConnection.set_team_id_api(cursor, 39, team, team_id_api)
#     connection.commit()

#     if result is not None:
#        result_dfs.append(result)

# final_result_df = pd.concat(result_dfs, ignore_index=True)
# final_result_df.to_excel('teams_not_updated.xlsx', index=False)
    
# cursor.close()
# connection.close()
   
a=1