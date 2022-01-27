from argparse import ArgumentParser

from flask import Flask, jsonify, request
import numpy as np

from model import Model


app = Flask(__name__)
model: Model = None


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return 'Optical Character Recognition Server is running'


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    #print(data)

    chars = []
    for line in data:
        for char in line:
            image = np.clip(np.array(char, dtype=np.float64), 0, 1) * 255
            image = image.astype(np.uint8)
            if np.sum(image) <= 0.001:
                chars.append(' ')
                continue                
            
            code = model.predict(image)
            
            chars.append(chr(code))
        chars.append('\n')

    return jsonify({
        'text': ''.join(chars)
    }), 200


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('model_path', help='a path to the image classifier model')
    
    args = parser.parse_args()

    model = Model(args.model_path)

    app.run(port=2640)
