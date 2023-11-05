import pandas as pd
import telegram
import asyncio
from dotenv import load_dotenv
import os
from criando_conexao_bd import conexao_bd

class tratando_dados():
    
    def __init__(self, time_casa, time_fora):
        
        self.time_casa = time_casa
        self.time_fora = time_fora
        self.gols_total = None
        self.gols_home = None
        self.gols_away = None
               
    def estatistica_gol(self):
        
        conexao = conexao_bd.conectando()
        cursor = conexao.cursor()
        consulta_time_casa = "SELECT * FROM gols WHERE nome LIKE %s"
        cursor.execute(consulta_time_casa, (f'%{self.time_casa}%',))
        
        resultado_casa = cursor.fetchall()
        
        consulta_time_fora = "SELECT * FROM gols WHERE nome LIKE %s"
        cursor.execute(consulta_time_fora, (f'%{self.time_fora}%',))
        resultado_fora = cursor.fetchall()
        
        print('Estatistica gols:')
        print(self.time_casa)
        for item in resultado_casa:
            print(item)  
        
        print()
        print(self.time_fora)
        for item in resultado_fora:
            print(item)      
        print()   
                                                           
        cursor.close()
        conexao.close()  
        
    def estatistica_escanteios(self):
       
        conexao = conexao_bd.conectando()       
        cursor = conexao.cursor()
        consulta_time_casa = "SELECT * FROM escanteios WHERE nome LIKE %s"
        cursor.execute(consulta_time_casa, (f'%{self.time_casa}%',))
        resultado_casa = cursor.fetchall()
             
        cursor = conexao.cursor()
        consulta_time_fora = "SELECT * FROM escanteios WHERE nome LIKE %s"
        cursor.execute(consulta_time_fora, (f'%{self.time_fora}%',))
        resultado_fora = cursor.fetchall()

        print('Estatistica escanteios:')
        print(self.time_casa)
        for item in resultado_casa:
            print(item)  
        
        print()
        print(self.time_fora)
        for item in resultado_fora:
            print(item)  
              
        cursor.close()
        conexao.close()
    
    def estatistica_filtrada_gol(self):
        
            conexao = conexao_bd.conectando()      
            cursor = conexao.cursor()
            consulta_time_casa = "SELECT * FROM gols WHERE nome LIKE %s"
            cursor.execute(consulta_time_casa, (f'%{self.time_casa.lower()}%',))
            resultado_casa = cursor.fetchall()
                            
            consulta_time_fora = "SELECT * FROM gols WHERE nome LIKE %s"
            cursor.execute(consulta_time_fora, (f'%{self.time_fora.lower()}%',))
            resultado_fora = cursor.fetchall()
                                             
            dados_finais = []

            async def enviar_mensagem_telegram(mensagem):
                load_dotenv()
                bot_token = os.getenv('bot_token')
                chat_id = os.getenv('chat_id')
                bot = telegram.Bot(token=bot_token)
                await bot.send_message(chat_id=chat_id, text=mensagem)
                                            
            for tupla_time_casa, tupla_time_fora in zip(resultado_fora, resultado_casa):
                chave = tupla_time_casa[1]
                total = (tupla_time_casa[3] + tupla_time_fora[3]) / 2
                casa_vs_visitante = (tupla_time_casa[4] + tupla_time_fora[5]) / 2
                dados_finais.append((chave, total, casa_vs_visitante))

            df = pd.DataFrame(dados_finais, columns=['gols', 'total', 'casavisitante'])
            df_filtrado_gols_acima = df[(df['total'] >= 75) & (df['casavisitante'] >= 75)]
            df_filtrado_gols_abaixo = df[(df['total'] <= 25) & (df['casavisitante'] <= 25)]
                                  
            mensagem =''
            mensagem_gols_acima=''
            mensagem_gols_abaixo=''       
            
            if not df_filtrado_gols_acima.empty:
                mensagem_gols_acima = f"Chances para {self.time_casa} vs {self.time_fora} ⚽:\n\n"
                for index, row in df_filtrado_gols_acima.iterrows():
                    gols = row['gols']
                    casavisitante = row['casavisitante']                                  
                    mensagem_gols_acima += f"Gols acima de {gols}: {casavisitante}% 🎯\n"
                mensagem += mensagem_gols_acima
                

            if not df_filtrado_gols_abaixo.empty:
                mensagem_gols_abaixo = f"Chances para {self.time_casa} vs {self.time_fora} ⚽:\n\n"
                for index, row in df_filtrado_gols_abaixo.iterrows():
                    gols = row['gols']
                    casavisitante =100 - row['casavisitante']                               
                    mensagem_gols_abaixo += f"Gols abaixo de {gols}: {casavisitante}% 🎯\n"   
            mensagem += mensagem_gols_abaixo
            
            if mensagem:
                asyncio.run(enviar_mensagem_telegram(mensagem))  
                     
            cursor.close()
            conexao.close()
                              
    def estatistica_filtrada_escanteios(self):
        
        conexao = conexao_bd.conectando()
        cursor = conexao.cursor()
        consulta_time_casa = f"SELECT * FROM escanteios WHERE nome = '{self.time_casa}'"
        cursor.execute(consulta_time_casa)
        resultado_casa = cursor.fetchall()
            
        cursor = conexao.cursor()
        consulta_time_fora = f"SELECT * FROM escanteios WHERE nome = '{self.time_fora}'"
        cursor.execute(consulta_time_fora)
        resultado_fora = cursor.fetchall()
        
        async def enviar_mensagem_telegram(mensagem):
            load_dotenv()
            bot_token = os.getenv('bot_token')
            chat_id = os.getenv('chat_id')
            bot = telegram.Bot(token=bot_token)
            await bot.send_message(chat_id=chat_id, text=mensagem)
                
        dados_finais=[]
        
        for tupla1, tupla2 in zip(resultado_fora, resultado_casa):
            chave = tupla1[1]
            total = (float(tupla1[3]) + float(tupla2[3])) / 2
            casa_vs_visitante = (float(tupla1[4]) + float(tupla2[5])) / 2
            dados_finais.append((chave, total, casa_vs_visitante))
                
        df = pd.DataFrame(dados_finais, columns=['escanteios', 'total', 'casavisitante'])
        df_filtrado_escanteios_acima = df[(df['total'] >= 75) & (df['casavisitante'] >= 75)]    
        df_filtrado_escanteios_abaixo = df[(df['total'] <= 25) & (df['casavisitante'] <= 25)]
        
        mensagem =''
        mensagem_escanteios_acima=''
        mensagem_escanteios_abaixo=''
                                    
        if not df_filtrado_escanteios_acima.empty:
            mensagem_escanteios_acima = f"Chances para {self.time_casa} vs {self.time_fora} ⚽:\n\n"
            for index, row in df_filtrado_escanteios_acima.iterrows():
                escanteios = row['escanteios']
                casavisitante = row['casavisitante']
                print(f'Escanteios: acima de {escanteios} probabilidade {casavisitante}')               
                mensagem += f"Escanteios {escanteios}: {casavisitante}% 🎌\n"
            mensagem += mensagem_escanteios_acima
        
        
        if not df_filtrado_escanteios_abaixo.empty:
            mensagem_escanteios_abaixo = f"Chances para {self.time_casa} vs {self.time_fora} ⚽:\n\n"
            for index, row in df_filtrado_escanteios_abaixo.iterrows():
                escanteios = row['escanteios']
                casavisitante = 100 - row['casavisitante']             
                mensagem_escanteios_abaixo += f"Escanteios abaixo de {escanteios}: {casavisitante}% 🎌\n"
            mensagem += mensagem_escanteios_abaixo
        
        if mensagem:
            asyncio.run(enviar_mensagem_telegram(mensagem))
                        
        cursor.close()
        conexao.close()
    