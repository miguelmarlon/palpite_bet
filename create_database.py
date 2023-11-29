from scraping_corners import Corners
from scraping_team_goals_total import Goals
import mysql.connector
from dotenv import load_dotenv
import os
from db_functions import DatabaseConnection
from scraping_team_goals import TeamGoals
  
class CreateDatabase:
    goal_team_goals_quantities = ['Over 0.5', 'Over 1.5', 'Over 2.5']
    goal_total_quantities = ['Over 1.5', 'Over 2.5', 'Over 3.5']
    corner_quantities = ['7.5', '8.5','9.5', '10.5', '11.5', '12.5']

    #pegar as informações do banco de dados
    country_list = [['Italy', 'Serie A',135 ], ['Italy', 'Serie B',136 ], ['England', 'Premier League',39 ], ['England', 'Championship',40 ], ['England', 'League One',41], ['England', 'League Two', 42 ], 
                ['Spain', 'La Liga',140 ], ['Spain', 'Segunda Division',141 ] ,['Germany','Bundesliga',78 ],['Germany','Bundesliga 2',79],['France', 'Ligue 1',61 ],['France', 'Ligue 2',62 ],
                ['Scotland','SPL',179], ['Netherlands', 'Eredivisie',88 ], ['Netherlands', 'Eerste Divisie',89], 
                ['Portugal','Portugese Liga NOS', 94],['Turkey','Turkish Super Lig', 203],['Greece','Greek Super League',197],['Belgium','Pro League',144], ['Brazil','Serie A',71],['Brazil','Serie B',72],
                ['Austria','Bundesliga',218], ['Argentina','Primera Division',128],['Denmark', 'Superliga',119], ['USA','US MLS',253],
                ['Norway','Norwegian Eliteserien',103],['Switzerland','Swiss Super League',207],['Mexico','Liga MX',262]]
                        
    def create_goals_total_database(self):
        for goals_quantity in self.goal_total_quantities:
            for country, league, api_id in self.country_list:
                goals_instance = Goals(country, league, goals_quantity, api_id)
                data = goals_instance.create_goals_scored_conceded_table()
                print(data)
    
    def create_corners_database(self):
        for corner_quantity in self.corner_quantities:
            for country, league,api_id in self.country_list:
                corners_instance = Corners(country, league, corner_quantity, api_id)
                data = corners_instance.create_corners_table()
                print(data)
    
    def create_goals_scored_database(self):
        for goals_quantity in self.goal_team_goals_quantities:
            for country, league,api_id in self.country_list:
                team_goals_instance = TeamGoals(country, league, goals_quantity, api_id)
                data = team_goals_instance.create_goals_scored_table()
                print(data)
    
    def create_goals_conceded_database(self):
        for goals_quantity in self.goal_team_goals_quantities:
            for country, league, api_id in self.country_list:
                team_goals_instance = TeamGoals(country, league, goals_quantity, api_id)
                data = team_goals_instance.create_goals_conceded_table()
                print(data)

    def update_goals_database(self):
        for goals_quantity in self.goal_total_quantities:
            for country, league, api_id in self.country_list:
                goals_instance = Goals(country, league, goals_quantity,api_id)
                data = goals_instance.update_goals_scored_conceded_table()
                print(data)
    
    def update_corners_database(self):
        for corner_quantity in self.corner_quantities:
            for country, league, api_id in self.country_list:
                corners_instance = Corners(country, league, corner_quantity, api_id)
                data = corners_instance.update_corners_table()
                print(data)
    
    def remove_duplicate_rows_from_database(self):
        connection = DatabaseConnection.connect()
        cursor = connection.cursor()

        try:            
            create_temporary_goals_table_query = """
            CREATE TABLE gols_temp AS
            SELECT DISTINCT id, tipo, nome, total, casa, fora
            FROM gols
            """
            cursor.execute(create_temporary_goals_table_query)
            drop_original_goals_table_query = "DROP TABLE gols"
            cursor.execute(drop_original_goals_table_query)
            
            rename_goals_table_query = "RENAME TABLE gols_temp TO gols"
            cursor.execute(rename_goals_table_query)

            connection.commit()
            print("Duplicate rows from 'goals' table successfully removed!")
            
            create_temporary_corners_table_query  = """
            CREATE TABLE escanteios_temp AS
            SELECT DISTINCT id, tipo, nome, total, casa, fora
            FROM escanteios
            """
            cursor.execute(create_temporary_corners_table_query )
            drop_original_corners_table_query = "DROP TABLE escanteios"
            cursor.execute(drop_original_corners_table_query)
            
            rename_corners_table_query = "RENAME TABLE escanteios_temp TO escanteios"
            cursor.execute(rename_corners_table_query)

            connection.commit()
            print("Linhas duplicadas da tabela escanteios excluídas com sucesso!")

        except mysql.connector.Error as e:
            connection.rollback()
            print(f"Erro ao excluir linhas duplicadas: {e}")

        finally:
            cursor.close()
            connection.close()
    

