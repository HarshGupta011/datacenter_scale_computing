#!/usr/bin/env python3

import requests
import json, jsonpickle
import os
import sys
import base64
import glob
import redis


app = Flask(__name__)
@app.route('/apiv1/separate', methods=['POST'])
def separate():
    r = request
    if app.debug:
        print(f"Received {r} containing {r.data}")
    try:
        print(f"Received data is {r.data}")
        json = jsonpickle.decode(r.data)
        print(f"Decoded json is {json}")
        mp3data = base64.b64decode(json['mp3'])
        callback = json['data']
        r = redis.Redis(host='localhost',db=0)
        setname = "toWorker"
        redisClient.sadd(setname, mp3data)
    except:
        
@app.route('/apiv1/queue', methods=['GET'])
def queue():
    r = redis.Redis(host='localhost',db=0)
    r.get("toWorker")
    
    
@app.route('/apiv1/track', methods=['GET'])
def track():

@app.route('/apiv1/remove', methods=['GET'])
def remove():
    
/apiv1/separate[POST] - analyze the JSON base64 encoded data mp3 with model model and queue the work for waveform separation. When the analysis is completed the specified callback may be called but does not need to succeed. The REST server should return a unique identifier (songhash) that can later be used to retrieve the separated tracks or delete them.
/apiv1/queue/[GET] - dump the queued entries from the Redis database
/apiv1/track//track [GET] - retrieve the track ( any of base.mp3, vocals.mp3, drums.mp3, other.mp3) as a binary download. For example, you should be able to redirect the output of a curl command to a file and play that file as an MP3 file.
/apiv1/remove//track [GET] - remove the corresponding track. This could be a DELETE response since that would be a more "restful" semantics.