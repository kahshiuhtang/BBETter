import sqlite3
import os
import pandas as pd

class DataLoader:
    def __init__(self):
        self.con = sqlite3.connect(os.path.abspath(os.path.abspath("./nba.sqlite"))) # Should move this back to dataset
        self.cur = self.con.cursor()
        self.table_names = []

    def load_data(self):
        self.load_all_table_names() 
        self.load_all_data()
        return
    
    def load_all_table_names(self):
        # res = self.cur.execute("SELECT * FROM " + table + ";")
        res = self.cur.execute("SELECT name FROM sqlite_master")
        table_names = res.fetchall()
        for table_tup in table_names:
            self.table_names.append(table_tup[0])
        return self.table_names

    def load_all_data(self):
        print(self.table_names)
        for table_name in self.table_names:
            res = pd.read_sql_query("SELECT * FROM " + table_name, self.con)
            print(res)
        return