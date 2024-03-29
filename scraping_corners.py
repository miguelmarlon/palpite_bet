import re
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from db_functions import DatabaseConnection
import mysql.connector
from selenium.common.exceptions import WebDriverException, TimeoutException

class Corners:
    
    def __init__(self, country, league, corner_quantity):
        self.country = country
        self.league = league
        self.corner_quantity = corner_quantity

    def create_corners_table(self):
        connection_attempts = 5

        for attempt in range(connection_attempts):
            try:
                my_list = []
                team_list = []

                options = Options()
                options.add_argument('window-size=800,1200')

                driver = webdriver.Chrome(options=options)
                wait = WebDriverWait(driver, 60)
                driver.get('https://www.adamchoi.co.uk/corners/detailed')

                league_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="country"]')))
                select = Select(league_button)
                
                select.select_by_visible_text(self.country)

                league_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="league"]')))
                select = Select(league_button)
                
                select.select_by_visible_text(self.league)

                select_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div/div[3]/div/div[2]/div/select')))
                select = Select(select_element)
                
                select.select_by_visible_text(self.corner_quantity)
                sleep(2)

                page_content = driver.page_source
                site = BeautifulSoup(page_content, 'html.parser')

                team_search = site.find('div', attrs={'class': 'row ng-scope', 'data-ng-if': '!vm.isLoading'})
                teams = team_search.find_all('div', attrs={'data-ng-repeat': 'team in :refreshStats:vm.teams', 'class': 'ng-scope'})

                for team in teams:
                    team_name_div = team.find('div', attrs={'class': 'col-lg-3 col-sm-6 col-xs-12 ng-binding'})

                    if team_name_div:
                        match_5 = re.search(r'^(.+?)\s(?=Overall)', team_name_div.text)
                        if match_5:
                            team_name = match_5.group(1).strip()
                        else:
                            raise Exception('TEAM NOT FOUND!')
                    else:
                        raise Exception('Team name not found!')

                    corners_search = team.find('div', attrs={'class': 'progress'})

                    total_corners_div = corners_search.find('div', attrs={'class': 'progress-bar progress-bar-success ng-binding'})
                    total_corners = total_corners_div.text.replace('%', '')
                    total_corners_div = corners_search.find('div', attrs={'class': 'progress-bar progress-bar-danger ng-binding'})

                    if total_corners != '':
                        total_corners = float(total_corners)
                    else:
                        total_corners = None

                    corners_home_away_search = team.find('div', attrs={'class': 'panel-body'})
                    corners_home_away_search = corners_home_away_search.find_all('div', attrs={'class': 'col-lg-9 col-sm-6 col-xs-12'})

                    corners_home_div = corners_home_away_search[0]
                    home_corners = corners_home_div.find('div', attrs={'class': 'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')

                    if home_corners != '':
                        home_corners = float(home_corners)
                    else:
                        home_corners = None

                    corners_away_div = corners_home_away_search[1]
                    away_corners = corners_away_div.find('div', attrs={'class': 'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')

                    if away_corners != '':
                        away_corners = float(away_corners)
                    else:
                        away_corners = 0

                    team_list = [
                        team_name,
                        total_corners,
                        home_corners,
                        away_corners,
                    ]

                    my_list.append(team_list)

                connection = DatabaseConnection.connect()
                cursor = connection.cursor(buffered=True)
                variable_amount_corners = float(self.corner_quantity)

                for line in my_list:
                    team_name, total, home, away = line
                    print(team_name, total, home, away)
                    
                    if variable_amount_corners == 7.5:
                        type_id = 1
                    elif variable_amount_corners == 8.5:
                        type_id = 2       
                    elif variable_amount_corners == 9.5:
                        type_id = 3 
                    elif variable_amount_corners == 10.5:
                        type_id = 4
                    elif variable_amount_corners == 11.5:
                        type_id = 5 
                    elif variable_amount_corners == 12.5:
                        type_id = 6 
                    
                    team_id_result = DatabaseConnection.search_and_select_team_id_by_name(cursor, team_name)
                    if team_id_result:
                        team_id = team_id_result[0]
                        query_check_duplicate = (
                            "SELECT 1 FROM corners "
                            "WHERE team_id = %s AND type_id = %s"
                        )
                        cursor.execute(query_check_duplicate, (team_id, type_id))
                        
                        if cursor.fetchone():
                            continue
                                                    
                        query = 'INSERT INTO corners (team_id, type_id, total, home, away) VALUES (%s, %s, %s, %s, %s)'
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
                            "SELECT 1 FROM corners "
                            "WHERE team_id = %s AND type_id = %s"
                        )
                        cursor.execute(query_check_duplicate, (team_id, type_id))
                        
                        if cursor.fetchone():
                            continue
                                                    
                        query = 'INSERT INTO corners (team_id, type_id, total, home, away) VALUES (%s, %s, %s, %s, %s)'
                        values = (team_id, type_id, total, home, away)
                        try:
                            cursor.execute(query, values)
                        except mysql.connector.Error as err:
                            print(f"MySQL Error: {err}")
                            connection.rollback()
                    else:
                        print('Id não encontrado')        
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
        
    def update_corners_table(self):
        connection_attempts = 5  

        for attempt in range(connection_attempts):
            try:
                my_list = []
                team_list = []

                options = Options()
                options.add_argument('window-size=800,1200')

                driver = webdriver.Chrome(options=options)
                wait = WebDriverWait(driver, 60)
                driver.get('https://www.adamchoi.co.uk/corners/detailed')

                country_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="country"]')))
                select = Select(country_button)
                select.select_by_visible_text(self.country)

                league_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="league"]')))
                select = Select(league_button)
                select.select_by_visible_text(self.league)

                select_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div/div[3]/div/div[2]/div/select')))
                select = Select(select_element)
                select.select_by_visible_text(self.corner_quantity)
                sleep(2)

                page_content = driver.page_source
                site = BeautifulSoup(page_content, 'html.parser')

                team_search = site.find('div', attrs={'class': 'row ng-scope', 'data-ng-if': '!vm.isLoading'})
                teams = team_search.find_all('div', attrs={'data-ng-repeat': 'team in :refreshStats:vm.teams', 'class': 'ng-scope'})

                for team in teams:
                    team_name_div = team.find('div', attrs={'class': 'col-lg-3 col-sm-6 col-xs-12 ng-binding'})

                    if team_name_div:
                        match_5 = re.search(r'^(.+?)\s(?=Overall)', team_name_div.text)
                        if match_5:
                            team_name = match_5.group(1).strip()
                        else:
                            raise Exception('TEAM NOT FOUND!')
                    else:
                        raise Exception('Team name not found!')

                    corners_search = team.find('div', attrs={'class': 'progress'})

                    total_corners_div = corners_search.find('div', attrs={'class': 'progress-bar progress-bar-success ng-binding'})
                    total_corners = total_corners_div.text.replace('%', '')
                    total_corners_div = corners_search.find('div', attrs={'class': 'progress-bar progress-bar-danger ng-binding'})

                    if total_corners != '':
                        total_corners = float(total_corners)
                    else:
                        total_corners = None

                    corners_home_away_search = team.find('div', attrs={'class': 'panel-body'})
                    corners_home_away_search = corners_home_away_search.find_all('div', attrs={'class': 'col-lg-9 col-sm-6 col-xs-12'})

                    corners_home_div = corners_home_away_search[0]
                    home_corners = corners_home_div.find('div', attrs={'class': 'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')

                    if home_corners != '':
                        home_corners = float(home_corners)
                    else:
                        home_corners = None

                    corners_away_div = corners_home_away_search[1]
                    away_corners = corners_away_div.find('div', attrs={'class': 'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')

                    if away_corners != '':
                        away_corners = float(away_corners)
                    else:
                        away_corners = 0

                    team_list = [
                        team_name,
                        total_corners,
                        home_corners,
                        away_corners,
                    ]

                    my_list.append(team_list)

                connection = DatabaseConnection.connect()
                cursor = connection.cursor()

                variable_amount_corners = float(self.corner_quantity)
                
                for line in my_list:
                    team_name, total, home, away = line
                    
                    for linha in my_list:
                        team_name, total, home, away = linha
                        
                        if variable_amount_corners == 7.5:
                            type_id = 1
                        elif variable_amount_corners == 8.5:
                            type_id = 2       
                        elif variable_amount_corners == 9.5:
                            type_id = 3 
                        elif variable_amount_corners == 10.5:
                            type_id = 4
                        elif variable_amount_corners == 11.5:
                            type_id = 5 
                        elif variable_amount_corners == 12.5:
                            type_id = 6 
                                    
                        team_id_result = DatabaseConnection.search_and_select_team_id_by_name(cursor, team_name)
                        
                        if team_id_result:
                            team_id = team_id_result[0]
                            query_update = "UPDATE corners SET total = %s, home = %s, away = %s WHERE team_id = %s AND type_id = %s"
                            
                            values = (total, home, away, team_id, type_id)
                    
                            try:
                                cursor.execute(query_update, values)
                            except mysql.connector.Error as err:
                                print(f"Erro MySQL: {err}")
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