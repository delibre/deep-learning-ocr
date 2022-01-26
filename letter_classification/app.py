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

    print(data)

    image = data['mwdata'][0]['mwdata'][0]
    image = np.clip(np.array(image, dtype=np.float64), 0, 1) * 255
    image = image.astype(np.uint8)

    code = model.predict(image)

    return jsonify({
        'code': int(code)
    }), 200


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('model_path', help='a path to the image classifier model')
    
    args = parser.parse_args()

    model = Model(args.model_path)

    app.run(port=2640)
