from argparse import ArgumentParser
import numpy as np
from model import Model
import json


model: Model = None

def predict(data):
    
    for line in data:
        for char in line:
            image = np.clip(np.array(char, dtype=np.float64), 0, 1) * 255
            image = image.astype(np.uint8)
            if np.sum(image) <= 0.001:
                print(' ', end='')
                continue                
            
            code = model.predict(image)
            
            print(chr(code), end='')
        print()



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('model_path', help='a path to the image classifier model')
    parser.add_argument('json_data', help='path to json format')
    
    args = parser.parse_args()

    model = Model(args.model_path)
    
    f = open(args.json_data)
    data = json.load(f)
    f.close()

    print("\n\n\n ############## Encoded text ##############")
    predict(data)
