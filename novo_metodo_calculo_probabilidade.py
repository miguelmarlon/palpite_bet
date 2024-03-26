from pandas import pandas as pd
from dotenv import load_dotenv
from db_functions import DatabaseConnection


connection = DatabaseConnection.connect()      
cursor = connection.cursor()

tabelas = ['goals_scored', 'goals_conceded']
times_api_id = [50, 40]
tipos_de_gols = [1, 2, 3]
for tabela in tabelas:
    for time in times_api_id:
        for tipo_de_gol in tipos_de_gols:
            object_db_funcitions_away_team_scored = DatabaseConnection.query_goals(cursor,tabelas, times_api_id, tipos_de_gols)

print(object_db_funcitions_away_team_scored)           
# # ALGORITIMO DO GPT
# time_a_marcar_05 = 1
# time_a_marcar_15 = 0.714
# time_a_marcar_25 = 0.357
# time_a_sofrer_05 = 0.929
# time_a_sofrer_15 = 0.714
# time_a_sofrer_25 = 0.286

# time_b_marcar_05 = 0.462
# time_b_marcar_15 = 0.77
# time_b_marcar_25 = 0.77
# time_b_sofrer_05 = 0.923
# time_b_sofrer_15 = 0.528
# time_b_sofrer_25 = 0.308

# chance_sair_1gol = ((time_a_marcar_05 * time_b_sofrer_05) + (time_b_marcar_05 * time_a_sofrer_05))/2
# chance_sair_mais_1_gol = ((time_a_marcar_15 * time_b_sofrer_15) + (time_b_marcar_15 * time_a_sofrer_15))/2
# chance_sair_mais_2_gol = ((time_a_marcar_25 * time_b_sofrer_25) + (time_b_marcar_25 * time_a_sofrer_25))/2

# print(f'Chance de sair 1 gol: {chance_sair_1gol}')
# print(f'Chance de sair mais de 1 gols: {chance_sair_mais_1_gol}')
# print(f'Chance de sair mais de 2 gols: {chance_sair_mais_2_gol}')

# # ALGORITIMO DO GEMINI
# prob_a_1_gol = 1
# prob_a_mais_1_gol = 0.714
# prob_a_mais_2_gols = 0.357
# prob_a_sofrer_1_gol = 0.929

# # Probabilidades do Time B
# prob_b_1_gol = 0.462
# prob_b_mais_1_gol = 0.77
# prob_b_mais_2_gols = 0.77
# prob_b_sofrer_1_gol = 0.923

# # Probabilidades de gols na partida
# prob_1_gol = (prob_a_1_gol * prob_b_sofrer_1_gol) + (prob_b_1_gol * prob_a_sofrer_1_gol)
# prob_mais_1_gol = (prob_a_mais_1_gol * 1) + (prob_b_mais_1_gol * 1) + (prob_a_mais_1_gol * prob_b_mais_1_gol)
# prob_mais_2_gols = (prob_a_mais_2_gols * 1) + (prob_b_mais_2_gols * 1) + (prob_a_mais_2_gols * prob_b_mais_2_gols)

# # Ajustando as probabilidades
# prob_1_gol = prob_1_gol / 2
# prob_mais_1_gol = prob_mais_1_gol / 3
# prob_mais_2_gols = prob_mais_2_gols / 3

# # Imprimindo os resultados
# print(f"Probabilidade de sair 1 gol: {prob_1_gol:.2%}")
# print(f"Probabilidade de sair mais de 1 gol: {prob_mais_1_gol:.2%}")
# print(f"Probabilidade de sair mais de 2 gols: {prob_mais_2_gols:.2%}")

# ### Para sair 1 gol ###
# # 1 gol time A - time B sofrendo 1 gol
# # 1 gol time B - tima A sofrendo 1 gol
# # resultados: A 1 x B 0 // A 0 x B 1

# ### Para sair mais de 1 gol ###
# # 2 gols time A com time B sofrendo 2 gols
# # 1 gol time A com time B sofrendo 1 gol e 1 gol time B com time A sofrendo 1 gol
# # 2 gols tim B com time A sofrendo 2 gols
# # resultados: A 2 X B 0 // A 1 X B 1 // A 0 X B 2

# ### Para sair mais de 2 gols ###
# # 3 gols do time A com o Time B sofrendo 3 gols
# # 2 gols do time A com o time B sofrendo 2 gols e 1 gol do time B com o time A sofrendo 1 gol
# # 1 gol do time A com o time B sofrendo 1 gol e 1 2 gols do time B com o time A sofrendo 2 gols
# # 3 gols do time B com o time A sofrendo 3 gols
# # resultados: A 3 X B 0 // A 2 X B 1 // A 1 X B 2 // A 0 X B 3

# # minha adptação
# prob_a_1_gol = 1
# prob_a_mais_1_gol = 0.714
# prob_a_mais_2_gols = 0.357
# prob_a_sofrer_1_gol = 0.929
# time_a_sofrer_15_gols = 0.714
# time_a_sofrer_25_gols = 0.286

# # Probabilidades do Time B
# prob_b_1_gol = 0.462
# prob_b_mais_1_gol = 0.77
# prob_b_mais_2_gols = 0.77
# prob_b_sofrer_1_gol = 0.923
# time_b_sofrer_15_gols = 0.538
# time_b_sofrer_25_gols = 0.308


# # Probabilidades de gols na partida
# prob_1_gol = (prob_a_1_gol * prob_b_sofrer_1_gol) + (prob_b_1_gol * prob_a_sofrer_1_gol)

# # 2 gols time A com time B sofrendo 2 gols
# # 1 gol time A com time B sofrendo 1 gol e 1 gol time B com time A sofrendo 1 gol
# # 2 gols tim B com time A sofrendo 2 gols
# prob_mais_1_gol = (prob_a_mais_1_gol * time_b_sofrer_15_gols) + (prob_b_mais_1_gol * time_a_sofrer_15_gols) + (prob_a_1_gol * prob_b_sofrer_1_gol + prob_b_1_gol * prob_a_sofrer_1_gol)
    
# # 3 gols do time A com o Time B sofrendo 3 gols ok
# # 2 gols do time A com o time B sofrendo 2 gols e 1 gol do time B com o time A sofrendo 1 gol ok
# # 1 gol do time A com o time B sofrendo 1 gol e 1 2 gols do time B com o time A sofrendo 2 gols
# # 3 gols do time B com o time A sofrendo 3 gols ok
# prob_mais_2_gols = (prob_a_mais_2_gols * time_b_sofrer_25_gols) + (prob_b_mais_2_gols * time_a_sofrer_25_gols) + (prob_a_mais_1_gol * time_b_sofrer_15_gols + prob_b_1_gol * prob_a_1_gol) + (prob_b_mais_1_gol * time_a_sofrer_15_gols + prob_a_1_gol * prob_b_sofrer_1_gol)

# # Ajustando as probabilidades
# prob_1_gol = prob_1_gol / 2
# prob_mais_1_gol = prob_mais_1_gol / 3
# prob_mais_2_gols = prob_mais_2_gols / 4

# # Imprimindo os resultados
# print(f"Probabilidade de sair 1 gol: {prob_1_gol:.2%}")
# print(f"Probabilidade de sair mais de 1 gol: {prob_mais_1_gol:.2%}")
# print(f"Probabilidade de sair mais de 2 gols: {prob_mais_2_gols:.2%}")