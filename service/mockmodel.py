import random

class MockModelService:
    def __init__(self, data):
        self.data = data

    def predict(self):
        random_index = random.randint(0, self.data.shape[0] - 1)
        return self.data[random_index]