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
from db_functions import DatabaseConnection
from selenium.common.exceptions import WebDriverException, TimeoutException

class TeamGoals:
    def __init__(self, country, league, goal_quantity):
        self.country = country
        self.league = league
        self.goal_quantity = goal_quantity
                
    def create_goals_scored_table(self):
        connection_attempts = 5
        for attempt in range(connection_attempts):
            try: 
                options= Options()
                options.add_argument('window-size=800,1200')
                options.add_argument("--lang=en-US")
                options.add_argument("--country-code=US")  
                driver = webdriver.Chrome(options=options)
                wait = WebDriverWait(driver, 60)
                driver.get('https://www.adamchoi.co.uk/teamgoals/detailed')
                sleep(2)        
                my_list=[]
                statistics_list=[]
                
                country_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="country"]')))
                select = Select(country_button)
                sleep(1)
                select.select_by_visible_text(self.country)
                        
                league_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="league"]')))
                select = Select(league_button)
                sleep(1)
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
                cursor = connection.cursor(buffered=True)
                
                variable_amount_of_goals_scored =self.goal_quantity.replace('Over ','')
                float(variable_amount_of_goals_scored)
                
                for line in my_list:
                    team_name, total, home, away = line 
                    if variable_amount_of_goals_scored == '0.5':
                        type_id = 1
                    elif variable_amount_of_goals_scored == '1.5':
                        type_id = 2
                    elif variable_amount_of_goals_scored == '2.5':
                        type_id = 3
                    
                    team_id_result = DatabaseConnection.search_and_select_team_id_by_name(cursor, team_name)         
                    
                    if team_id_result:
                        team_id = team_id_result[0]
                        
                        query_check_duplicate = (
                            "SELECT 1 FROM goals_scored "
                            "WHERE team_id = %s AND type_id = %s"
                        )
                        cursor.execute(query_check_duplicate, (team_id, type_id))
                        
                        if cursor.fetchone():
                    
                            continue
                                                    
                        query = 'INSERT INTO goals_scored (team_id, type_id, total, home, away) VALUES (%s, %s, %s, %s, %s)'
                        values = (team_id, type_id, total, home, away)
                        try:
                            cursor.execute(query, values)
                        except mysql.connector.Error as err:
                            print(f"MySQL Error: {err}")
                            connection.rollback()
                    else:
                        DatabaseConnection.create_team_table(cursor, team_name, self.country, self.league)   
                        
                    team_id_result = DatabaseConnection.search_and_select_team_id_by_name(cursor, team_name)         
                    
                    if team_id_result:
                        team_id = team_id_result[0]
                        
                        query_check_duplicate = (
                            "SELECT 1 FROM goals_scored "
                            "WHERE team_id = %s AND type_id = %s"
                        )
                        cursor.execute(query_check_duplicate, (team_id, type_id))
                        
                        if cursor.fetchone():
                    
                            continue
                                                    
                        query = 'INSERT INTO goals_scored (team_id, type_id, total, home, away) VALUES (%s, %s, %s, %s, %s)'
                        values = (team_id, type_id, total, home, away)
                        try:
                            cursor.execute(query, values)
                        except mysql.connector.Error as err:
                            print(f"MySQL Error: {err}")
                            connection.rollback()
                
                connection.commit()
                connection.close()    
                return my_list
                break
            except (WebDriverException, TimeoutException) as e:
                print(f"Erro de conexão: {e}")
                print(f"Tentativa {attempt + 1} de {connection_attempts}")
                sleep(60)
            finally:
                try:
                    driver.quit()
                except:
                    pass
        else:  
            print("Falha ao conectar após várias tentativas. Saindo...")
            return None
        
    def create_goals_conceded_table(self):
        connection_attempts = 5 
        
        for attempt in range(connection_attempts):
            try:       
                options= Options()
                options.add_argument('window-size=800,1200')
                options.add_argument("--lang=en-US")
                options.add_argument("--country-code=US")  
                driver = webdriver.Chrome(options=options)
                wait = WebDriverWait(driver, 60)
                driver.get('https://www.adamchoi.co.uk/teamgoals/detailed')
                    
                my_list=[] 
                statistics_list=[]
                
                country_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="country"]')))
                select = Select(country_button)
                sleep(1)
                select.select_by_visible_text(self.country)       
                league_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="league"]')))
                select = Select(league_button)
                sleep(1)
                select.select_by_visible_text(self.league)
                
                over_button = wait.until(EC.visibility_of_element_located((By.XPATH, f"//label[@class='btn btn-sm btn-primary ng-pristine ng-untouched ng-valid ng-not-empty'][normalize-space()='{self.goal_quantity}']"))).click()
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
                cursor = connection.cursor(buffered=True)
                
                variable_amount_of_goals_conceded =self.goal_quantity.replace('Over ','')
                float(variable_amount_of_goals_conceded)
                
                for line in my_list:
                    team_name, total, home, away = line 
                    
                    if variable_amount_of_goals_conceded == '0.5':
                        type_id = 1
                    elif variable_amount_of_goals_conceded == '1.5':
                        type_id = 2
                    elif variable_amount_of_goals_conceded == '2.5':
                        type_id = 3
                    
                    team_id_result = DatabaseConnection.search_and_select_team_id_by_name(cursor, team_name)         
                    
                    if team_id_result:
                        team_id = team_id_result[0]
                        
                        query_check_duplicate = (
                            "SELECT 1 FROM goals_conceded "
                            "WHERE team_id = %s AND type_id = %s"
                        )
                        cursor.execute(query_check_duplicate, (team_id, type_id))
                        
                        if cursor.fetchone():
                    
                            continue
                                                    
                        query = 'INSERT INTO goals_conceded (team_id, type_id, total, home, away) VALUES (%s, %s, %s, %s, %s)'
                        values = (team_id, type_id, total, home, away)
                        try:
                            cursor.execute(query, values)
                        except mysql.connector.Error as err:
                            print(f"MySQL Error: {err}")
                            connection.rollback()
                    else:
                        DatabaseConnection.create_team_table(cursor, team_name, self.country, self.league)   
                        
                    team_id_result = DatabaseConnection.search_and_select_team_id_by_name(cursor, team_name)         
                    
                    if team_id_result:
                        team_id = team_id_result[0]
                        
                        query_check_duplicate = (
                            "SELECT 1 FROM goals_conceded "
                            "WHERE team_id = %s AND type_id = %s"
                        )
                        cursor.execute(query_check_duplicate, (team_id, type_id))
                        
                        if cursor.fetchone():
                    
                            continue
                                                    
                        query = 'INSERT INTO goals_conceded (team_id, type_id, total, home, away) VALUES (%s, %s, %s, %s, %s)'
                        values = (team_id, type_id, total, home, away)
                        try:
                            cursor.execute(query, values)
                        except mysql.connector.Error as err:
                            print(f"MySQL Error: {err}")
                            connection.rollback()
                
                connection.commit()
                connection.close()       
                return my_list
                
            except (WebDriverException, TimeoutException) as e:
                print(f"Connection Error: {e}")
                print(f"Attempt {attempt + 1} de {connection_attempts}")
                sleep(60)  
            finally:
                try:
                    driver.quit()
                except:
                    pass
        else:
            print("Failed to connect after multiple attempts.")
            return None

    def update_goals_scored_table(self):
        connection_attempts = 5
        for attempt in range(connection_attempts):
            try: 
                options= Options()
                options.add_argument('window-size=800,1200')
                options.add_argument("--lang=en-US")
                options.add_argument("--country-code=US")  
                driver = webdriver.Chrome(options=options)
                wait = WebDriverWait(driver, 60)
                driver.get('https://www.adamchoi.co.uk/teamgoals/detailed')
                sleep(2)        
                my_list=[]
                statistics_list=[]
                
                country_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="country"]')))
                select = Select(country_button)
                sleep(1)
                select.select_by_visible_text(self.country)
                        
                league_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="league"]')))
                select = Select(league_button)
                sleep(1)
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
                cursor = connection.cursor(buffered=True)
                
                variable_amount_of_goals_scored =self.goal_quantity.replace('Over ','')
                float(variable_amount_of_goals_scored)
                
                for line in my_list:
                    team_name, total, home, away = line 
                    if variable_amount_of_goals_scored == '0.5':
                        type_id = 1
                    elif variable_amount_of_goals_scored == '1.5':
                        type_id = 2
                    elif variable_amount_of_goals_scored == '2.5':
                        type_id = 3
                    
                    team_id_result = DatabaseConnection.search_and_select_team_id_by_name(cursor, team_name)         
                    
                    if team_id_result:
                        team_id = team_id_result[0]
                                                                                                    
                        query = 'UPDATE goals_scored SET total = %s, home = %s, away = %s WHERE team_id = %s AND type_id = %s'
                        values = ( total, home, away,team_id, type_id)
                        try:
                            cursor.execute(query, values)
                        except mysql.connector.Error as err:
                            print(f"MySQL Error: {err}")
                            connection.rollback()
                    else:
                        DatabaseConnection.create_team_table(cursor, team_name, self.country, self.league)   
                        
                    team_id_result = DatabaseConnection.search_and_select_team_id_by_name(cursor, team_name)         
                    
                    if team_id_result:
                        team_id = team_id_result[0]
                                                                                                   
                        query = 'UPDATE goals_scored SET total = %s, home = %s, away = %s WHERE team_id = %s AND type_id = %s'
                        values = ( total, home, away,team_id, type_id)
                        try:
                            cursor.execute(query, values)
                        except mysql.connector.Error as err:
                            print(f"MySQL Error: {err}")
                            connection.rollback()
                
                connection.commit()
                connection.close()    
                return my_list
                
            except (WebDriverException, TimeoutException) as e:
                print(f"Erro de conexão: {e}")
                print(f"Tentativa {attempt + 1} de {connection_attempts}")
                sleep(60)
            finally:
                try:
                    driver.quit()
                except:
                    pass
        else:  
            print("Falha ao conectar após várias tentativas. Saindo...")
            return None
    
    def update_goals_conceded_table(self):
        connection_attempts = 5 
        
        for attempt in range(connection_attempts):
            try:       
                options= Options()
                options.add_argument('window-size=800,1200')
                options.add_argument("--lang=en-US")
                options.add_argument("--country-code=US")  
                driver = webdriver.Chrome(options=options)
                wait = WebDriverWait(driver, 60)
                driver.get('https://www.adamchoi.co.uk/teamgoals/detailed')
                    
                my_list=[] 
                statistics_list=[]
                
                country_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="country"]')))
                select = Select(country_button)
                sleep(1)
                select.select_by_visible_text(self.country)       
                league_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="league"]')))
                select = Select(league_button)
                sleep(1)
                select.select_by_visible_text(self.league)
                
                over_button = wait.until(EC.visibility_of_element_located((By.XPATH, f"//label[@class='btn btn-sm btn-primary ng-pristine ng-untouched ng-valid ng-not-empty'][normalize-space()='{self.goal_quantity}']"))).click()
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
                cursor = connection.cursor(buffered=True)
                
                variable_amount_of_goals_conceded =self.goal_quantity.replace('Over ','')
                float(variable_amount_of_goals_conceded)
                
                for line in my_list:
                    team_name, total, home, away = line 
                    
                    if variable_amount_of_goals_conceded == '0.5':
                        type_id = 1
                    elif variable_amount_of_goals_conceded == '1.5':
                        type_id = 2
                    elif variable_amount_of_goals_conceded == '2.5':
                        type_id = 3
                    
                    team_id_result = DatabaseConnection.search_and_select_team_id_by_name(cursor, team_name)         
                    
                    if team_id_result:
                        team_id = team_id_result[0]
                                                                                                    
                        query = 'UPDATE goals_conceded SET total = %s, home = %s, away = %s WHERE team_id = %s AND type_id = %s'
                        values = (total, home, away, team_id, type_id)
                        try:
                            cursor.execute(query, values)
                        except mysql.connector.Error as err:
                            print(f"MySQL Error: {err}")
                            connection.rollback()
                    else:
                        DatabaseConnection.create_team_table(cursor, team_name, self.country, self.league)   
                        
                    team_id_result = DatabaseConnection.search_and_select_team_id_by_name(cursor, team_name)         
                    
                    if team_id_result:
                        team_id = team_id_result[0]
                                                                                                    
                        query = 'UPDATE goals_conceded SET total = %s, home = %s, away = %s WHERE team_id = %s AND type_id = %s'
                        values = ( total, home, away,team_id, type_id,)
                        try:
                            cursor.execute(query, values)
                        except mysql.connector.Error as err:
                            print(f"MySQL Error: {err}")
                            connection.rollback()
                
                connection.commit()
                connection.close()       
                return my_list
                
            except (WebDriverException, TimeoutException) as e:
                print(f"Connection Error: {e}")
                print(f"Attempt {attempt + 1} de {connection_attempts}")
                sleep(60)  
            finally:
                try:
                    driver.quit()
                except:
                    pass
        else:
            print("Failed to connect after multiple attempts.")
            return None