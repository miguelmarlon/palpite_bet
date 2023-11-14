from tratando_dados import tratando_dados
from dotenv import load_dotenv
import os
from create_database import database_connection
from criando_bd import criando_banco_de_dados

def search_team_by_name(cursor, team_name):
        consulta_time = "SELECT * FROM gols WHERE nome LIKE %s"
        cursor.execute(consulta_time, (f'%{team_name}%',))
        return cursor.fetchall()
    
conexao = database_connection.connect()
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
                
            for time_casa, time_fora in teams_list:    
                tratando_dados_objeto = tratando_dados(time_casa, time_fora)       
                df_gols = tratando_dados_objeto.estatistica_filtrada_gol()
                df_escanteios = tratando_dados_objeto.estatistica_filtrada_escanteios()
            exit()     
            
        case '2':
            criando_banco_de_dados_gols_obj = criando_banco_de_dados()
            criando_banco_de_dados_gols_obj.atualizando_banco_de_dados_gols()
            criando_banco_de_dados_escanteios_obj = criando_banco_de_dados()
            criando_banco_de_dados_escanteios_obj.atualizando_banco_de_dados_escanteios()
            break
            
        case '3':
            criando_banco_de_dados_gols_obj = criando_banco_de_dados()
            criando_banco_de_dados_gols_obj.criando_banco_de_dados_gols()
            criando_banco_de_dados_escanteios_obj = criando_banco_de_dados()
            criando_banco_de_dados_escanteios_obj.criando_banco_de_dados_escanteios()
            break
        
        case '4':
            criando_banco_de_dados_obj = criando_banco_de_dados()
            criando_banco_de_dados_obj.excluindo_linhas_duplicadas_no_banco_de_dados()
            
            break
                
        case _:
            print('OPÇÃO INVÁLIDA!')

