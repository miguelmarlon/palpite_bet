import requests
import json
from datetime import datetime, timedelta
from tratando_dados import tratando_dados
import asyncio
from dotenv import load_dotenv
import os
from send_telegram_message import send_message



lista_pais_id = [['Belgium','Pro League', 144],['Greece','Greek Super League', 197],['Scotland','SPL', 179], ['Italy', 'Serie A', 135], ['Italy', 'Serie B', 136],
                ['England', 'Premier League', 39], ['England', 'Championship', 40], ['England', 'League One', 41],  
                ['Spain', 'La Liga', 140], ['Spain', 'Segunda Division', 141], ['Germany', 'Bundesliga', 78],['Germany','2. Bundesliga', 79], ['France', 'Ligue 1', 61], ['France', 'Ligue 2', 62],
                ['Europa','UEFA Champions League', 2],['Europa','UEFA Europa League', 3],['Europa','Europa Conference League', 848],['Netherlands', 'Eredivisie', 88], ['Netherlands', 'Eerste Divisie', 89], 
                ['Portugal', 'Primeira Liga', 94], ['Turkey', 'Super Lig', 203], ['Brazil', 'Serie A', 71], ['Brazil', 'Serie B', 72], 
                ['Denmark', 'Superliga', 119], ['USA', 'Major League Soccer', 253], ['Norway', 'Eliteserien', 103], ['Australia', 'A-League', 188],['Austria', 'Bundesliga', 218],
                ['Sweden', 'Allsvenskan', 113], ['Switzerland', 'Super League', 207],  ['Mexico', 'Liga MX', 262], ['Poland', 'Ekstraklasa', 106],['Argentina','Primera Division', 128]]

data_atual = datetime.now()
data_posterior = data_atual + timedelta(days=1)
data_posterior_formatada_para_pesquisa_api = data_posterior.strftime("%Y-%m-%d")
data_para_postagem_telegram = data_posterior.strftime("%d-%m")
mensagem_jogos_posterior = f'🤑🤑⚽ JOGOS DIA {data_para_postagem_telegram} ⚽🤑🤑'

           
def busca_jogos_dia_posterior():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    team_names = []
    lista_times_final = []
    RapidAPI = os.getenv('RapidAPI')
    
    for lista in lista_pais_id:
        querystring = {"date":data_posterior_formatada_para_pesquisa_api,"league":lista[2],"season":"2023"}
        headers = {
            "X-RapidAPI-Key": RapidAPI,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:    
            data = response.json()       
           
        else:
            print(f"Erro na solicitação. Código de status: {response.status_code}")
        
        if "response" in data and data["response"]:
            for game in data["response"]:
                home_team_name = game["teams"]["home"]["name"].rstrip()
                away_team_name = game["teams"]["away"]["name"].rstrip()
                team_names.append([home_team_name, away_team_name])  
                            
        else:
            print(f"Nenhum jogo encontrado para {lista[0]} {lista[1]}")  
        
        lista_times_final.append([team_names])  
    
    for time_casa, time_fora in team_names:       
        
        tratando_dados_obj =tratando_dados(time_casa, time_fora)
        tratando_dados_obj.estatistica_filtrada_gol()
        #tratando_dados_obj.estatistica_filtrada_escanteios()     

if __name__=="__main__":
    asyncio.run(send_message(mensagem_jogos_posterior))
    busca_jogos_dia_posterior()

 

