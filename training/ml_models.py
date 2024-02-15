from sklearn.cluster import KMeans
from data_loader import DataLoader
from sklearn.model_selection import train_test_split
import torch

class KMeansModel:
    def __init__(self):
        self.loader = DataLoader()
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_text = None

    def load_tables(self):
        return self.loader.load_data()

    def train_model(self):
        model = KMeans()

    def test_model(self):
        pass
model = KMeansModel()
print(model.load_tables())