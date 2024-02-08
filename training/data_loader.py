import sqlite3
import os


class DataLoader:
    def __init__(self):
        self.con = sqlite3.connect(os.path.abspath("nba.sqlite")) # Should move this back to dataset
        self.cur = self.con.cursor()
        self.tables = []
        self.setup()

    def setup(self):
        
        return
    
    def load_data(self, table):
        # res = self.cur.execute("SELECT * FROM " + table + ";")
        res = self.cur.execute("SELECT name FROM sqlite_master")
        return res.fetchall()
