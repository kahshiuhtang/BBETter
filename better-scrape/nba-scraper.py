from nba_api.stats.endpoints import boxscoretraditionalv3
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import boxscoreusagev3
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import teams
from nba_api.stats.static import players

from datetime import date
from datetime import timedelta


def get_last_nights_box_scores():
    nba_teams = teams.get_teams()
    teams_searched = set()
    for team in nba_teams:
        team_id = team['id']
        if team_id in teams_searched:
            continue
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
            teams_searched |= set(box_score['teamId'].unique())


def get_player_career_stats():
    nba_players = players.get_active_players()
    for player in nba_players:
        player_id = player['id']
        game_logs = playergamelog.PlayerGameLog(
            player_id=player_id, season='ALL')
        game_logs_df = game_logs.get_data_frames()[0]
        print(game_logs_df['SEASON_ID'].unique())
        yearly_stats_df = game_logs_df.groupby('SEASON_ID').sum().reset_index().drop(
            ['GAME_DATE', 'Game_ID', 'WL', 'MATCHUP', 'FT_PCT', 'FG3_PCT', 'FG_PCT'], axis=1)
        print(yearly_stats_df.to_csv("test.csv"))
        break


get_player_career_stats()
