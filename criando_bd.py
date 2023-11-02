
from scraping_escanteios import Escanteios
from scraping_gols_marcados_sofridos import Gols
from criando_conexao_bd import conexao_bd
import mysql.connector

class criando_banco_de_dados:
    
    # pesquisa_gols= 'Over 1.5'
    # pais_teste ='Italy'
    # liga_teste= 'Serie A'
    # escanteios_teste='7.5'

    quantidade_gols = ['Over 1.5', 'Over 2.5', 'Over 3.5']
    quantidade_escanteios =['10.5', '11.5', '12.5']

    list_pais = [['Italy', 'Serie A'], ['Italy', 'Serie B'], ['England', 'Premier League'], ['England', 'Championship'], ['England', 'League One'], ['England', 'League Two'], 
                ['England', 'National League'], ['Spain', 'La Liga'], ['Spain', 'Segunda Division'] ,['Germany','Bundesliga'],['Germany','Bundesliga 2'],['France', 'Ligue 1'],['France', 'Ligue 2'],
                ['Scotland','SPL'], ['Scotland','Scottish Championship'], ['Scotland','Scottish League 1'], ['Scotland','Scottish League 2'], ['Netherlands', 'Eredivisie'], ['Netherlands', 'Eerste Divisie'], 
                ['Portugal','Portugese Liga NOS'],['Turkey','Turkish Super Lig'],['Greece','Greek Super League'],['Belgium','Pro League'], ['Belgium','First Division B'], ['Brazil','Serie A'],['Brazil','Serie B'],
                ['Austria','Bundesliga'],['Russia','Premier League'],['Argentina','Primera Division'],['Denmark', 'Superliga'],['Poland','Ekstraklasa'],['USA','US MLS'],
                ['Norway','Norwegian Eliteserien'],['Sweden','Swedish Allsvenskan'],['Switzerland','Swiss Super League'],['Australia','A League'],['Japan','J League'],
                ['China','Super League'],['Mexico','Liga MX'],['Czechia','Czech Liga'],['Saudi Arabia','Saudi Pro League'],['Finland','Finnish Veikkausliiga']]
    
     
                # ['Finland','Finnish Veikkausliiga'] não tem essa liga para corners 
    list_pais_escanteios = [['Italy', 'Serie A'],['Italy', 'Serie B'],['England', 'Premier League'],['England', 'Championship'],['England', 'League One'],['England', 'League Two'],['England', 'National League'],['Spain', 'La Liga'],['Spain', 'Segunda Division'],
                            ['Germany','Bundesliga'],['Germany','Bundesliga 2'],['France', 'Ligue 1'],['France', 'Ligue 2'],['Scotland','SPL'],['Scotland','Scottish Championship'],['Scotland','Scottish League 1'],['Scotland','Scottish League 2'],
                            ['Netherlands', 'Eredivisie'],['Netherlands', 'Eerste Divisie'],['Portugal','Portugese Liga NOS'],['Turkey','Turkish Super Lig'],['Greece','Greek Super League'],['Belgium','Pro League'],
                            ['Brazil','Serie A'],['Austria','Bundesliga'],['Russia','Premier League'],['Argentina','Primera Division'],['Denmark', 'Superliga'],['Poland','Ekstraklasa'],
                            ['USA','US MLS'],['Norway','Norwegian Eliteserien'],['Sweden','Swedish Allsvenskan'],['Switzerland','Swiss Super League'],['Australia','A League'],['Japan','J League'],
                            ['China','Super League'],['Mexico','Liga MX'],['Czechia','Czech Liga'],['Saudi Arabia','Saudi Pro League']]                   


    #criando bando de dados de gols
    def criando_banco_de_dados_gols(self):
        for gol in self.quantidade_gols:
            for pais, liga in self.list_pais:
                gols = Gols(pais, liga, gol)
                dados = gols.cria_bd_gols()
                print (dados)


    # criando estatísticas de escanteios no DB
    def criando_banco_de_dados_escanteios(self):
        for escanteio in self.quantidade_escanteios:
            for pais, liga in self.list_pais_escanteios:
                escanteios = Escanteios(pais, liga, escanteio)
                dados = escanteios.cria_bd_escanteios()
                print (dados)

    #atualizando bando de dados de gols
    def atualizando_banco_de_dados_gols(self):
        for gol in self.quantidade_gols:
            for pais, liga in self.list_pais:
                gols = Gols(pais, liga, gol)
                dados = gols.atualiza_bd_gols()
                print (dados)
    
    def atualizando_banco_de_dados_escanteios(self):
        for escanteio in self.quantidade_escanteios:
            for pais, liga in self.list_pais_escanteios:
                escanteios = Escanteios(pais, liga, escanteios)
                dados = escanteios.atualiza_bd_escanteios()
                print (dados)
    
    def excluindo_linhas_duplicadas_no_banco_de_dados(self):
        conexao = conexao_bd.conectando()
        cursor = conexao.cursor()

        try:            
            consulta_criar_temporaria_tabela_gols = """
            CREATE TABLE gols_temp AS
            SELECT DISTINCT id, tipo, nome, total, casa, fora
            FROM gols
            """
            cursor.execute(consulta_criar_temporaria_tabela_gols)
            consulta_excluir_original = "DROP TABLE gols"
            cursor.execute(consulta_excluir_original)
            
            consulta_renomear = "RENAME TABLE gols_temp TO gols"
            cursor.execute(consulta_renomear)

            conexao.commit()
            print("Linhas duplicadas da tabela gols excluídas com sucesso!")
            
            consulta_criar_temporaria_tabela_escanteios = """
            CREATE TABLE escanteios_temp AS
            SELECT DISTINCT id, tipo, nome, total, casa, fora
            FROM escanteios
            """
            cursor.execute(consulta_criar_temporaria_tabela_escanteios)
            consulta_excluir_original = "DROP TABLE escanteios"
            cursor.execute(consulta_excluir_original)
            
            consulta_renomear = "RENAME TABLE escanteios_temp TO escanteios"
            cursor.execute(consulta_renomear)

            conexao.commit()
            print("Linhas duplicadas da tabela escanteios excluídas com sucesso!")

        except mysql.connector.Error as e:
            conexao.rollback()
            print(f"Erro ao excluir linhas duplicadas: {e}")

        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            conexao.close()