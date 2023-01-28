import requests
import json
import time
import sys
import base64
import random
import grpc
import grpc_pb2
import grpc_pb2_grpc

host = sys.argv[1]
h = f"{host}:50051"
channel = grpc.insecure_channel(h)
cmd = sys.argv[2]
reps = int(sys.argv[3])
img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()

if cmd == 'rawImage':
    start = time.perf_counter()
    stub = grpc_pb2_grpc.rawImageStub(channel)
    for x in range(reps):
        req = grpc_pb2.rawImageMsg(img = img)
        response = stub.rawImage(req)
        print("Height: ", response.height,"Width: ", response.width)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")

elif cmd == 'add':
    start = time.perf_counter()
    stub = grpc_pb2_grpc.addStub(channel)
    for x in range(reps):
        req = grpc_pb2.addMsg(a=100,b=200)
        response = stub.add(req)
        print("Sum is ", response.sum)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")

elif cmd == 'jsonImage':
    start = time.perf_counter()
    stub = grpc_pb2_grpc.jsonImageStub(channel)
    for x in range(reps):
        b64_img = base64.b64encode(img)
        str_img = b64_img.decode("utf-8")
        req = grpc_pb2.jsonImageMsg(img = str_img)
        response = stub.jsonImage(req)
        print("Height: ", response.height,"Width: ", response.width)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")

elif cmd == 'dotProduct':
    start = time.perf_counter()
    stub = grpc_pb2_grpc.dotProductStub(channel)
    for x in range(reps):
        n1,n2 = [],[]
        for i in range(100):
            n1.append(random.random())
            n2.append(random.random())
        req = grpc_pb2.dotProductMsg(a=n1,b=n2)
        response = stub.dotProduct(req)
        print("Dot Product is ", response.dotproduct)
    delta = ((time.perf_counter() - start)/reps)*1000
    print("Took", delta, "ms per operation")
else:
    print("Unknown option", cmd)