from nba_api.stats.endpoints import boxscoretraditionalv3, boxscoreusagev3, boxscoreadvancedv3, boxscoredefensivev2, boxscorefourfactorsv3, boxscorehustlev2, boxscorematchupsv3, boxscoremiscv3, boxscoreplayertrackv3, boxscorescoringv3, boxscoresummaryv2, hustlestatsboxscore
from nba_api.stats.endpoints import leaguegamefinder, leaguedashplayerstats, leaguedashptstats, shotchartdetail, shotchartlineupdetail
from nba_api.stats.endpoints import leaguedashteamstats, leaguehustlestatsplayer, leaguehustlestatsteam, matchupsrollup
from nba_api.stats.endpoints import playerdashptpass, playerdashptreb, playerdashptshotdefend, playerdashptshots,playerestimatedmetrics
from nba_api.stats.endpoints import playergamelog, leaguedashlineups, leaguedashplayerptshot, leaguedashplayershotlocations
from nba_api.stats.endpoints import teamplayeronoffdetails, teamplayeronoffsummary, teamdashptreb, teamdashptpass, teamdashptshots, teamestimatedmetrics, teamdashlineups
from nba_api.stats.static import teams, players

from datetime import date
from datetime import timedelta

def _get_box_scores(game_id):
    game = boxscoretraditionalv3.BoxScoreTraditionalV3(
        game_id=game_id)
    box_score = game.get_data_frames()[0]
    ret_val = box_score['teamId'].unique()

    game = boxscoreusagev3.BoxScoreUsageV3(game_id=game_id)
    box_score = game.get_data_frames()[0]
    box_score.to_csv("BoxScoreUsageV3.csv")

    game = boxscoreadvancedv3.BoxScoreAdvancedV3(game_id=game_id)
    box_score = game.get_data_frames()[0]
    box_score.to_csv("BoxScoreAdvancedV3.csv")
    return ret_val
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

    game = hustlestatsboxscore.HustleStatsBoxScore(game_id=game_id)
    box_score = game.get_data_frames()[0]
    box_score.to_csv("BoxScoreHustle.csv")

    return ret_val

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
            ret = _get_box_scores(game_id)
            teams_searched |= ret
            return


def get_top_lineups():
    lineup = leaguedashlineups.LeagueDashLineups(
        measure_type_detailed_defense="Advanced")
    line_up_data = lineup.get_data_frames()[0]
    line_up_data.to_csv("top-lineups-advanced.csv")

    lineup = leaguedashlineups.LeagueDashLineups(
        measure_type_detailed_defense="Opponent")
    line_up_data = lineup.get_data_frames()[0]
    line_up_data.to_csv("top-lineups-opponents.csv")


def get_player_career_stats():
    nba_players = players.get_active_players()
    for player in nba_players:
        player_id = player['id']
        game_logs = playergamelog.PlayerGameLog(
            player_id=player_id, season='ALL')
        game_logs_df = game_logs.get_data_frames()[0]
        yearly_stats_df = game_logs_df.groupby('SEASON_ID').sum().reset_index().drop(
            ['GAME_DATE', 'Game_ID', 'WL', 'MATCHUP', 'FT_PCT', 'FG3_PCT', 'FG_PCT'], axis=1)
        break

def get_lineup_data():
    lineups = leaguedashlineups.LeagueDashLineups(measure_type_detailed_defense="Advanced",per_mode_detailed="Per48")
    lineups.get_data_frames()[0].to_csv("advanced_lineups.csv")
    lineups =leaguedashlineups.LeagueDashLineups(measure_type_detailed_defense="Opponent",per_mode_detailed="Per48")
    lineups.get_data_frames()[0].to_csv("opponent_lineups.csv")
    ptshot = leaguedashplayerptshot.LeagueDashPlayerPtShot (per_mode_simple="PerGame", location_nullable="Home")
    ptshot.get_data_frames()[0].to_csv("ptshot_home.csv")
    ptshot = leaguedashplayerptshot.LeagueDashPlayerPtShot (per_mode_simple="PerGame", location_nullable="Road")
    ptshot.get_data_frames()[0].to_csv("ptshot_away.csv")
    shot_locations = leaguedashplayershotlocations.LeagueDashPlayerShotLocations(distance_range="By Zone", per_mode_detailed="Per48")
    shot_locations.get_data_frames()[0].to_csv("shot_locations.csv")

def get_last_ten_games_stats():
    stats = leaguedashplayerstats.LeagueDashPlayerStats(last_n_games="10", measure_type_detailed_defense="Base")
    stats.get_data_frames()[0].to_csv("last_ten_stats_base.csv")
    stats = leaguedashplayerstats.LeagueDashPlayerStats(last_n_games="10", measure_type_detailed_defense="Advanced")
    stats.get_data_frames()[0].to_csv("last_ten_stats_advanced.csv")
    stats = leaguedashplayerstats.LeagueDashPlayerStats(last_n_games="10", measure_type_detailed_defense="Usage")
    stats.get_data_frames()[0].to_csv("last_ten_stats_usage.csv")
    stats = leaguedashplayerstats.LeagueDashPlayerStats(last_n_games="10", measure_type_detailed_defense="Defense")
    stats.get_data_frames()[0].to_csv("last_ten_stats_defense.csv")

def get_recent_team_performance_last_10():
    pt_stats = leaguedashptstats.LeagueDashPtStats(last_n_games="10", per_mode_simple="PerGame", pt_measure_type="SpeedDistance")
    pt_stats.get_data_frames()[0].to_csv("pt_stats_speed_distance.csv")
    pt_stats = leaguedashptstats.LeagueDashPtStats(last_n_games="10", per_mode_simple="PerGame", pt_measure_type="Possessions")
    pt_stats.get_data_frames()[0].to_csv("pt_stats_posessions.csv")
    pt_stats = leaguedashptstats.LeagueDashPtStats(last_n_games="10", per_mode_simple="PerGame", pt_measure_type="CatchShoot")
    pt_stats.get_data_frames()[0].to_csv("pt_stats_catchshoot.csv")
    pt_stats = leaguedashptstats.LeagueDashPtStats(last_n_games="10", per_mode_simple="PerGame", pt_measure_type="PullUpShot")
    pt_stats.get_data_frames()[0].to_csv("pt_stats_pullupshoot.csv")
    pt_stats = leaguedashptstats.LeagueDashPtStats(last_n_games="10", per_mode_simple="PerGame", pt_measure_type="Defense")
    pt_stats.get_data_frames()[0].to_csv("pt_stats_defense.csv")
    pt_stats = leaguedashptstats.LeagueDashPtStats(last_n_games="10", per_mode_simple="PerGame", pt_measure_type="Drives")
    pt_stats.get_data_frames()[0].to_csv("pt_stats_drives.csv")
    pt_stats = leaguedashptstats.LeagueDashPtStats(last_n_games="10", per_mode_simple="PerGame", pt_measure_type="Possessions")
    pt_stats.get_data_frames()[0].to_csv("pt_stats_posessions.csv")
    pt_stats = leaguedashptstats.LeagueDashPtStats(last_n_games="10", per_mode_simple="PerGame", pt_measure_type="Efficiency")
    pt_stats.get_data_frames()[0].to_csv("pt_stats_efficiency.csv")
    pt_stats = leaguedashptstats.LeagueDashPtStats(last_n_games="10", per_mode_simple="PerGame", pt_measure_type="ElbowTouch")
    pt_stats.get_data_frames()[0].to_csv("pt_stats_elbow_touch.csv")
    pt_stats = leaguedashptstats.LeagueDashPtStats(last_n_games="10", per_mode_simple="PerGame", pt_measure_type="PostTouch")
    pt_stats.get_data_frames()[0].to_csv("pt_stats_post_touch.csv")
    pt_stats = leaguedashptstats.LeagueDashPtStats(last_n_games="10", per_mode_simple="PerGame", pt_measure_type="PaintTouch")
    pt_stats.get_data_frames()[0].to_csv("pt_stats_paint_touch.csv")
    pt_stats = leaguedashptstats.LeagueDashPtStats(last_n_games="10", per_mode_simple="PerGame", pt_measure_type="Rebounding")
    pt_stats.get_data_frames()[0].to_csv("pt_stats_rebounding.csv")

def get_team_stats_last_10():
    team_last10 = leaguedashteamstats.LeagueDashTeamStats(last_n_games="10", per_mode_detailed="Per48", measure_type_detailed_defense="Base")
    team_last10.get_data_frames()[0].to_csv("team_last10_base.csv")
    team_last10 = leaguedashteamstats.LeagueDashTeamStats(last_n_games="10", per_mode_detailed="Per48", measure_type_detailed_defense="Advanced")
    team_last10.get_data_frames()[0].to_csv("team_last10_advanced.csv")
    team_last10 = leaguedashteamstats.LeagueDashTeamStats(last_n_games="10", per_mode_detailed="Per48", measure_type_detailed_defense="Defense")
    team_last10.get_data_frames()[0].to_csv("team_last10_defense.csv")

def get_hustle():
    hustle_player = leaguehustlestatsplayer.LeagueHustleStatsPlayer(per_mode_time="Per48")
    hustle_player.get_data_frames()[0].to_csv("hustle_player.csv")
    hustle_team = leaguehustlestatsteam.LeagueHustleStatsTeam(per_mode_time="Per48")
    hustle_team.get_data_frames()[0].to_csv("hustle_team.csv")

def get_other_player_info():
    # [NOTE] Need team_id and player_id
    player_pt_pass = playerdashptpass.PlayerDashPtPass(last_n_games="10")
    player_pt_pass.get_data_frames()[0].to_csv("player_pt_pass.csv")
    player_pt_reb = playerdashptreb.PlayerDashPtReb()
    player_pt_reb.get_data_frames()[0].to_csv("player_pt_reb.csv")
    player_pt_shots = playerdashptshots.PlayerDashPtShots()
    player_pt_shots.get_data_frames()[0].to_csv("player_pt_shots.csv")
    player_pt_est_metrics = playerestimatedmetrics.PlayerEstimatedMetrics()
    player_pt_est_metrics.get_data_frames()[0].to_csv("player_pt_est_metrics.csv")

    chartdetail = shotchartdetail.ShotChartDetail()
    chartdetail.get_data_frames()[0].to_csv("chart_detail.csv")
    chartlineupdetail = shotchartlineupdetail.ShotChartLineupDetail()
    chartlineupdetail.get_data_frames()[0].to_csv("chart_lineup_detail.csv")

def get_on_off_details():
    # [NOTE] Need team_id
    nba_teams = teams.get_teams()
    for team in nba_teams:
        team_id = team["id"]
        team_pt_shots = teamdashptshots.TeamDashPtShots(last_n_games="10", team_id=team_id)
        team_pt_shots.get_data_frames()[0].to_csv(str(team["id"]) + "_team_pt_shots.csv")
        team_pt_pass = teamdashptpass.TeamDashPtPass(last_n_games="10", team_id=team_id)
        team_pt_pass.get_data_frames()[0].to_csv(str(team["id"]) +"_team_pt_pass.csv")
        team_pt_est_metrics = teamestimatedmetrics.TeamEstimatedMetrics()
        team_pt_est_metrics.get_data_frames()[0].to_csv(str(team["id"]) + "_team_pt_est_metrics.csv")
        return

def get_all_games_last_15_years():
    nba_teams = teams.get_teams()
    game_ids = set()
    for i in range(23,24):
        season_year = "20" + str(i) + "-" + str(i+1)
        for team in nba_teams:
            team_id = team['id']
            gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season_year, team_id_nullable=team_id)
            all_games = gamefinder.get_data_frames()[
                0].sort_values('GAME_DATE')
            for game_id in all_games['GAME_ID']:
                print("New Round")
                _get_box_scores(game_id)
            print(all_games.to_csv("GAMES.csv"))
            break
"""
LeagueDashTeamClutch (Mins)
[NOTE]: Add in this metric later
"""
import nba_scraper.nba_scraper as ns

#scrape a season
nba_df = ns.scrape_season(2019)

# if you want a csv if you don't pass a file path the default is home
# directory
ns.scrape_season(2019, data_format='csv', data_dir='file/path')