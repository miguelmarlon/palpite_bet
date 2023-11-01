from tratando_dados import tratando_dados
import mysql.connector
from dotenv import load_dotenv
import os
from criando_conexao_bd import conexao_bd
from criando_bd import criando_banco_de_dados

load_dotenv()
conexao = conexao_bd.conectando()
lista_times= []

print()
print('******************BEM VINDO AO PROGRAMA!******************')
print()

while True:
    opcao = input('0 - SAIR\n\n'
                '1 - ENTRAR NA SELEÇÃO DE TIMES\n\n'
                '2 - ATUALIZAR O BANCO DE DADOS\n\n'
                '3 - CRIAR O BANCO DE DADOS\n\n'
                '4 - EXLCUIR LINHAS DUPLICADAS NO BANCO DE DADOS\n\n'
                'OPÇÃO : ')
    match opcao:
        case '0':
            print('SAINDO DO PROGRAMA...')
            exit()
        case '1':
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
                objeto = tratando_dados(time_casa, time_fora)       
                df_gols = objeto.estatistica_filtrada_gol()
            conexao.commit()
            conexao.close()
            
        case '2':
            objeto_um = criando_banco_de_dados()
            objeto_um.atualizando_banco_de_dados_gols()
            objeto_dois = criando_banco_de_dados()
            objeto_dois.atualizando_banco_de_dados_escanteios()
            break
            
        case '3':
            objeto_um = criando_banco_de_dados()
            objeto_um.criando_banco_de_dados_gols()
            objeto_dois = criando_banco_de_dados()
            objeto_dois.criando_banco_de_dados_escanteios()
            break
        
        case '4':
            objeto_um = criando_banco_de_dados()
            objeto_um.excluindo_linhas_duplicadas_no_banco_de_dados()
            
            break
                
        case _:
            print('OPÇÃO INVÁLIDA!')


    