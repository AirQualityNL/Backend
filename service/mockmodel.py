import random

class MockModelService:
    def __init__(self, data):
        self.data = data

    def predict(self):
        random_index = random.randint(0, self.data.shape[0] - 1)
        no2 = [self.data[random_index][0][0], self.data[random_index][1][0]]
        pm25 = [self.data[random_index][0][3], self.data[random_index][1][3]]
        pm10 = [self.data[random_index][0][2], self.data[random_index][1][2]]
        o3 = [self.data[random_index][0][4], self.data[random_index][1][4]]
        return pm25, pm10, no2, o3