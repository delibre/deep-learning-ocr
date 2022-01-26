import glob

from scipy.ndimage.interpolation import shift
from PIL import ImageOps, Image
import numpy as np
import cv2

from evaluate import load


def negate(img):
    return ImageOps.invert(img)


def trim(img):
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


def process_char(img):
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


def create_dataset(filepaths):
    def roll(img, shifts, axis):
        img = np.copy(img)
        indexing = [slice(0, img.shape[i], 1) for i in range(img.ndim)]
        for i in range(img.shape[axis]):
            indexing[axis] = i
            img[tuple(indexing)] = np.roll(img[tuple(indexing)], shifts[i])
        return img
    
    X = []
    y = []
    for fp in filepaths:
        image = load(fp)
        img = image.image

        if img.ndim > 2:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # processing image the same way it will be done in ocr
        img = trim(img)
        img = process_char(img)
        
        # adding processed image to dataset
        X.append(img)
        y.append(image.code)
        
        # data augmentation
        # shifting
        for dx, dy in [(1, 0), (0,   1),   (-1, 0), (0, -1),
                       (1, 1), (-1, -1), (-1, 1), (1, -1)]:
            X.append(shift(img, (dx, dy)))
            y.append(image.code)
            
        # shearing
        for _ in range(5):
            # along axis 0
            shifts0 = np.random.randint(0, 2, size=img.shape[0])
            rolled0 = roll(img, shifts0, 0)
            X.append(rolled0)
            y.append(image.code)
            
            # along axis 1
            shifts1 = np.random.randint(0, 2, size=img.shape[1])
            X.append(roll(img, shifts1, 1))
            y.append(image.code)
            
            # along both axes
            X.append(roll(rolled0, shifts1, 1))
            y.append(image.code)
            
    return np.array(X, dtype=np.uint8), \
           np.array(y, dtype=np.uint8)


if __name__ == '__main__':
    fps = list(glob.glob('letters/*.png'))

    X, y = create_dataset(fps)

    np.save('X.npy', X)
    np.save('y.npy', y)
