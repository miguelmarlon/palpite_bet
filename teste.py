from scraping_team_goals import TeamGoals

country, league, goal_quantity= 'Italy' , 'Serie B'  , 'Over 0.5'


team_goals_obj = TeamGoals(country, league, goal_quantity)
team_goals_obj.create_goals_database()

a=1