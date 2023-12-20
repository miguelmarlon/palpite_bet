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
    
    country_list = [['Italy', 'Serie A',135 ], ['Italy', 'Serie B',136 ],['England', 'Premier League',39 ], ['England', 'Championship',40 ], ['England', 'League One',41], ['England', 'League Two', 42 ], 
                ['Spain', 'La Liga',140 ], ['Spain', 'Segunda Division',141 ] ,['Germany','Bundesliga',78 ],['Germany','Bundesliga 2',79],['France', 'Ligue 1',61 ],['France', 'Ligue 2',62 ],
                ['Scotland','SPL',179], ['Netherlands', 'Eredivisie',88 ], ['Netherlands', 'Eerste Divisie',89],['Portugal','Portugese Liga NOS', 94],['Turkey','Turkish Super Lig', 203],['Greece','Greek Super League',197],['Belgium','Pro League',144], ['Brazil','Serie A',71],['Brazil','Serie B',72],
                ['Austria','Bundesliga',218], ['Argentina','Primera Division',128],['Denmark', 'Superliga',119], ['USA','US MLS',253],['Norway','Norwegian Eliteserien',103],['Mexico','Liga MX',262]]
    
    
    country_list_corners = [['Italy', 'Serie A',135 ], ['Italy', 'Serie B',136 ], ['England', 'Premier League',39 ], ['England', 'Championship',40 ], ['England', 'League One',41], ['England', 'League Two', 42 ], 
                ['Spain', 'La Liga',140 ], ['Spain', 'Segunda Division',141 ] ,['Germany','Bundesliga',78 ],['Germany','Bundesliga 2',79],['France', 'Ligue 1',61 ],['France', 'Ligue 2',62 ],
                ['Scotland','SPL',179], ['Netherlands', 'Eredivisie',88 ], ['Netherlands', 'Eerste Divisie',89],['Portugal','Portugese Liga NOS', 94],['Turkey','Turkish Super Lig', 203],['Greece','Greek Super League',197],['Belgium','Pro League',144], ['Brazil','Serie A',71],
                ['Austria','Bundesliga',218], ['Argentina','Primera Division',128],['Denmark', 'Superliga',119], ['USA','US MLS',253],['Norway','Norwegian Eliteserien',103],['Mexico','Liga MX',262]]
    
    def create_country_league_database(self):
        connection = DatabaseConnection.connect()
        cursor = connection.cursor()
        for country_name in set(row[0] for row in self.country_list):
            cursor.execute("INSERT INTO country (name) VALUES (%s)", (country_name,))
        
        for league_data in self.country_list:
            country_name, league_name, api_id = league_data
            cursor.execute("""
                INSERT INTO league (name, api_id, country_id)
                VALUES (%s, %s, (SELECT country_id FROM country WHERE name = %s))
            """, (league_name, api_id, country_name))        
        connection.commit()
        connection.close()
        
    def create_goals_total_database(self):
        for goals_quantity in self.goal_total_quantities:
            for country, league, api_id in self.country_list:
                goals_instance = Goals(country, league, goals_quantity)
                data = goals_instance.create_goals_scored_conceded_table()
                print(data)
    
    def create_corners_database(self):
        
        for corner_quantity in self.corner_quantities:
            for country, league,api_id in self.country_list_corners:
                corners_instance = Corners(country, league, corner_quantity)
                data = corners_instance.create_corners_table()
                print(data)
    
    def create_goals_scored_database(self):
        
        for goals_quantity in self.goal_team_goals_quantities:
            for country, league,api_id in self.country_list:
                team_goals_instance = TeamGoals(country, league, goals_quantity)
                data = team_goals_instance.create_goals_scored_table()
                print(data)
    
    def create_goals_conceded_database(self):
        for goals_quantity in self.goal_team_goals_quantities:
            for country, league, api_id in self.country_list:
                team_goals_instance = TeamGoals(country, league, goals_quantity)
                data = team_goals_instance.create_goals_conceded_table()
                print(data)

    def update_goals_database(self):
        for goals_quantity in self.goal_total_quantities:
            for country, league, api_id in self.country_list:
                goals_instance = Goals(country, league, goals_quantity)
                data = goals_instance.update_goals_scored_conceded_table()
                print(data)
    
    def update_corners_database(self):
        for corner_quantity in self.corner_quantities:
            for country, league, api_id in self.country_list_corners:
                corners_instance = Corners(country, league, corner_quantity)
                data = corners_instance.update_corners_table()
                print(data)
    
    def update_goals_scored_database(self):
        for goals_quantity in self.goal_team_goals_quantities:
            for country, league,api_id in self.country_list:
                team_goals_instance = TeamGoals(country, league, goals_quantity)
                data = team_goals_instance.update_goals_scored_table()
                print(data)
    
    def update_goals_conceded_database(self):
        for goals_quantity in self.goal_team_goals_quantities:
            for country, league, api_id in self.country_list:
                team_goals_instance = TeamGoals(country, league, goals_quantity)
                data = team_goals_instance.update_goals_conceded_table()
                print(data)
    

