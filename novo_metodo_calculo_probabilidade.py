from pandas import pandas as pd
from dotenv import load_dotenv
from db_functions import DatabaseConnection
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import requests


def testando_novos_calculos(self, home_team, home_team_id, away_team, away_team_id):
    self.home_team = home_team
    self.home_team_id = home_team_id
    self.away_team = away_team
    self.away_team_id = away_team_id
        
    connection = DatabaseConnection.connect()      
    cursor = connection.cursor()
    df_scored = pd.DataFrame()
    df_conceded = pd.DataFrame()
    tabelas = ['goals_scored', 'goals_conceded']
    
    tipos_de_gols = [0.5, 1.5, 2.5]
    
    for tipo_de_gol in tipos_de_gols:
        object_db_funcitions_away_team_scored = DatabaseConnection.query_goals(cursor, 'goals_scored', self.home_team_id, tipo_de_gol)
        df_scored = pd.concat([df_scored, object_db_funcitions_away_team_scored])

    
    for tipo_de_gol in tipos_de_gols:
        object_db_funcitions_away_team_scored = DatabaseConnection.query_goals(cursor, 'goals_conceded', self.away_team_id, tipo_de_gol)
        df_conceded = pd.concat([df_conceded, object_db_funcitions_away_team_scored])         
            
    groups = df_scored.groupby('name')
    home_team_scored_df = groups.get_group('Man City')
    away_team_scored_df = groups.get_group('Liverpool')

    groups = df_conceded.groupby('name')
    home_team_conceded_df = groups.get_group('Man City')
    away_team_conceded_df = groups.get_group('Liverpool')

    time_a_marcar_05 = float(home_team_scored_df.loc[home_team_scored_df['type_goal'] == 0.5, 'home'].iloc[0])/100
    time_a_marcar_15 = float(home_team_scored_df.loc[home_team_scored_df['type_goal'] == 1.5, 'home'].iloc[0])/100
    time_a_marcar_25 = float(home_team_scored_df.loc[home_team_scored_df['type_goal'] == 2.5, 'home'].iloc[0])/100
    time_a_sofrer_05 = float(home_team_conceded_df.loc[home_team_conceded_df['type_goal'] == 0.5, 'home'].iloc[0])/100
    time_a_sofrer_15 = float(home_team_conceded_df.loc[home_team_conceded_df['type_goal'] == 1.5, 'home'].iloc[0])/100
    time_a_sofrer_25 = float(home_team_conceded_df.loc[home_team_conceded_df['type_goal'] == 2.5, 'home'].iloc[0])/100

    time_b_marcar_05 = float(away_team_scored_df.loc[away_team_scored_df['type_goal'] == 0.5, 'home'].iloc[0])/100
    time_b_marcar_15 = float(away_team_scored_df.loc[away_team_scored_df['type_goal'] == 1.5, 'home'].iloc[0])/100
    time_b_marcar_25 = float(away_team_scored_df.loc[away_team_scored_df['type_goal'] == 2.5, 'home'].iloc[0])/100
    time_b_sofrer_05 = float(away_team_conceded_df.loc[away_team_conceded_df['type_goal'] == 0.5, 'home'].iloc[0])/100
    time_b_sofrer_15 = float(away_team_conceded_df.loc[away_team_conceded_df['type_goal'] == 1.5, 'home'].iloc[0])/100
    time_b_sofrer_25 = float(away_team_conceded_df.loc[away_team_conceded_df['type_goal'] == 2.5, 'home'].iloc[0])/100


    ######## ALGORITIMO DO GPT (TEORIA DA PROBABILIDADE TOTAL)#########
    chance_sair_1gol = ((time_a_marcar_05 * time_b_sofrer_05) + (time_b_marcar_05 * time_a_sofrer_05))/2
    chance_sair_mais_1_gol = ((time_a_marcar_15 * time_b_sofrer_15) + (time_b_marcar_15 * time_a_sofrer_15))/2
    chance_sair_mais_2_gol = ((time_a_marcar_25 * time_b_sofrer_25) + (time_b_marcar_25 * time_a_sofrer_25))/2

    print('Algoritmo do GPT')
    print(f'Chance de sair 1 gol: {chance_sair_1gol}')
    print(f'Chance de sair mais de 1 gols: {chance_sair_mais_1_gol}')
    print(f'Chance de sair mais de 2 gols: {chance_sair_mais_2_gol}')

    ############### ALGORITIMO DO GEMINI################

    # Probabilidades de gols na partida
    prob_1_gol = (time_a_marcar_05 * time_b_sofrer_05) + (time_b_marcar_05 * time_a_sofrer_05)
    prob_mais_1_gol = (time_a_marcar_15 * 1) + (time_b_marcar_15 * 1) + (time_a_marcar_15 * time_b_marcar_15)
    prob_mais_2_gols = (time_a_marcar_25 * 1) + (time_b_marcar_25 * 1) + (time_a_marcar_25 * time_b_marcar_25)

    # Ajustando as probabilidades
    prob_1_gol = prob_1_gol / 2
    prob_mais_1_gol = prob_mais_1_gol / 3
    prob_mais_2_gols = prob_mais_2_gols / 3

    print('Algoritmo do GEMINI')
    print(f"Probabilidade de sair 1 gol: {prob_1_gol:.2%}")
    print(f"Probabilidade de sair mais de 1 gol: {prob_mais_1_gol:.2%}")
    print(f"Probabilidade de sair mais de 2 gols: {prob_mais_2_gols:.2%}")

    ### Para sair 1 gol ###
    # 1 gol time A - time B sofrendo 1 gol
    # 1 gol time B - tima A sofrendo 1 gol
    # resultados: A 1 x B 0 // A 0 x B 1

    ### Para sair mais de 1 gol ###
    # 2 gols time A com time B sofrendo 2 gols
    # 1 gol time A com time B sofrendo 1 gol e 1 gol time B com time A sofrendo 1 gol
    # 2 gols tim B com time A sofrendo 2 gols
    # resultados: A 2 X B 0 // A 1 X B 1 // A 0 X B 2

    ### Para sair mais de 2 gols ###
    # 3 gols do time A com o Time B sofrendo 3 gols
    # 2 gols do time A com o time B sofrendo 2 gols e 1 gol do time B com o time A sofrendo 1 gol
    # 1 gol do time A com o time B sofrendo 1 gol e 1 2 gols do time B com o time A sofrendo 2 gols
    # 3 gols do time B com o time A sofrendo 3 gols
    # resultados: A 3 X B 0 // A 2 X B 1 // A 1 X B 2 // A 0 X B 3

    ############# MINHA ADAPTAÇÃO ###################
    # Probabilidades de gols na partida
    prob_1_gol = (time_a_marcar_05 * time_b_sofrer_05) + (time_b_marcar_05 * time_a_sofrer_05)

    # 2 gols time A com time B sofrendo 2 gols
    # 1 gol time A com time B sofrendo 1 gol e 1 gol time B com time A sofrendo 1 gol
    # 2 gols tim B com time A sofrendo 2 gols
    prob_mais_1_gol = (time_a_marcar_15 * time_b_sofrer_15) + (time_b_marcar_15 * time_a_sofrer_15) + (time_a_marcar_05 * time_b_sofrer_05 + time_b_marcar_05 * time_a_sofrer_05)
        
    # 3 gols do time A com o Time B sofrendo 3 gols ok
    # 2 gols do time A com o time B sofrendo 2 gols e 1 gol do time B com o time A sofrendo 1 gol ok
    # 1 gol do time A com o time B sofrendo 1 gol e 1 2 gols do time B com o time A sofrendo 2 gols
    # 3 gols do time B com o time A sofrendo 3 gols ok
    prob_mais_2_gols = (time_a_marcar_25 * time_b_sofrer_25) + (time_b_marcar_25 * time_a_sofrer_25) + (time_a_marcar_15 * time_b_sofrer_15 + time_b_marcar_05 * time_a_marcar_05) + (time_b_marcar_15 * time_a_sofrer_15 + time_a_marcar_05 * time_b_sofrer_05)

    # Ajustando as probabilidades
    prob_1_gol = prob_1_gol / 2
    prob_mais_1_gol = prob_mais_1_gol / 3
    prob_mais_2_gols = prob_mais_2_gols / 4

    print('Minha adaptação')
    print(f"Probabilidade de sair 1 gol: {prob_1_gol:.2%}")
    print(f"Probabilidade de sair mais de 1 gol: {prob_mais_1_gol:.2%}")
    print(f"Probabilidade de sair mais de 2 gols: {prob_mais_2_gols:.2%}")

# list_country_id_for_search_next_day_games = [['Belgium','Pro League', 144],['Greece','Greek Super League', 197],['Scotland','SPL', 179], ['Italy', 'Serie A', 135], ['Italy', 'Serie B', 136],
#                         ['England', 'Premier League', 39], ['England', 'Championship', 40], ['England', 'League One', 41],  ['England', 'League Two', 42],
#                         ['Spain', 'La Liga', 140], ['Spain', 'Segunda Division', 141], ['Germany', 'Bundesliga', 78],['Germany','2. Bundesliga', 79], ['France', 'Ligue 1', 61], ['France', 'Ligue 2', 62],
#                         ['Netherlands', 'Eredivisie', 88], ['Netherlands', 'Eerste Divisie', 89],['France', 'Coupe de France', 66],['Europa','UEFA Champions League', 2],['Europa','UEFA Europa League', 3],['Europa','Europa Conference League', 848], 
#                         ['Portugal', 'Primeira Liga', 94], ['Turkey', 'Super Lig', 203], 
#                         ['Denmark', 'Superliga', 119], ['USA', 'Major League Soccer', 253], ['Norway', 'Eliteserien', 103], ['Austria', 'Bundesliga', 218], ['Mexico', 'Liga MX', 262], ['Argentina','Primera Division', 128]]   

list_country_id_for_search_next_day_games = ['England', 'Premier League', 39], ['England', 'Championship', 40]
games_date = '16-03-2024'

conexao = DatabaseConnection.connect()
cursor = conexao.cursor()
date_object = datetime.strptime(games_date, '%d-%m-%Y')
date_us_format = date_object.strftime("%Y-%m-%d")

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
list_team_id = []
RapidAPI = os.getenv('RapidAPI')


for country_list in list_country_id_for_search_next_day_games:
    query_params = {"date": date_us_format , "league": country_list[2], "season": "2023"}
    
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
            home_team_name = game["teams"]["home"]["name"]
            home_team_id = game["teams"]["home"]["id"]
            away_team_name = game["teams"]["away"]["name"]
            away_team_id = game["teams"]["away"]["id"]
            
            query_home_team_id = 'SELECT team_id FROM team WHERE api_id = %s'
            cursor.execute(query_home_team_id, (home_team_id,))
            result_home_team_id = cursor.fetchall()
            if result_home_team_id:
                query_away_team_id = 'SELECT team_id FROM team WHERE api_id = %s'
                cursor.execute(query_away_team_id, (away_team_id,))
                result_away_team_id = cursor.fetchall()
                if result_away_team_id:
                    list_team_id.append([home_team_name, home_team_id, away_team_name, away_team_id])
    else:
        print(f"No games found for {country_list[0]} {country_list[1]}")  
print(list_team_id)

for home_team, home_team_id, away_team, away_team_id in list_team_id:  

    df_gols = testando_novos_calculos(home_team, home_team_id, away_team, away_team_id)                 
