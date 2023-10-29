from tratando_dados import tratando_dados
import mysql.connector
from dotenv import load_dotenv
import os
from criando_conexao_bd import conexao_bd

load_dotenv()

conexao = conexao_bd.conectando()
lista_times= []

print()
print('******************BEM VINDO AO PROGRAMA!******************')
print()

while True:
    time_casa = input('DIGITE O NOME DO TIME DA CASA:').capitalize()
    cursor = conexao.cursor()
    consulta_time_casa = "SELECT * FROM gols WHERE nome LIKE %s"
    cursor.execute(consulta_time_casa, (f'%{time_casa}%',))
    resultado_casa = cursor.fetchall()

    if resultado_casa:
        time_fora = input('DIGITE O NOME DO TIME VISITANTE:').capitalize()
        consulta_time_fora = "SELECT * FROM gols WHERE nome LIKE %s"
        cursor.execute(consulta_time_fora, (f'%{time_fora}%',))
        resultado_fora = cursor.fetchall()
        
        if resultado_fora:
            lista_temporaria = [time_casa, time_fora]
            lista_times.append(lista_temporaria)
        else:
            print(f'O TIME {time_fora} NÃO FOI ENCONTRADO!')
    else:
        print(f'O TIME {time_casa} NÃO FOI ENCONTRADO!')

    continuar = input('DIGITE QUALQUER TECLA PARA CONTINUAR OU 2 PARA SAIR:')
    if continuar == '2':
        print('AGUARDE UM INSTANTE PARA FINALIZAR:)')
        print()
        break
for time_casa, time_fora in lista_times:    
    teste = tratando_dados(time_casa, time_fora)       
    df_gols = teste.estatistica_filtrada_gol()

conexao.commit()
conexao.close()

a=1





