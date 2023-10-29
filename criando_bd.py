
from tratando_dados import tratando_dados
from scraping_escanteios import Escanteios
from scraping_gols_marcados_sofridos import Gols


pesquisa_gols= 'Over 1.5'
pais_teste ='Italy'
liga_teste= 'Serie A'
escanteios_teste='7.5'

quantidade_gols = ['Over 1.5', 'Over 2.5', 'Over 3.5']
quantidade_escanteios = ['7.5','8.5','9.5','10.5', '11.5']

list_pais = [['Finland','Finnish Veikkausliiga'],['Italy', 'Serie A'],['England', 'Premier League'],['Spain', 'La Liga'],['Germany','Bundesliga'],['France', 'Ligue 1'],
             ['Scotland','SPL'],['Netherlands', 'Eredivisie'],['Portugal','Portugese Liga NOS'],['Turkey','Turkish Super Lig'],['Greece','Greek Super League'],['Belgium','Pro League'],['Brazil','Serie A'],
            ['Austria','Bundesliga'],['Russia','Premier League'],['Argentina','Primera Division'],['Denmark', 'Superliga'],['Poland','Ekstraklasa'],['USA','US MLS'],
            ['Norway','Norwegian Eliteserien'],['Sweden','Swedish Allsvenskan'],['Switzerland','Swiss Super League'],['Australia','A League'],['Japan','J League'],
            ['China','Super League'],['Mexico','Liga MX'],['Ukraine','Premier League'],['Czechia','Czech Liga'],['Saudi Arabia','Saudi Pro League']
            ]
            # ['Finland','Finnish Veikkausliiga'] não tem essa liga para corners 
list_pais_escanteios = [['Italy', 'Serie A'],['England', 'Premier League'],['Spain', 'La Liga'],['Germany','Bundesliga'],['France', 'Ligue 1'],['Scotland','SPL'],
                        ['Netherlands', 'Eredivisie'],['Portugal','Portugese Liga NOS'],['Turkey','Turkish Super Lig'],['Greece','Greek Super League'],['Belgium','Pro League'],
                        ['Brazil','Serie A'],['Austria','Bundesliga'],['Russia','Premier League'],['Argentina','Primera Division'],['Denmark', 'Superliga'],['Poland','Ekstraklasa'],
                        ['USA','US MLS'],['Norway','Norwegian Eliteserien'],['Sweden','Swedish Allsvenskan'],['Switzerland','Swiss Super League'],['Australia','A League'],['Japan','J League'],
                        ['China','Super League'],['Mexico','Liga MX'],['Ukraine','Premier League'],['Czechia','Czech Liga'],['Saudi Arabia','Saudi Pro League']]                   


#criando bando de dados de gols
# for gol in quantidade_gols:
#     for pais, liga in list_pais:
#         gols = Gols(pais, liga, gol)
#         dados = gols.cria_bd_gols()
#         print (dados)


# criando estatísticas de escanteios no DB
# for escanteio in quantidade_escanteios:
#     for pais, liga in list_pais_escanteios:
     
#         escanteios = Escanteios(pais, liga, escanteio)
#         dados = escanteios.cria_bd_escanteios()
#         print (dados)

#atualizando bando de dados de gols
for gol in quantidade_gols:
    for pais, liga in list_pais:
        gols = Gols(pais, liga, gol)
        dados = gols.atualiza_bd_gols()
        print (dados)

a=1