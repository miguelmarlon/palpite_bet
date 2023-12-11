import requests
from database_connection import DatabaseConnection


country_list = [['Italy', 'Serie A'], ['Italy', 'Serie B'], ['England', 'Premier League'], ['England', 'Championship'], ['England', 'League One'], ['England', 'League Two'], 
                ['England', 'National League'], ['Spain', 'La Liga'], ['Spain', 'Segunda Division'] ,['Germany','Bundesliga'],['Germany','Bundesliga 2'],['France', 'Ligue 1'],['France', 'Ligue 2'],
                ['Scotland','SPL'], ['Netherlands', 'Eredivisie'], ['Netherlands', 'Eerste Divisie'], 
                ['Portugal','Portugese Liga NOS'],['Turkey','Turkish Super Lig'],['Greece','Greek Super League'],['Belgium','Pro League'], ['Belgium','First Division B'], ['Brazil','Serie A'],['Brazil','Serie B'],
                ['Austria','Bundesliga'], ['Argentina','Primera Division'],['Denmark', 'Superliga'],['Poland','Ekstraklasa'],['USA','US MLS'],
                ['Norway','Norwegian Eliteserien'],['Switzerland','Swiss Super League'],
                ['Mexico','Liga MX']]

list_country_id = [['Belgium','Pro League', 144],['Greece','Greek Super League', 197],['Scotland','SPL', 179], ['Italy', 'Serie A', 135], ['Italy', 'Serie B', 136],
                ['England', 'Premier League', 39], ['England', 'Championship', 40], ['England', 'League One', 41],  ['England', 'League Two', 42],
                ['Spain', 'La Liga', 140], ['Spain', 'Segunda Division', 141], ['Germany', 'Bundesliga', 78],['Germany','2. Bundesliga', 79], ['France', 'Ligue 1', 61], ['France', 'Ligue 2', 62],
                ['Europa','UEFA Champions League', 2],['Europa','UEFA Europa League', 3],['Europa','Europa Conference League', 848],['Netherlands', 'Eredivisie', 88], ['Netherlands', 'Eerste Divisie', 89], 
                ['Portugal', 'Primeira Liga', 94], ['Turkey', 'Super Lig', 203], ['Brazil', 'Serie A', 71], ['Brazil', 'Serie B', 72], 
                ['Denmark', 'Superliga', 119], ['USA', 'Major League Soccer', 253], ['Norway', 'Eliteserien', 103], ['Austria', 'Bundesliga', 218], ['Mexico', 'Liga MX', 262], ['Argentina','Primera Division', 128],['France', 'Coupe de France', 66],
                ['Switzerland','Super League',207]]




# try:
#     connection = DatabaseConnection.connect()
#     cursor = connection.cursor()
#     for country, league, id in list_country_id:
#         query = 'INSERT INTO country (name) VALUES (%s) ON DUPLICATE KEY UPDATE name=name'
#         values = (country,)
#         cursor.execute(query, values)
        
#         query = 'SELECT country_id FROM country WHERE name = %s'
#         cursor.execute(query, (country,))
#         country_id = cursor.fetchall()[0][0]
        
#         query = 'INSERT INTO league (name, api_id, country_id) VALUES (%s, %s, %s)'
#         values = (league, id, country_id)
#         cursor.execute(query, values)
#     connection.commit()
    
# except Exception as e:
#     print(f"Erro: {e}")
#     connection.rollback()

# finally:
#     cursor.close()
#     connection.close()


# # Convertendo as listas em conjuntos
# set_country_id = {tuple(item) for item in list_country_id}
# set_country_list = {tuple(item) for item in country_list}

# # Encontrando os itens em set_country_id que não estão em set_country_list
# items_not_in_country_list = [list(item) for item in set_country_id if item[:2] not in set_country_list]

# print(items_not_in_country_list)

#

a=1