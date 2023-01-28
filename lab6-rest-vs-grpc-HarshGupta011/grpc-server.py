import grpc
from concurrent import futures
import time
from PIL import Image
import base64
import io

import grpc_pb2
import grpc_pb2_grpc

class addServicer(grpc_pb2_grpc.addServicer):
    def add(self, request, context):
        response = grpc_pb2.addReply()
        response.sum = request.a  + request.b
        return response

class rawImageServicer(grpc_pb2_grpc.rawImageServicer):
    def rawImage(self, request, context):
        response = grpc_pb2.imageReply()
        ioBuffer = io.BytesIO(request.img)
        img = Image.open(ioBuffer)
        response.width = img.size[0]
        response.height = img.size[1]
        return response

class dotProductServicer(grpc_pb2_grpc.dotProductServicer):
    def dotProduct(self, request, context):
        response = grpc_pb2.dotProductReply()
        a = request.a[:]
        b = request.b[:]
        response.dotproduct = sum(a[i]*b[i] for i in range(len(b)))
        return response

class jsonImageServicer(grpc_pb2_grpc.jsonImageServicer):
    def jsonImage(self, request, context):
        response = grpc_pb2.imageReply()
        imgdata = base64.b64decode(request.img)
        img = Image.open(io.BytesIO(imgdata))
        response.width = img.size[0]
        response.height = img.size[1]
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
grpc_pb2_grpc.add_addServicer_to_server(addServicer(), server)
grpc_pb2_grpc.add_rawImageServicer_to_server(rawImageServicer(), server)
grpc_pb2_grpc.add_dotProductServicer_to_server(dotProductServicer(), server)
grpc_pb2_grpc.add_jsonImageServicer_to_server(jsonImageServicer(), server)

server.add_insecure_port('[::]:50051')
print("Server started....")
server.start()
server.wait_for_termination()