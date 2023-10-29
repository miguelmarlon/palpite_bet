import re
import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import mysql.connector

class Gols:
    def __init__(self, country,  league, quantidade_gols):
        self.country = country
        self.league = league
        self.quantidade_gols = quantidade_gols
        
        
    def cria_bd_gols(self):
                
        options= Options()
        options.add_argument('window-size=800,1200')
        options.add_argument("--lang=en-US")
        options.add_argument("--country-code=US")  
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        driver.get('https://www.adamchoi.co.uk/overs/detailed')
        sleep(1)
        
        my_list=[] 
        list_estatisticas=[]
        button_over = driver.find_element(By.XPATH, f'(//label[normalize-space()="{self.quantidade_gols}"])[1]').click()
        sleep(1)

        button_country = driver.find_element(By.XPATH, '//*[@id="country"]')
        select = Select(button_country)
        sleep(3)
        select.select_by_visible_text(self.country)
                
        button_league = driver.find_element(By.XPATH, '//*[@id="league"]')
        select = Select(button_league)
        sleep(3)
        select.select_by_visible_text(self.league)

        page_content = driver.page_source
        site= BeautifulSoup(page_content, 'html.parser')
        
        busca_times = site.find('div', attrs={'class':'row ng-scope', 'data-ng-if': '!vm.isLoading'})
        #print(busca_times.prettify())
        
        for time in busca_times.find_all('div', attrs={'data-ng-repeat': 'team in :refreshStats:vm.teams', 'class':'ng-scope'}):
            time_nome = time.find('div', attrs={'class':'col-lg-3 col-sm-6 col-xs-12 ng-binding'})
            
            if busca_times:
                match_5 = re.search(r'^(.+?)\s(?=Overall)', time_nome.text)
                if match_5:
                    time_nome = match_5.group(1).strip()  
                else:
                    raise Exception('TIME NÃO ENCONTRADO!')
            else:
                    raise Exception('Nome do time não encontrado!')
            
            gols_total = time.find('div', attrs={'class':'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            
            busca_gol_casa_fora = time.find('div', attrs={'class':'panel-body'})
            busca_gol_casa_fora = busca_gol_casa_fora.find_all('div', attrs={'col-lg-9 col-sm-6 col-xs-12'})
            
            busca_gol_casa = busca_gol_casa_fora[0]
            gols_casa = busca_gol_casa.find('div', attrs= {'class':'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            
            busca_gol_casa = busca_gol_casa_fora[1]
            gols_fora = busca_gol_casa.find('div', attrs= {'class':'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            
            list_estatisticas = [
                    time_nome,
                    gols_total,
                    gols_casa,
                    gols_fora,
                    ]
            
            my_list.append(list_estatisticas)
          
        
        conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='130889',
        database='estatisticas',
        )
        cursor = conexao.cursor()
        
        for linha in my_list:
            nome_time, total, casa, fora = linha 
            query = f'INSERT INTO gols (tipo, nome, total, casa, fora) VALUES ("{self.quantidade_gols.replace('Over ','')}", "{nome_time}", "{total}", "{casa}", "{fora}")'
            cursor.execute(query)
       
        conexao.commit()
        conexao.close()
        
        return(my_list)
    
    def atualiza_bd_gols(self):
                
        options= Options()
        options.add_argument('window-size=800,1200')
        options.add_argument("--lang=en-US")  
        options.add_argument("--country-code=US")  
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        driver.get('https://www.adamchoi.co.uk/overs/detailed')
        sleep(1)
        
        my_list=[] 
        list_estatisticas=[]
        button_over = driver.find_element(By.XPATH, f'(//label[normalize-space()="{self.quantidade_gols}"])[1]').click()
        sleep(1)

        button_country = driver.find_element(By.XPATH, '//*[@id="country"]')
        select = Select(button_country)
        sleep(3)
        select.select_by_visible_text(self.country)
                
        button_league = driver.find_element(By.XPATH, '//*[@id="league"]')
        select = Select(button_league)
        sleep(3)
        select.select_by_visible_text(self.league)

        page_content = driver.page_source
        site= BeautifulSoup(page_content, 'html.parser')
        
        busca_times = site.find('div', attrs={'class':'row ng-scope', 'data-ng-if': '!vm.isLoading'})
        
        
        for time in busca_times.find_all('div', attrs={'data-ng-repeat': 'team in :refreshStats:vm.teams', 'class':'ng-scope'}):
            time_nome = time.find('div', attrs={'class':'col-lg-3 col-sm-6 col-xs-12 ng-binding'})
            
            if busca_times:
                match_5 = re.search(r'^(.+?)\s(?=Overall)', time_nome.text)
                if match_5:
                    time_nome = match_5.group(1).strip()  
                else:
                    raise Exception('TIME NÃO ENCONTRADO!')
            else:
                    raise Exception('Nome do time não encontrado!')
                        
            gols_total = time.find('div', attrs={'class':'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            
            busca_gol_casa_fora = time.find('div', attrs={'class':'panel-body'})
            busca_gol_casa_fora = busca_gol_casa_fora.find_all('div', attrs={'col-lg-9 col-sm-6 col-xs-12'})
            
            busca_gol_casa = busca_gol_casa_fora[0]
            gols_casa = busca_gol_casa.find('div', attrs= {'class':'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            
            busca_gol_casa = busca_gol_casa_fora[1]
            gols_fora = busca_gol_casa.find('div', attrs= {'class':'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            
            list_estatisticas = [
                    time_nome,
                    gols_total,
                    gols_casa,
                    gols_fora,
                    ]
            
            my_list.append(list_estatisticas)
            
        conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='130889',
        database='estatisticas',
        )
        cursor = conexao.cursor()
        
        for linha in my_list:
            nome_time, total, casa, fora = linha 
            query = "UPDATE gols SET total = %s, casa = %s, fora = %s WHERE tipo = %s AND nome = %s"
            tipo= self.quantidade_gols.replace('Over ', '')
            valores = (total, casa, fora, tipo, nome_time)
    
            try:
                cursor.execute(query, valores)
            except mysql.connector.Error as err:
                print(f"Erro MySQL: {err}")
                conexao.rollback()
       
        conexao.commit()
        conexao.close()
        
        return(my_list)
    