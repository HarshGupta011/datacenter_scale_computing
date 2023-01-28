from flask import Flask, request, Response
import jsonpickle
import json
from PIL import Image
import io

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a,b):
    response = {'sum' : str( a + b)}
    response_pickled = jsonpickle.encode(response)
    print(f"Send response {response_pickled}")
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/sub', methods=['POST'])
def sub():
    r = request
    if app.debug:
        print(f"Received {r} with {len(r.data)} bytes of data")

    try:
        print(f"Received data is {r.data}")
        json = jsonpickle.decode(r.data)
        print(f"Decoded json is {json}")
        response = {'difference' : str( json['a'] - json['b'] )}
    except:
        response = { 'difference' : 0, 'error' : True }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


# route http posts to this method
@app.route('/api/image', methods=['POST'])
def image():
    r = request
    # convert the data to a PIL image type so we can extract dimensions
    if app.debug:
        print(f"Received {r} with {len(r.data)} bytes of data")
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)
    # build a response dict to send back to client
        response = {
            'width' : img.size[0],
            'height' : img.size[1]
            }
    except Exception as exp:
        print(f"Exception", exp)
        response = { 'width' : 0, 'height' : 0, 'error' : True}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
host = "0.0.0.0"
port = 5000
print(f"Running REST server on {host}:{port}")
app.run(host=host, port=port, debug=True)
