**OBSERVATIONS**
| Method          | Local   | Same-Zone | Different Region |
|-----------------|---------|-----------|------------------|
| REST add        | 2.863   | 2.9417    | 287.4033         |
| gRPC add        | 0.643   | 0.7549    | 145.1820         |
| REST rawimg     | 4.6812  | 5.2269    | 1180.4518        |
| gRPC rawimg     | 5.0546  | 5.8302    | 195.4452         |
| REST dotproduct | 2.915   | 3.1962    | 289.3381         |
| gRPC dotproduct | 0.7291  | 0.9854    | 146.1619         |
| REST Jsonimg    | 82.5412 | 83.5064   | 2042.2770        |
| gRPC Jsonimg    | 17.9961 | 22.9783   | 240.1708         |
| Ping            | 0.054   | 0.360     | 142              |

I created the add, rawImage, dotProduct, jsonImage endpoints and I ran the REST service and the GRPC service on all the endpoints for an iteration count of 1000 for the local and same zone (US server - US client)test. When the client was on the different region(EU) I ran the rawImage and JsonImage endpoints for a count of 100 iterations while the add and dotProduct for 1000.

Results:

**Local Server and Client**

The GRPC service performed 4-5 times faster than the REST service while executing the add service, jsonImg service and the dot product service. This is mainly due to the tight packing of the protocol buffers used in gRPC in comparison to the JSON format used in REST sevices for data transfer. GRPC uses HTTP/2 which enable clients to open long-lived connections for subsequent queries whereas the REST api calls use HTTP 1.1 which require a fresh TCP connection for each query. The time required to establish a fresh connection for every query is an overhead which significantly increases the average time required per query when compared to gRPC. Also GRPC is designed for low latency and high throughput communication and it suitable for low-weight services such as the add and dotProduct functions.

However GRPC performed slower than REST in terms of sending **streaming data** such as images.Protocol buffers are not designed to be used with large messeges and when we need to transfer data that is greater than a MB it is not the best choice due to the time required for the transfer . As both the client and server are running on the same host, REST communication could be faster since the data doesn't have to be serialised. However, GRPC serialises data even on the local network, thereby increasing the time required to query.



**Same-Zone Server and Client**

While testing on two difference hosts that are within the same zone, the GRPC add, dotProduct and JsonImage service surpasses those of the REST by roughly 4 - 5 times in terms of performance which is similar to what we observed in the Local server client case. The time taken for all the actions are slightly more than the previous case as now the servers and clients are located on separate machines. This increase in time could be explained by the fact that the Network latency depends on the pysical distance between the server and client.

The ratio of time taken by the REST rawimage and the GRPC rawimage services is along the same lines as we previously observed. GRPCs are slightly poor when it comes to streaming large data. The difference in performance of samezone tests to the local tests can be explained by the physical distance the packet needs to travel from source to destination.



**Different region Server and Client**

When I placed the client on a different region(EU) than the server(US), the performance takes a huge hit. Network latency is directly dependent on the number of network devices which have to be crossed by a packet and this is the main reason for the increase in time.  The Rest performs worse than gRPC as it creates a new TCP connection for every request made and this request might need to make several hops before reaching the europe-west 3 server.Although the performance for gRPC also takes a great hit while in different zones but it is still significantly better when compared to the REST service. GRPC makes just a single TCP connection from client to server which is used for all its queries which can make better use of server resources.

The ratio in time required by REST to that by gRPC increases as we use differnet services. For add and dot product service since the data that was needed to be transferred was minimal, REST performs 2-3 times worse than gRPC, however, as we increse the volume of the data transferred, GRPC becomes very fast owing to the compactness of protocol buffers. There is a 5-6 times difference in gRPC and REST speeds for rawImage (note that the performance boost received by the compactness of protobufs overcomes the slower speed for streaming data in gRPC). This ratio becomes even higher and reaches 10X when we send the JsonImage due to the increase in size of the transferred data.