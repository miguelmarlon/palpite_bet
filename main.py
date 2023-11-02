from tratando_dados import tratando_dados
from dotenv import load_dotenv
import os
from criando_conexao_bd import conexao_bd
from criando_bd import criando_banco_de_dados

def buscar_time_por_nome(cursor, nome_time):
        consulta_time = "SELECT * FROM gols WHERE nome LIKE %s"
        cursor.execute(consulta_time, (f'%{nome_time}%',))
        return cursor.fetchall()
    
conexao = conexao_bd.conectando()
cursor = conexao.cursor()
load_dotenv()
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
                time_casa = input('DIGITE O NOME DO TIME DA CASA:')
                resultado_casa = buscar_time_por_nome(cursor, time_casa)

                if resultado_casa:
                    nomes_time_casa = set(row[2] for row in resultado_casa)

                    if len(nomes_time_casa) == 1:
                        time_casa = resultado_casa[0][2]
                    else:
                        print("Vários times correspondentes foram encontrados. Escolha um:")
                        for i, nome in enumerate(nomes_time_casa):
                            print(f"{i + 1}. {nome}")

                        escolha = int(input("Digite o número do time desejado: "))
                        nomes_time_casa = list(nomes_time_casa)
                        time_casa = nomes_time_casa[escolha - 1]
                        print(f"O nome do time escolhido é: {time_casa}")

                    time_fora = input('DIGITE O NOME DO TIME VISITANTE:')
                    resultado_fora = buscar_time_por_nome(cursor, time_fora)

                    if resultado_fora:
                        nomes_time_fora = set(row[2] for row in resultado_fora)

                        if len(nomes_time_fora) == 1:
                            time_fora = resultado_fora[0][2]
                        else:
                            print("Vários times correspondentes foram encontrados. Escolha um:")
                            for i, nome in enumerate(nomes_time_fora):
                                print(f"{i + 1}. {nome}")

                            escolha = int(input("Digite o número do time desejado: "))
                            nomes_time_fora = list(nomes_time_fora)
                            time_fora = nomes_time_fora[escolha - 1]
                            print(f"O nome do time escolhido é: {time_fora}")

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
                df_escanteios = objeto.estatistica_filtrada_escanteios()
            exit()
            
        case '2':
            objeto_um = criando_banco_de_dados()
            objeto_um.atualizando_banco_de_dados_gols()
            objeto_dois = criando_banco_de_dados()
            objeto_dois.atualizando_banco_de_dados_escanteios()
            break
            
        case '3':
            objeto_um = criando_banco_de_dados()
            objeto_um.criando_banco_de_dados_gols()
            # objeto_dois = criando_banco_de_dados()
            # objeto_dois.criando_banco_de_dados_escanteios()
            break
        
        case '4':
            objeto_um = criando_banco_de_dados()
            objeto_um.excluindo_linhas_duplicadas_no_banco_de_dados()
            
            break
                
        case _:
            print('OPÇÃO INVÁLIDA!')


    