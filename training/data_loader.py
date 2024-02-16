import sqlite3
import os
import pandas as pd

class DataLoader:
    def __init__(self):
        # self.con = sqlite3.connect(os.path.abspath(os.path.abspath("./nba.sqlite"))) # Should move this back to dataset
        # self.cur = self.con.cursor()
        self.tables = []
        self.file_names = ['dataset/games_details.csv', 'dataset/games.csv', 'dataset/players.csv', 'dataset/ranking.csv', 'dataset/teams.csv']
        self.merged_df = None

    def load_data(self):
        if self.load_all_data():
            return
        self.merge_tables()
        self.clean_columns()
        self.clean_up_table()
        self.convert_types()
        return


    def load_all_data(self):
        if os.path.isfile(os.path.abspath('dataset/merged.csv')):
            self.merged_df = pd.read_csv(os.path.abspath(os.path.abspath('dataset/merged.csv')),dtype=str)
            return True
        for file in self.file_names:
            df = pd.read_csv(os.path.abspath(os.path.abspath(file)),dtype=str)
            self.tables.append(df)   
        return False
    
    def merge_tables(self):
        merge_df = pd.merge(self.tables[0], self.tables[1], how='left', left_on=['GAME_ID'], right_on=['GAME_ID'])
        merge_df = pd.merge(merge_df, self.tables[2], how='left', left_on=['TEAM_ID', 'PLAYER_ID'], right_on=['TEAM_ID', 'PLAYER_ID'])
        merge_df = pd.merge(merge_df, self.tables[3], how='left', left_on=['TEAM_ID','GAME_DATE_EST'], right_on=['TEAM_ID', 'STANDINGSDATE'])
        merge_df.to_csv('dataset/merged.csv')
        self.merged_df = merge_df
        return
    
    def clean_columns(self):
        self.merged_df.drop(columns=['TEAM_CITY', 'TEAM', 'RETURNTOPLAY','SEASON_y', 'PLAYER_NAME_y', 'NICKNAME'])
        self.merged_df.to_csv('dataset/merged.csv')
        return
    
    def convert_types(self):
        self.merged_df.apply(pd.to_numeric, errors='ignore')
        print(self.merged_df.dtypes)
        self.merged_df.to_csv('dataset/merged.csv')
        return
    
    def clean_up_table(self):
        self.merged_df.drop(['COMMENT', 'PLAYER_NAME_y', 'LEAGUE_ID', 'TEAM_ABBREVIATION','TEAM_CITY', 'PLAYER_NAME_x', 'NICKNAME', 'GAME_STATUS_TEXT', 'SEASON_y', 'TEAM', 'RETURNTOPLAY'],axis=1, inplace=True)
        self.merged_df['START_POSITION'].replace({'G':0, 'F':1, 'C':2}, inplace=True)
        self.merged_df['CONFERENCE'].replace({'East':0, 'West': 1}, inplace=True)
        self.merged_df.rename(columns={'Unnamed: 0.1': 'idx'}, inplace=True)
        self.merged_df.set_index('idx', inplace=True)
        self.merged_df.drop(['COMMENT'], axis=1, inplace=True)
        self.merged_df['MIN'] = self.merged_df['MIN'].apply(lambda x: x.replace(':','.'))
        self.merged_df['HOME_RECORD'] = self.merged_df['HOME_RECORD'].apply(lambda x: x.replace(' ','.'))
        self.merged_df['ROAD_RECORD'] = self.merged_df['ROAD_RECORD'].apply(lambda x: x.replace(' ','.'))
        self.merged_df.to_csv('dataset/merged.csv')
