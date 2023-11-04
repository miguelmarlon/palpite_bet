import requests
import json
from datetime import datetime, timedelta
from tratando_dados import tratando_dados
import asyncio
from dotenv import load_dotenv
import os
import telegram

list_pais_id = [['Belgium','Pro League', 144],['Greece','Greek Super League', 197],['Scotland','SPL', 179], ['Scotland','Scottish Championship', 180], ['Italy', 'Serie A', 135], ['Italy', 'Serie B', 136],
                ['England', 'Premier League', 39], ['England', 'Championship', 40], ['England', 'League One', 41], ['England', 'League Two', 42], 
                ['England', 'National League', 43], ['Spain', 'La Liga', 140], ['Spain', 'Segunda Division', 141], ['Germany', 'Bundesliga', 78],['Germany','2. Bundesliga', 79], ['France', 'Ligue 1', 61], ['France', 'Ligue 2', 62], 
                ['Netherlands', 'Eredivisie', 88], ['Netherlands', 'Eerste Divisie', 89], ['Portugal', 'Primeira Liga', 94], ['Turkey', 'Super Lig', 203], ['Brazil', 'Serie A', 71], ['Brazil', 'Serie B', 72], 
                 ['Russia', 'Premier League', 235], ['Denmark', 'Superliga', 119], ['USA', 'Major League Soccer', 253], ['Norway', 'Eliteserien', 103], 
                ['Sweden', 'Allsvenskan', 113], ['Switzerland', 'Super League', 207],  ['Mexico', 'Liga MX', 262], ]

#reduzindo o tamanho da lista para evitar problemas de conexão com API
#['Australia', 'A-League', 188],['China','Super League', 169],['Belgium','First Division B', 145],['Austria', 'Bundesliga', 218],
# ['Poland', 'Ekstraklasa', 106],['Finland', 'Veikkausliiga', 244], ['Japan', 'J1 League', 98],['Argentina','Primera Division', 128],

data_atual = datetime.now()
data_posterior = data_atual + timedelta(days=2)
data_posterior_formatada_para_pesquisa_api = data_posterior.strftime("%Y-%m-%d")
data_para_postagem_telegram = data_posterior.strftime("%d-%m")
mensagem = f'🤑🤑⚽ JOGOS DIA {data_para_postagem_telegram} ⚽🤑🤑'

async def enviar_mensagem_telegram(mensagem):
    load_dotenv()
    bot_token = os.getenv('bot_token')
    chat_id = os.getenv('chat_id')
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=mensagem)
           
def busca_jogos_dia_posterior():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    team_names = []
    lista_times_final = []
    RapidAPI = os.getenv('RapidAPI')
    
    for lista in list_pais_id:
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
                #print(team_names)                
        else:
            print(f"Nenhum jogo encontrado para {lista[0]} {lista[1]}")  
        
        lista_times_final.append([team_names])  
    
    for time_casa, time_fora in team_names:       
        
        tratando_dados_obj =tratando_dados(time_casa, time_fora)
        tratando_dados_obj.estatistica_filtrada_gol(),
        tratando_dados_obj.estatistica_filtrada_escanteios()
               
        
def encontrar_id_ligas():
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    lista_pais_id = []
    RapidAPI = os.getenv('RapidAPI')
    
    for pais_nome, liga_nome in list_pais_id:
        querystring = {"name":liga_nome,"country":pais_nome,"season":"2023"}
        headers = {
            "X-RapidAPI-Key": RapidAPI,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            data = response.json()
            if "response" in data and data["response"]:
                pais = pais_nome
                liga = liga_nome
                id = data["response"][0]["league"]["id"]
                lista_pais_id.append([pais, liga, id])
                print('achei a liga ' + liga_nome)
            else:
                print(f"Nenhum dado encontrado para {pais_nome}, {liga_nome}")
        else:
            print(f"Erro na solicitação. Código de status: {response.status_code}")

    print(lista_pais_id)

if __name__=="__main__":
    loop = asyncio.get_event_loop()
    asyncio.run(enviar_mensagem_telegram(mensagem))
    busca_jogos_dia_posterior()

a=1
