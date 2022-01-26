import numpy as np
import cv2
from tensorflow.keras.models import load_model
from PIL import Image
import matplotlib.pyplot as plt


class Model:
    def __init__(self, filepath: str) -> None:
        self._model = load_model(filepath, compile = True)

    def trim(self, img):
        h, w = img.shape
        
        rboundary = np.amax((img > 127).astype(np.uint8), axis=1)
        cboundary = np.amax((img > 127).astype(np.uint8), axis=0)
        
        rnonzero = np.nonzero(rboundary)
        rstart = rnonzero[0][0]
        rend = rnonzero[0][-1]
        
        cnonzero = np.nonzero(cboundary)
        cstart = cnonzero[0][0]
        cend = cnonzero[0][-1]
        
        return img[rstart:rend, cstart:cend]


    def process_char(self, img):
        h, w = img.shape
        coef = 20 / max(h, w)
        if h > w:
            new_size = (int(coef * w), 20)
        else:
            new_size = (20, int(coef * h))
        
        pil_img = Image.fromarray(img.astype(np.uint8), mode='L')
        pil_img = pil_img.resize(new_size, resample=Image.BICUBIC)

        img = np.array(pil_img, dtype=np.uint8)
        h, w = img.shape
        
        pad_h = (20-h) // 2
        pad_w = (20-w) // 2
        img = np.pad(img, [(pad_h, 20-pad_h-h), (pad_w, 20-pad_w-w)])
        
        return img

    def prepare(self, image: np.ndarray) -> np.ndarray:
        if image.ndim > 2:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        image = self.trim(image)
        image = self.process_char(image)

        return image / 255

    def predict(self, image: np.ndarray) -> int:
        images = [self.prepare(image).reshape((1, 20, 20))]
        predictions = self._model.predict(images)

        return np.argmax(predictions[0])

    
