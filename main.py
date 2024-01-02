from data_processor import DataProcessor
from dotenv import load_dotenv
import os
from db_functions import DatabaseConnection
from create_database import CreateDatabase
from send_telegram_message import TelegramMessenger
from functions_api import FunctionsApi
import asyncio
    
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
            games_date= input('What is the date of the games?\n EXAMPLE:\n dd-mm-aaaa\n')
            games_day = f'🤑🤑⚽ PALPITES PARA O DIA {games_date} ⚽🤑🤑'
                                    
            automatically_or_manually = input('Type 1 to search for the games automatically or 2 to type the games you want:')
            
            match automatically_or_manually:
                case '1':
                    
                    functions_api_instance = FunctionsApi(games_date)
                    functions_api_instance.search_games()
                
                case '2':
                    
                    while True:
                        
                        home_team = input('ENTER THE NAME OF THE HOME TEAM:')
                        result_home = DatabaseConnection.search_team_by_name(cursor, home_team)

                        if result_home:
                            
                            if len(result_home) == 1:
                                _, home_team_name, _, team_id_home_api = result_home[0]
                            else:
                                print("Multiple matching teams found. Choose one:")
                                for i, (team_id, name, _, _) in enumerate(result_home):
                                    print(f"{i + 1}- {name}")

                                choice = int(input("Enter the number of the desired team: "))
                                _, home_team_name, _, team_id_home_api = result_home[choice - 1]
                                print(f"The chosen team name is: {home_team_name}")

                            away_team = input('ENTER THE NAME OF THE AWAY TEAM:')
                            result_away = DatabaseConnection.search_team_by_name(cursor, away_team)

                            if result_away:
                                
                                if len(result_away) == 1:
                                    _, away_team_name, _, team_id_away_api = result_away[0]
                                else:
                                    print("Multiple matching teams found. Choose one:")
                                    for i, (team_id, name, _, _) in enumerate(result_away):
                                        print(f"{i + 1}. {name}")

                                    choice = int(input("Enter the number of the desired team: "))
                                    _, away_team_name, _, team_id_away_api = result_away[choice - 1]
                                    print(f"The chosen team name is: {away_team}")

                                temporary_list = [team_id_home_api, team_id_away_api]
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
                    instance_send_telegram_message = TelegramMessenger()
                    asyncio.run(instance_send_telegram_message.send_message_with_retry(games_day))
                     
                case _: 
                    print('INVALID OPTION!')
                    
            for id_home, id_away in teams_list:    
                tratando_dados_objeto = DataProcessor(id_home, id_away)     
                df_gols = tratando_dados_objeto.filtered_goal_statistics()
                df_escanteios = tratando_dados_objeto.filtered_corners_statistics()
            exit()     
            
        case '2':
            print("""Enter 1 to update goal and corners table:\nEnter 2 to update the corners table:\nEnter 3 to update the goal table:""")
            type_update = input('Select an option: ')
            match type_update:
                
                case '1':
                    connection = DatabaseConnection.connect()
                    cursor = connection.cursor()
                    create_db_goals_instance = CreateDatabase()
                    create_db_goals_instance.update_goals_database()
                    
                    create_db_goals_scored_instance = CreateDatabase()
                    create_db_goals_scored_instance.update_goals_scored_database()
                    
                    create_db_goals_conceded_instance = CreateDatabase()
                    create_db_goals_conceded_instance.update_goals_conceded_database()
                    
                    instance_create_database_corners = CreateDatabase()
                    instance_create_database_corners.update_corners_database()
                    
                    cursor.close()
                    connection.close()
                    break
                case '2':
                    instance_create_database_corners = CreateDatabase()
                    instance_create_database_corners.update_corners_database()
                    break
                case '3':
                    create_db_goals_instance = CreateDatabase()
                    create_db_goals_instance.update_goals_database()
                    break
                case _:
                    print('INVALID OPTION!')
                    
        case '3':
            print("""Enter 1 to create goal and corners table:\nEnter 1 to create the goal table:\nEnter 2 to create the corners table:""")
            type_create = input('Select an option: ')
            
            create_db_goals_instance = CreateDatabase()
            create_db_goals_instance.create_country_league_database()
            
            match type_create:
                case '1':
                    
                    connection = DatabaseConnection.connect()
                    cursor = connection.cursor()
                    
                    create_db_goals_instance = CreateDatabase()
                    create_db_goals_instance.create_goals_total_database()
                    
                    create_db_goals_scored_instance = CreateDatabase()
                    create_db_goals_scored_instance.create_goals_scored_database()
                    
                    create_db_goals_conceded_instance = CreateDatabase()
                    create_db_goals_conceded_instance.create_goals_conceded_database()
                    
                    create_db_corners_instance = CreateDatabase()
                    create_db_corners_instance.create_corners_database()
                    
                    cursor.close()
                    connection.close()
                case '2':
                    connection = DatabaseConnection.connect()
                    cursor = connection.cursor()
                    
                    create_db_goals_instance = CreateDatabase()
                    create_db_goals_instance.create_goals_total_database()
                    
                    create_db_goals_scored_instance = CreateDatabase()
                    create_db_goals_scored_instance.create_goals_scored_database()
                    
                    create_db_goals_conceded_instance = CreateDatabase()
                    create_db_goals_conceded_instance.create_goals_conceded_database()
                    
                    cursor.close()
                    connection.close()
                case '3':   
                    create_db_corners_instance = CreateDatabase()
                    create_db_corners_instance.create_corners_database()
                case _:
                    print('INVALID OPTION!')      
            break
        
        case '4':
            db_functions_instance = DatabaseConnection()
            db_functions_instance.remove_duplicate_rows_from_database()
            
            break
                
        case _:
            print('INVALID OPTION!')