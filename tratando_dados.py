import mysql.connector
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
    
    def excluindo_linhas_duplicadas(self):
        conexao = conexao_bd.conectando()
        cursor = conexao.cursor()

        try:
            # Criar uma nova tabela temporária sem duplicatas. tipo e nome são as colunas duplicadas
            consulta_criar_temporaria = """
            CREATE TABLE gols_temp AS
            SELECT DISTINCT tipo, nome, total, casa, fora
            FROM gols
            """

            cursor.execute(consulta_criar_temporaria)
            consulta_excluir_original = "DROP TABLE gols"
            cursor.execute(consulta_excluir_original)

            # Renomear a tabela temporária para o nome original
            consulta_renomear = "RENAME TABLE gols_temp TO gols"
            cursor.execute(consulta_renomear)

            # Confirmar a operação (commit)
            conexao.commit()
            print("Linhas duplicadas excluídas com sucesso!")

        except mysql.connector.Error as e:
            # Em caso de erro, fazer rollback
            conexao.rollback()
            print(f"Erro ao excluir linhas duplicadas: {e}")

        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            conexao.close()
       
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
        cursor.execute(consulta_time_casa, (f'%{self.time_casa}%',))
        resultado_casa = cursor.fetchall()
                        
        consulta_time_fora = "SELECT * FROM gols WHERE nome LIKE %s"
        cursor.execute(consulta_time_fora, (f'%{self.time_fora}%',))
        resultado_fora = cursor.fetchall()
                      
        dados_finais = []
        
        async def enviar_mensagem_telegram(mensagem):
            load_dotenv()
            bot_token = os.getenv('bot_token')
            chat_id = os.getenv('chat_id')
            bot = telegram.Bot(token=bot_token)
            await bot.send_message(chat_id=chat_id, text=mensagem)
                        
        for tupla1, tupla2 in zip(resultado_fora, resultado_casa):
            chave = tupla1[1]
            total = (float(tupla1[3]) + float(tupla2[3])) / 2
            casa_vs_visitante = (float(tupla1[4]) + float(tupla2[5])) / 2

            # Adicione uma tupla diretamente à lista dados_finais
            dados_finais.append((chave, total, casa_vs_visitante))

        # Crie um DataFrame diretamente a partir da lista de tuplas
        df = pd.DataFrame(dados_finais, columns=['gols', 'total', 'casavisitante'])
                        
        # Filtre o DataFrame com base na condição > 75
        df_filtrado = df[(df['total'] >= 75) & (df['casavisitante'] >= 75)]
        if not df_filtrado.empty:
            #df_filtrado['media_entre_total_casavistante'] = df_filtrado[['total', 'casavisitante']].mean(axis=1)
            mensagem = f"Chances para {self.time_casa} vs {self.time_fora} ⚽:\n\n"
            for index, row in df_filtrado.iterrows():
                gols = row['gols']
                casavisitante = row['casavisitante']
                print(f'Gols: {gols} probabilidade {casavisitante}')               
                mensagem += f"Gols {gols}: {casavisitante}% 🎯\n"
    
            # Crie e execute o loop de eventos assíncronos
            loop = asyncio.get_event_loop()
            loop.run_until_complete(enviar_mensagem_telegram(mensagem))
                    
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
            bot_token = '6608150715:AAENt1H31xQwgQaTQmUl6qRqKREOjkwj7tI'
            chat_id = '-4093651715'
            bot = telegram.Bot(token=bot_token)
            await bot.send_message(chat_id=chat_id, text=mensagem)
                
        dados_finais=[]
        
        for tupla1, tupla2 in zip(resultado_fora, resultado_casa):
            chave = tupla1[1]
            total = (float(tupla1[3]) + float(tupla2[3])) / 2
            casa_vs_visitante = (float(tupla1[4]) + float(tupla2[5])) / 2

            # Adicione uma tupla diretamente à lista dados_finais
            dados_finais.append((chave, total, casa_vs_visitante))

        # Crie um DataFrame diretamente a partir da lista de tuplas
        df = pd.DataFrame(dados_finais, columns=['escanteios', 'total', 'casavisitante'])
        
        # Filtre o DataFrame com base na condição > 75
        df_filtrado = df[(df['total'] >= 75) & (df['casavisitante'] >= 75)]    
        
        df_filtrado['media_entre_total_casavistante'] = df_filtrado[['total', 'casavisitante']].mean(axis=1)
        mensagem = f"Chances para {self.time_casa} vs {self.time_fora}:\n\n"
        for index, row in df_filtrado.iterrows():
            escanteios = row['escanteios']
            media_final_escanteios = row['media_entre_total_casavistante']
            print(f'Escanteios: {escanteios} probabilidade {media_final_escanteios}')

            #mensagem = f"Chances para {time_casa} vs {time_fora}:\n\n"
            mensagem += f"Escanteios {escanteios}: {media_final_escanteios}%\n"
    
        # Crie e execute o loop de eventos assíncronos
        loop = asyncio.get_event_loop()
        loop.run_until_complete(enviar_mensagem_telegram(mensagem))
                         
        cursor.close()
        conexao.close()
