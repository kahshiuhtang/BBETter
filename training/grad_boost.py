from data_loader import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from joblib import dump, load


# Too slow on my computer
class GradBoostModel:
    def __init__(self):
        self.loader = DataLoader()
        self.training_full =None
        self.testing_full = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

    def load_tables(self):
        self.full_data = self.loader.load_data()
        self.full_data.to_csv("dataset/merged.csv")
        self.training_full, self.testing_full = train_test_split(self.full_data, test_size=0.3)
        
        self.y_train = self.training_full["PTS_home"].astype(float) + self.training_full["PTS_away"].astype(float)
        self.y_test = self.testing_full["PTS_home"].astype(float) + self.testing_full["PTS_away"].astype(float)

        self.X_train = self.training_full.drop("PTS_home", axis="columns")
        self.X_train = self.X_train.drop("PTS_away", axis="columns")

        self.X_test = self.testing_full.drop("PTS_home", axis="columns")
        self.X_test = self.X_test.drop("PTS_away", axis="columns")

    def train_model(self):
        self.model = GradientBoostingRegressor(max_depth = 3, random_state = 0)
        self.model.fit(self.X_train, self.y_train)

    def test_model(self):
        self.score = self.model.score(self.X_test, self.y_test)
        return self.score
    
    def save_model(self, file_path=None):
        if file_path == None:
            dump(self.model, '../models/grad_boost.joblib')
        else:
            dump(self.model, file_path)

    def load_model(self, file_path=None):
        if file_path == None:
            self.model = load('../models/grad_boost.joblib')
        else:
            self.model = load(file_path)
model = GradBoostModel()
model.load_tables()
model.train_model()
print(model.test_model())
model.save_model()
