from scraping_team_goals_total import Goals
from scraping_corners import Corners
corner_quantities = ['7.5', '8.5','9.5', '10.5', '11.5', '12.5']
country_list = [['Germany','Bundesliga', 78 ]]
goal_total_quantities = [ 'Over 1.5','Over 2.5','Over 3.5']

# for goals_quantity in goal_total_quantities:
#     for country, league, api_league_id in country_list:
#         goals_instance = Goals(country, league, goals_quantity, api_league_id)
#         data = goals_instance.create_goals_scored_conceded_table()
        
for corner_quantity in corner_quantities:
    for country, league, api_league_id in country_list:        
        corners_instance = Corners(country, league, corner_quantity)
        data= corners_instance.create_corners_table()
        
a=1