import re
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import mysql.connector
from database_connection import DatabaseConnection

class Goals:
    def __init__(self, country, league, goal_quantity, api_team_id):
        self.country = country
        self.league = league
        self.goal_quantity = goal_quantity
        self.api_team_id = api_team_id
        
    def create_goals_table(self):
                
        options= Options()
        options.add_argument('window-size=800,1200')
        options.add_argument("--lang=en-US")
        options.add_argument("--country-code=US")  
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        driver.get('https://www.adamchoi.co.uk/overs/detailed')
        sleep(2)        
        my_list=[] 
        statistics_list=[]
        
        country_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="country"]')))
        select = Select(country_button)
        select.select_by_visible_text(self.country)
                
        league_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="league"]')))
        select = Select(league_button)
        select.select_by_visible_text(self.league)
        
        over_button = wait.until(EC.visibility_of_element_located((By.XPATH, f'(//label[normalize-space()="{self.goal_quantity}"])[1]'))).click()
        sleep(2)
        
        page_content = driver.page_source
        site= BeautifulSoup(page_content, 'html.parser')
        
        teams_section = site.find('div', attrs={'class':'row ng-scope', 'data-ng-if': '!vm.isLoading'})
                
        for team in teams_section.find_all('div', attrs={'data-ng-repeat': 'team in :refreshStats:vm.teams', 'class':'ng-scope'}):
            team_name_element = team.find('div', attrs={'class':'col-lg-3 col-sm-6 col-xs-12 ng-binding'})
            
            if teams_section:
                match_5 = re.search(r'^(.+?)\s(?=Overall)', team_name_element.text)
                if match_5:
                    team_name = match_5.group(1).strip() 
                else:
                    raise Exception('TIME NÃO ENCONTRADO!')
            else:
                    raise Exception('Nome do time não encontrado!')
            
            total_goals = team.find('div', attrs={'class':'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            
            goals_home_away_section = team.find('div', attrs={'class':'panel-body'})
            goals_home_away = goals_home_away_section.find_all('div', attrs={'col-lg-9 col-sm-6 col-xs-12'})
            
            goals_home = goals_home_away[0]
            home_goals = goals_home.find('div', attrs= {'class':'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            
            goals_away = goals_home_away[1]
            away_goals = goals_away.find('div', attrs= {'class':'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            
            statistics_list = [
                team_name,
                total_goals,
                home_goals,
                away_goals,
                ]
            
            my_list.append(statistics_list)
          
        connection = DatabaseConnection.connect()
        cursor = connection.cursor()
        
        self.goal_quantity.replace('Over ','')
        ###testar essas linhas!!!!!        
        for line in my_list:                        
            if self.goal_quantity == '1.5':
                type_id = 2
            elif self.goal_quantity == '2.5':
                type_id = 3        
            elif self.goal_quantity == '3.5':
                type_id = 4  
                                        
            team_name, total, home, away = line 
            query = f"SELECT country_id FROM country WHERE name = {self.country} "           
            cursor.execute(query)            
            country_id = cursor.fetchone()
            
            query = f"SELECT leaague_id FROM league WHERE country_id = {country_id} AND name = '{self.league}"           
            cursor.execute(query)            
            league_id = cursor.fetchone()
            
            query = 'INSERT INTO team (name, api_id, league_id) VALUES (%s, %s, %s)'
            values = (team_name, self.api_team_id, league_id)
            try:
                cursor.execute(query, values)
            except mysql.connector.Error as err:
                print(f"MySQL Error: {err}")
                connection.rollback()
            
            query = f"SELECT team_id FROM team WHERE name = {team_name}"           
            cursor.execute(query)            
            team_id = cursor.fetchone()
                                               
            query = 'INSERT INTO goals_scored_conceded (team_ai,type_id, total, home, away) VALUES (%s, %s, %s, %s, %s)'
            values = (team_id, type_id, total, home, away)
            try:
                cursor.execute(query, values)
            except mysql.connector.Error as err:
                print(f"MySQL Error: {err}")
                connection.rollback()
        
        connection.commit()
        connection.close()
               
        return my_list
    
    def update_goals_table(self):
                
        options= Options()
        options.add_argument('window-size=800,1200')
        options.add_argument("--lang=en-US")  
        options.add_argument("--country-code=US")  
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 30)
        driver.get('https://www.adamchoi.co.uk/overs/detailed')
                
        my_list=[] 
        statistics_list =[]
       
        country_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="country"]')))
        select = Select(country_button)
        select.select_by_visible_text(self.country)
        sleep(2)        
        league_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="league"]')))
        select = Select(league_button)
        select.select_by_visible_text(self.league)
        sleep(2)
        button_over = wait.until(EC.visibility_of_element_located((By.XPATH, f'(//label[normalize-space()="{self.goal_quantity}"])[1]'))).click()
        sleep(2)

        page_content = driver.page_source
        site= BeautifulSoup(page_content, 'html.parser')
        
        teams_section = site.find('div', attrs={'class':'row ng-scope', 'data-ng-if': '!vm.isLoading'})
                
        for team in teams_section.find_all('div', attrs={'data-ng-repeat': 'team in :refreshStats:vm.teams', 'class':'ng-scope'}):
            team_name_element = team.find('div', attrs={'class':'col-lg-3 col-sm-6 col-xs-12 ng-binding'})
            
            if teams_section:
                match_5 = re.search(r'^(.+?)\s(?=Overall)', team_name_element.text)
                if match_5:
                    team_name = match_5.group(1).strip()  
                else:
                    raise Exception('TIME NÃO ENCONTRADO!')
            else:
                    raise Exception('Nome do time não encontrado!')
                        
            total_goals = team.find('div', attrs={'class':'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            
            goals_home_away_section = team.find('div', attrs={'class':'panel-body'})
            goals_home_away = goals_home_away_section.find_all('div', attrs={'col-lg-9 col-sm-6 col-xs-12'})
            
            goals_home = goals_home_away[0]
            home_goals = goals_home.find('div', attrs={'class':'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            
            goals_away = goals_home_away[1]
            away_goals = goals_away.find('div', attrs={'class':'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            
            statistics_list = [
                    team_name,
                    total_goals,
                    home_goals,
                    away_goals,
                ]
            
            my_list.append(statistics_list)
            
        connection = DatabaseConnection.connect()
        cursor = connection.cursor()
           
        for linha in my_list:
            team_name, total, home, away = linha 
            query = "UPDATE goals SET total = %s, home = %s, away = %s WHERE type = %s AND name = %s"
            type= self.goal_quantity.replace('Over ', '')
            valores = (total, home, away, type, team_name)
    
            try:
                cursor.execute(query, valores)
            except mysql.connector.Error as err:
                print(f"Erro MySQL: {err}")
                connection.rollback()
       
        connection.commit()
        connection.close()
        
        return(my_list)
    