from data_processor import DataProcessor
from dotenv import load_dotenv
import os
from database_connection import DatabaseConnection
from create_database import CreateDatabase
from send_telegram_message import *

def search_team_by_name(cursor, team_name):
        team_query = "SELECT * FROM goals WHERE name LIKE %s"
        cursor.execute(team_query, (f'%{team_name}%',))
        return cursor.fetchall()
    
conexao = DatabaseConnection.connect()
cursor = conexao.cursor()
load_dotenv()
teams_list= []

print()
print('******************WELCOME TO THE PROGRAM!******************')
print()

while True:
    option = input('0 - EXIT\n\n'
                   '1 - ENTER TEAM SELECTION\n\n'
                   '2 - UPDATE DATABASE\n\n'
                   '3 - CREATE DATABASE\n\n'
                   '4 - DELETE DUPLICATE LINES IN THE DATABASE\n\n'
                   'OPTION: ')
    match option:
        case '0':
            print('EXITING THE PROGRAM...')
            exit()
        case '1':
            games_date= input('What is the date of the games?\n EXAMPLE:\n 22-11\n')
            games_day = f'🤑🤑⚽ PALPITES PARA O DIA {games_date} ⚽🤑🤑'
            while True:
                
                home_team = input('ENTER THE NAME OF THE HOME TEAM:')
                result_home = search_team_by_name(cursor, home_team)

                if result_home:
                    home_team_names = set(row[2] for row in result_home)

                    if len(home_team_names) == 1:
                        home_team = result_home[0][2]
                    else:
                        print("Multiple matching teams found. Choose one:")
                        for i, name in enumerate(home_team_names):
                            print(f"{i + 1}. {name}")

                        choice = int(input("Enter the number of the desired team: "))
                        home_team_names = list(home_team_names)
                        home_team = home_team_names[choice - 1]
                        print(f"The chosen team name is: {home_team}")

                    away_team = input('ENTER THE NAME OF THE AWAY TEAM:')
                    result_away = search_team_by_name(cursor, away_team)

                    if result_away:
                        away_team_names = set(row[2] for row in result_away)

                        if len(away_team_names) == 1:
                            away_team = result_away[0][2]
                        else:
                            print("Multiple matching teams found. Choose one:")
                            for i, name in enumerate(away_team_names):
                                print(f"{i + 1}. {name}")

                            choice = int(input("Enter the number of the desired team: "))
                            away_team_names = list(away_team_names)
                            away_team = away_team_names[choice - 1]
                            print(f"The chosen team name is: {away_team}")

                        temporary_list = [home_team, away_team]
                        teams_list.append(temporary_list)
                    else:
                        print(f'THE TEAM {away_team} WAS NOT FOUND!')
                else:
                    print(f'THE TEAM {home_team} WAS NOT FOUND!')
                    
                continue_input = input('PRESS ENTER TO CONTINUE OR 2 TO EXIT:')
                if continue_input == '2':
                    print('WAIT A MOMENT TO FINISH :)')
                    print()
                    break
            
            asyncio.run(send_message_with_retry(games_day))  
            for time_casa, time_fora in teams_list:    
                tratando_dados_objeto = DataProcessor(time_casa, time_fora)       
                df_gols = tratando_dados_objeto.filtered_goal_statistics()
                df_escanteios = tratando_dados_objeto.filtered_corners_statistics()
            exit()     
            
        case '2':
            criando_banco_de_dados_gols_obj = CreateDatabase()
            criando_banco_de_dados_gols_obj.update_goals_database()
            criando_banco_de_dados_escanteios_obj = CreateDatabase()
            criando_banco_de_dados_escanteios_obj.update_corners_database()
            break
            
        case '3':
            criando_banco_de_dados_gols_obj = CreateDatabase()
            criando_banco_de_dados_gols_obj.create_goals_total_database()
            criando_banco_de_dados_escanteios_obj = CreateDatabase()
            criando_banco_de_dados_escanteios_obj.create_corners_database()
            create_db_goals_scored_instance = CreateDatabase()
            create_db_goals_scored_instance.create_goals_scored_database()
            create_db_goals_conceded_instance = CreateDatabase()
            create_db_goals_conceded_instance.create_goals_conceded_database()
            break
        
        case '4':
            criando_banco_de_dados_obj = CreateDatabase()
            criando_banco_de_dados_obj.remove_duplicate_rows_from_database()
            
            break
                
        case _:
            print('INVALID OPTION!')
