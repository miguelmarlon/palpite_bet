import re
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from create_database import database_connection
import mysql.connector

class Escanteios:
    
    def __init__(self, pais, liga, quantidade_escanteios):
        self.pais = pais
        self.liga = liga
        self.quantidade_escanteios= quantidade_escanteios
        
    def cria_bd_escanteios(self):  
        
        my_list= []
        lista_times=[]
        
        options= Options()
        options.add_argument('window-size=800,1200')   

        navegador = webdriver.Chrome(options=options)
        wait = WebDriverWait(navegador, 10)
        navegador.get('https://www.adamchoi.co.uk/corners/detailed')

        button_league = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="country"]')))
        select = Select(button_league)
        select.select_by_visible_text(self.pais)
        
        button_league = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="league"]')))
        select = Select(button_league)
        select.select_by_visible_text(self.liga)
                
        select_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div/div[3]/div/div[2]/div/select')))
        select = Select(select_element)
        select.select_by_visible_text(self.quantidade_escanteios)
        sleep(3)

        page_content = navegador.page_source
        site= BeautifulSoup(page_content, 'html.parser')

        busca_times = site.find('div', attrs={'class':'row ng-scope', 'data-ng-if': '!vm.isLoading'})
        times = busca_times.find_all('div', attrs={'data-ng-repeat': 'team in :refreshStats:vm.teams', 'class':'ng-scope'})
        
        for time in times:
            time_nome = time.find('div', attrs={'class':'col-lg-3 col-sm-6 col-xs-12 ng-binding'})
                        
            if time_nome:
                match_5 = re.search(r'^(.+?)\s(?=Overall)', time_nome.text)
                if match_5:
                    time_nome = match_5.group(1).strip()
                else:
                    raise Exception('TIME NÃO ENCONTRADO!')
            else:
                raise Exception('Nome do time não encontrado!')
                        
            busca_escanteios = time.find('div', attrs={'class': 'progress'})
                
            busca_total_escanteios = busca_escanteios.find('div', attrs={'class':'progress-bar progress-bar-success ng-binding'})
            total_escanteios = busca_total_escanteios.text.replace('%', '')
            busca_total_escanteios = busca_escanteios.find('div', attrs={'class': 'progress-bar progress-bar-danger ng-binding'})
                     
            if total_escanteios != '':
                total_escanteios = float(total_escanteios)
            else:
                total_escanteios = None  
            
            busca_escanteios_home_away = time.find('div', attrs={'class': 'panel-body'})
            busca_escanteios_home_away = busca_escanteios_home_away.find_all('div', attrs={'class': 'col-lg-9 col-sm-6 col-xs-12'})
            
            busca_escanteios_home = busca_escanteios_home_away[0]
            escanteios_casa = busca_escanteios_home.find('div', attrs={'class': 'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
                
            if escanteios_casa != '':
                escanteios_casa = float(escanteios_casa)
            else:
                escanteios_casa = None
                        
            busca_escanteios_casa = busca_escanteios_home_away[1]
            escanteios_fora = busca_escanteios_casa.find('div', attrs={'class': 'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
                   
            if escanteios_fora != '':
                escanteios_fora = float(escanteios_fora)
            else:
                escanteios_fora = 0      
            
            lista_times = [
            time_nome,
            total_escanteios,
            escanteios_casa,
            escanteios_fora,
            ]
            
            my_list.append(lista_times)
        
        conexao = database_connection.connect()
        cursor = conexao.cursor()
        
        for linha in my_list:
            nome_time, total, casa, fora = linha 
            query = 'INSERT INTO escanteios (tipo, nome, total, casa, fora, pais, liga) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            values = (self.quantidade_escanteios, nome_time, total, casa, fora, self.pais, self.liga)
            cursor.execute(query, values)
       
        conexao.commit()
        conexao.close()
        
        return(my_list)
    
    def atualiza_bd_escanteios(self):  
        
        my_list= []
        lista_times=[]
        
        options= Options()
        options.add_argument('window-size=800,1200')    

        navegador = webdriver.Chrome(options=options)
        wait = WebDriverWait(navegador, 20)
        navegador.get('https://www.adamchoi.co.uk/corners/detailed')

        button_pais = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="country"]')))
        select = Select(button_pais)
        select.select_by_visible_text(self.pais)
        
        button_league = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="league"]')))
        select = Select(button_league)
        select.select_by_visible_text(self.liga)
                
        select_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div/div[3]/div/div[2]/div/select')))
        select = Select(select_element)
        select.select_by_visible_text(self.quantidade_escanteios)
        sleep(2)
        
        page_content = navegador.page_source
        site= BeautifulSoup(page_content, 'html.parser')

        busca_times = site.find('div', attrs={'class':'row ng-scope', 'data-ng-if': '!vm.isLoading'})
        times = busca_times.find_all('div', attrs={'data-ng-repeat': 'team in :refreshStats:vm.teams', 'class':'ng-scope'})
        for time in times:
            time_nome = time.find('div', attrs={'class':'col-lg-3 col-sm-6 col-xs-12 ng-binding'})
                        
            if time_nome:
                match_5 = re.search(r'^(.+?)\s(?=Overall)', time_nome.text)
                if match_5:
                     
                    time_nome = match_5.group(1).strip()
                else:
                    raise Exception('TIME NÃO ENCONTRADO!')
            else:
                raise Exception('Nome do time não encontrado!')
                        
            busca_escanteios = time.find('div', attrs={'class': 'progress'})
                
            busca_total_escanteios = busca_escanteios.find('div', attrs={'class':'progress-bar progress-bar-success ng-binding'})
            total_escanteios = busca_total_escanteios.text.replace('%', '')
            busca_total_escanteios = busca_escanteios.find('div', attrs={'class': 'progress-bar progress-bar-danger ng-binding'})
                     
            if total_escanteios != '':
                total_escanteios = float(total_escanteios)
            else:
                total_escanteios = None  
            
            busca_escanteios_home_away = time.find('div', attrs={'class': 'panel-body'})
            busca_escanteios_home_away = busca_escanteios_home_away.find_all('div', attrs={'class': 'col-lg-9 col-sm-6 col-xs-12'})
            
            busca_escanteios_home = busca_escanteios_home_away[0]
            escanteios_casa = busca_escanteios_home.find('div', attrs={'class': 'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
                
            if escanteios_casa != '':
                escanteios_casa = float(escanteios_casa)
            else:
                escanteios_casa = None
                        
            busca_escanteios_casa = busca_escanteios_home_away[1]
            escanteios_fora = busca_escanteios_casa.find('div', attrs={'class': 'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
                   
            if escanteios_fora != '':
                escanteios_fora = float(escanteios_fora)
            else:
                escanteios_fora = 0                 
            
            lista_times = [
            time_nome,
            total_escanteios,
            escanteios_casa,
            escanteios_fora,
            ]
            
            my_list.append(lista_times)
        
        conexao = database_connection.connect()
        cursor = conexao.cursor()
        
        for linha in my_list:
            nome_time, total, casa, fora = linha 
            query = "UPDATE escanteios SET total = %s, casa = %s, fora = %s WHERE tipo = %s AND nome = %s"
            tipo= self.quantidade_escanteios
            valores = (total, casa, fora, tipo, nome_time)
    
            try:
                cursor.execute(query, valores)
            except mysql.connector.Error as err:
                print(f"Erro MySQL: {err}")
                conexao.rollback()
       
        conexao.commit()
        conexao.close()
        
        return(my_list)