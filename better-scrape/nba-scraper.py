from nba_api.stats.endpoints import boxscoretraditionalv3
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams

from datetime import date
from datetime import timedelta


def get_last_nights_box_scores():
    nba_teams = teams.get_teams()
    teams_searched = set()
    for team in nba_teams:
        team_id = team['id']
        gamefinder = leaguegamefinder.LeagueGameFinder(
            team_id_nullable=team_id)
        yesterdays_game = gamefinder.get_data_frames()[
            0].sort_values('GAME_DATE').iloc[-1]
        game_id = yesterdays_game['GAME_ID']
        game_date = yesterdays_game['GAME_DATE']
        yesterday = date.today() - timedelta(days=1)
        if str(game_date) == str(yesterday):
            game = boxscoretraditionalv3.BoxScoreTraditionalV3(
                game_id=game_id)
            box_score = game.get_data_frames()[0]


get_last_nights_box_scores()
