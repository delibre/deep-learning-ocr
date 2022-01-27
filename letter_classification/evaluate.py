from argparse import ArgumentParser
from pathlib import Path
import glob

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tqdm
import cv2

from model import Model


class Image:
    def __init__(self, image: np.ndarray, code: int) -> None:
        self.image = image
        self.code = code


def load(filepath: str):
    filepath: Path = Path(filepath)

    name, _ = filepath.name.split('.', 1)
    code, _ = name.split('x')
    code = int(code)

    if code <= 26:
        code = int(code) + ord('A') - 1
    elif code >= 79:
        code = int(code) + ord('A') - 79
    elif code >= 27 and code <= 52:
        code = int(code) + ord('a') - 27
    elif code >= 53 and code <= 78:
        code = int(code) + ord('a') - 53

    return Image(cv2.imread(str(filepath)), code)


def load_csv(filepath: str):
    df = pd.read_csv(filepath)
    df = df.loc[df['m_label'] < 128]

    X = np.array(df.iloc[:, 12:])
    y = np.array(df['m_label'], dtype=np.uint8)

    return [Image(np.reshape(X[i, :], (20, 20)), y[i]) for i in range(y.shape[0])]


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('model_path', help='a path to the image classifier model')
    parser.add_argument('source', help='a source path')
    parser.add_argument('--csv', action='store_true', help='load from a csv')
    parser.add_argument('--show', action='store_true', help='show a few examples')
    parser.add_argument('--no_eval', action='store_false', help='do not evaluate')
    parser.add_argument('--limit', default=None, type=int, help='limit the number of images')
    
    args = parser.parse_args()

    if args.csv:
        images = load_csv(args.source)
    else:
        images = [load(fp) for fp in glob.glob(args.source)]
    
    model = Model(args.model_path)

    np.random.shuffle(images)

    if args.limit is not None:
        images = images[:args.limit]

    if args.show:
        for image in images[:5]:
            plt.imshow(image.image, cmap='gray')
            plt.title(f'code: {image.code}, chr: {chr(image.code)}')
            plt.show()

    if args.no_eval:
        tp = 0
        for image in tqdm.tqdm(images):
            code = model.predict(image.image)
            if code == image.code:
                tp += 1

        print(f'tp: {tp}')
        print(f'accuracy: {tp / len(images)}')
