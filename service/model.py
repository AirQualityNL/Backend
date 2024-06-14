import tensorflow as tf

class PollutantModel:
    def __init__(self):
        self.model = tf.keras.models.load_model("model/pollutant_model.keras")

    def summary(self):
        return self.model.summary()