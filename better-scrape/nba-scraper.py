from nba_api.stats.endpoints import boxscoretraditionalv3, boxscoreusagev3, boxscoreadvancedv3, boxscoredefensivev2, boxscorefourfactorsv3, boxscorehustlev2, boxscorematchupsv3, boxscoremiscv3, boxscoreplayertrackv3, boxscorescoringv3, boxscoresummaryv2
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import teams, players

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

            game = boxscoreusagev3.BoxScoreUsageV3(game_id=game_id)
            box_score = game.get_data_frames()[0]
            box_score.to_csv("BoxScoreUsageV3.csv")

            game = boxscoreadvancedv3.BoxScoreAdvancedV3(game_id=game_id)
            box_score = game.get_data_frames()[0]
            box_score.to_csv("BoxScoreAdvancedV3.csv")

            game = boxscoredefensivev2.BoxScoreDefensiveV2(game_id=game_id)
            box_score = game.get_data_frames()[0]
            box_score.to_csv("BoxScoreDefensiveV2.csv")

            game = boxscorefourfactorsv3.BoxScoreFourFactorsV3(game_id=game_id)
            box_score = game.get_data_frames()[0]
            box_score.to_csv("BoxScoreFourFactorsV3.csv")

            game = boxscorehustlev2.BoxScoreHustleV2(game_id=game_id)
            box_score = game.get_data_frames()[0]
            box_score.to_csv("BoxScoreHustleV2.csv")

            game = boxscorematchupsv3.BoxScoreMatchupsV3(game_id=game_id)
            box_score = game.get_data_frames()[0]
            box_score.to_csv("BoxScoreMatchupsV3.csv")

            game = boxscoremiscv3.BoxScoreMiscV3(game_id=game_id)
            box_score = game.get_data_frames()[0]
            box_score.to_csv("BoxScoreMiscV3.csv")

            game = boxscoreplayertrackv3.BoxScorePlayerTrackV3(game_id=game_id)
            box_score = game.get_data_frames()[0]
            box_score.to_csv("BoxScorePlayerTrackV3.csv")

            game = boxscorescoringv3.BoxScoreScoringV3(game_id=game_id)
            box_score = game.get_data_frames()[0]
            box_score.to_csv("BoxScoreScoringV3.csv")

            game = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id)
            box_score = game.get_data_frames()[0]
            box_score.to_csv("BoxScoreSummaryV2.csv")
            return


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


get_last_nights_box_scores()
