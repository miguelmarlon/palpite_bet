from scraping_corners import Corners
from scraping_team_goals_total import Goals
import mysql.connector
from dotenv import load_dotenv
import os
from database_connection import DatabaseConnection
from scraping_team_goals import TeamGoals
  
class CreateDatabase:
    goal_team_goals_quantities = ['Over 0.5', 'Over 1.5', 'Over 2.5']
    goal_total_quantities = ['Over 1.5', 'Over 2.5', 'Over 3.5']
    corner_quantities = ['7.5', '8.5', '10.5', '11.5', '12.5']

    country_list = [['Italy', 'Serie A'], ['Italy', 'Serie B'], ['England', 'Premier League'], ['England', 'Championship'], ['England', 'League One'], ['England', 'League Two'], 
                ['England', 'National League'], ['Spain', 'La Liga'], ['Spain', 'Segunda Division'] ,['Germany','Bundesliga'],['Germany','Bundesliga 2'],['France', 'Ligue 1'],['France', 'Ligue 2'],
                ['Scotland','SPL'], ['Scotland','Scottish Championship'], ['Netherlands', 'Eredivisie'], ['Netherlands', 'Eerste Divisie'], 
                ['Portugal','Portugese Liga NOS'],['Turkey','Turkish Super Lig'],['Greece','Greek Super League'],['Belgium','Pro League'], ['Belgium','First Division B'], ['Brazil','Serie A'],['Brazil','Serie B'],
                ['Austria','Bundesliga'],['Russia','Premier League'],['Argentina','Primera Division'],['Denmark', 'Superliga'],['Poland','Ekstraklasa'],['USA','US MLS'],
                ['Norway','Norwegian Eliteserien'],['Sweden','Swedish Allsvenskan'],['Switzerland','Swiss Super League'],['Australia','A League'],['Japan','J League'],
                ['China','Super League'],['Mexico','Liga MX'],['Czechia','Czech Liga'],['Saudi Arabia','Saudi Pro League'],['Finland','Finnish Veikkausliiga']]
    
     
                # ['Finland','Finnish Veikkausliiga'] não tem essa liga para corners 
    country_list_corners = [['Italy', 'Serie A'],['Italy', 'Serie B'],['England', 'Premier League'],['England', 'Championship'],['England', 'League One'],['England', 'League Two'],['England', 'National League'],['Spain', 'La Liga'],['Spain', 'Segunda Division'],
                            ['Germany','Bundesliga'],['Germany','Bundesliga 2'],['France', 'Ligue 1'],['France', 'Ligue 2'],['Scotland','SPL'],['Scotland','Scottish Championship'],['Scotland','Scottish League 1'],['Scotland','Scottish League 2'],
                            ['Netherlands', 'Eredivisie'],['Netherlands', 'Eerste Divisie'],['Portugal','Portugese Liga NOS'],['Turkey','Turkish Super Lig'],['Greece','Greek Super League'],['Belgium','Pro League'],
                            ['Brazil','Serie A'],['Austria','Bundesliga'],['Russia','Premier League'],['Argentina','Primera Division'],['Denmark', 'Superliga'],['Poland','Ekstraklasa'],
                            ['USA','US MLS'],['Norway','Norwegian Eliteserien'],['Sweden','Swedish Allsvenskan'],['Switzerland','Swiss Super League'],['Australia','A League'],['Japan','J League'],
                            ['China','Super League'],['Mexico','Liga MX'],['Czechia','Czech Liga'],['Saudi Arabia','Saudi Pro League']]                   
    
    def create_goals_total_database(self):
        for goals_quantity in self.goal_total_quantities:
            for country, league in self.country_list:
                goals_instance = Goals(country, league, goals_quantity)
                data = goals_instance.create_goals_database()
                print(data)
    
    def create_corners_database(self):
        for corner_quantity in self.corner_quantities:
            for country, league in self.country_list_corners:
                corners_instance = Corners(country, league, corner_quantity)
                data = corners_instance.create_corners_database()
                print(data)
    
    def create_goals_scored_database(self):
        for goals_quantity in self.goal_team_goals_quantities:
            for country, league in self.country_list:
                team_goals_instance = TeamGoals(country, league, goals_quantity)
                data = team_goals_instance.create_goals_scored_database()
                print(data)
    
    def create_goals_conceded_database(self):
        for goals_quantity in self.goal_team_goals_quantities:
            for country, league in self.country_list:
                team_goals_instance = TeamGoals(country, league, goals_quantity)
                data = team_goals_instance.create_goals_conceded_database()
                print(data)

    def update_goals_database(self):
        for goals_quantity in self.goal_total_quantities:
            for country, league in self.country_list:
                goals_instance = Goals(country, league, goals_quantity)
                data = goals_instance.update_goals_database()
                print(data)
    
    def update_corners_database(self):
        for corner_quantity in self.corner_quantities:
            for country, league in self.country_list_corners:
                corners_instance = Corners(country, league, corner_quantity)
                data = corners_instance.update_corners_database()
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
    

