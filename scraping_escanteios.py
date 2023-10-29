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
from criando_conexao_bd import conexao_bd

class Escanteios:
    
    def __init__(self, pais, league, quantidade_escanteios):
        self.pais = pais
        self.league = league
        self.quantidade_escanteios= quantidade_escanteios
        
    def cria_bd_escanteios(self):  
        
        my_list= []
        list_times=[]
        
        options= Options()
        options.add_argument('window-size=800,1200')
              

        navegador = webdriver.Chrome(options=options)
        wait = WebDriverWait(navegador, 20)
        navegador.get('https://www.adamchoi.co.uk/corners/detailed')

        button_league = navegador.find_element(By.XPATH, '//*[@id="country"]')
        select = Select(button_league)
        sleep(3)
        select.select_by_visible_text(self.pais)
        
        button_league = navegador.find_element(By.XPATH, '//*[@id="league"]')
        select = Select(button_league)
        sleep(3)
        select.select_by_visible_text(self.league)
                
        select_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div/div[3]/div/div[2]/div/select')))
        select = Select(select_element)
        select.select_by_visible_text(self.quantidade_escanteios)

        page_content = navegador.page_source
        site= BeautifulSoup(page_content, 'html.parser')


        busca_times = site.find('div', attrs={'class':'row ng-scope', 'data-ng-if': '!vm.isLoading'})
        times = busca_times.find_all('div', attrs={'data-ng-repeat': 'team in :refreshStats:vm.teams', 'class':'ng-scope'})
        for time in times:
            time_nome = time.find('div', attrs={'class':'col-lg-3 col-sm-6 col-xs-12 ng-binding'})
                        
            if time_nome:
                match_5 = re.search(r'^(.+?)\s(?=Overall)', time_nome.text)
                if match_5:
                    time_nome = match_5.group(1).replace('FR', '').replace('CA', '').replace('FBC', '').replace('EC', '').replace('RJ', '').replace('FC', '').replace('Al', '').replace('RS', '').replace('SE', '').strip()  
                    time_nome = match_5.group(1).strip()
                else:
                    raise Exception('TIME NÃO ENCONTRADO!')
            else:
                raise Exception('Nome do time não encontrado!')
                        
            busca_escanteios = time.find('div', attrs={'class': 'progress'})
                
            busca_total_escanteios = busca_escanteios.find('div', attrs={'class':'progress-bar progress-bar-success ng-binding'})
            total_escanteios = busca_total_escanteios.text.replace('%', '')
            busca_total_escanteios = busca_escanteios.find('div', attrs={'class': 'progress-bar progress-bar-danger ng-binding'})
            #verifica se tem um valor atribuido ou não antes de converter em float           
            if total_escanteios != '':
                total_escanteios = float(total_escanteios)
            else:
                total_escanteios = None  
            
            busca_escanteios_home_away = time.find('div', attrs={'class': 'panel-body'})
            busca_escanteios_home_away = busca_escanteios_home_away.find_all('div', attrs={'class': 'col-lg-9 col-sm-6 col-xs-12'})
            
            busca_escanteios_home = busca_escanteios_home_away[0]
            escanteios_home = busca_escanteios_home.find('div', attrs={'class': 'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            #verifica se tem um valor atribuido ou não antes de converter em float      
            if escanteios_home != '':
                escanteios_home = float(escanteios_home)
            else:
                escanteios_home = None
                        
            busca_escanteios_away = busca_escanteios_home_away[1]
            escanteios_away = busca_escanteios_away.find('div', attrs={'class': 'progress-bar progress-bar-success ng-binding'}).text.replace('%', '')
            #verifica se tem um valor atribuido ou não antes de converter em float       
            if escanteios_away != '':
                escanteios_away = float(escanteios_away)
            else:
                escanteios_away = 0  
                               
            
            list_times = [
            time_nome,
            total_escanteios,
            escanteios_home,
            escanteios_away,
            ]
            
            my_list.append(list_times)
        
        conexao = conexao_bd.conectando()
        cursor = conexao.cursor()
        
        for linha in my_list:
            nome_time, total, casa, fora = linha 
            query = f'INSERT INTO escanteios (tipo, nome, total, casa, fora) VALUES ({self.quantidade_escanteios}, "{nome_time}", "{total}", "{casa}", "{fora}")'
            cursor.execute(query)
       
        conexao.commit()
        conexao.close()
        
        return(my_list)
        