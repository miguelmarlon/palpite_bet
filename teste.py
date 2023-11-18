from scraping_team_goals import TeamGoals
from data_processor import DataProcessor

country, league, goal_quantity= 'Germany' , 'Bundesliga'  , 'Over 1.5'

# team_goals_obj = TeamGoals(country, league, goal_quantity)
# team_goals_obj.create_goals_scored_database()

# team_goals_obj = TeamGoals(country, league, goal_quantity)
# team_goals_obj.create_goals_conceded_database()

data_processor_obj = DataProcessor('Bayern Munich', 'Bochum')
data_processor_obj.additional_goals_statistics()

a=1