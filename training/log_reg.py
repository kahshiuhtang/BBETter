import sqlite3
from data_loader import DataLoader

class LogReg:
    def __init__(self):
        self.loader = DataLoader()

    def load_tables(self, tables=""):
        return self.loader.load_data(tables)

model = LogReg()
print(model.load_tables(tables="game"))