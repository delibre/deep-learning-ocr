import numpy as np
import cv2
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt


class Model:
    def __init__(self, filepath: str) -> None:
        self._model = load_model(filepath, compile = True)

    def prepare(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = 255 - image

        return cv2.resize(image, dsize=(20, 20), interpolation=cv2.INTER_CUBIC) / 255

    def predict(self, image):
        predictions = self._model.predict([self.prepare(image).reshape((1, 20, 20))])

        return chr(np.argmax(predictions[0]))

    
