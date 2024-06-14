class PollutantModel:
    def __init__(self, model):
        self.model = model

    def summary(self):
        return self.model.summary()
    
    def predict(self, data, forecasted_weather):
        predict = self.model.predict([data, forecasted_weather])
        return predict[0].tolist()