# Simple REST server tutorial

## Dependencies

```
pip3 install pillow jsonpickle
```

## Overview

This is a simple example of a REST server using both GET and POST
queries written using the Flask package. This is not intended to be an
example of good programming practice or secure coding examples.

## Sample Queries

### Simple GET
```
 curl --verbose http://127.0.0.1:5000/api/add/10/20
*   Trying 127.0.0.1:5000...
* Connected to 127.0.0.1 (127.0.0.1) port 5000 (#0)
> GET /api/add/10/20 HTTP/1.1
> Host: 127.0.0.1:5000
> User-Agent: curl/7.71.1
> Accept: */*
>
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 13
< Server: Werkzeug/1.0.1 Python/3.8.5
< Date: Tue, 21 Sep 2021 17:39:02 GMT
<
* Closing connection 0
{"sum": "30"}
```

### Simple POST
curl --verbose -d '{ "a" : [2,3], "b" : [1,2]}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/dotproduct
```
curl --verbose -d '{ "a" : 200, "b" : 100}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/sub
*   Trying 127.0.0.1:5000...
* Connected to 127.0.0.1 (127.0.0.1) port 5000 (#0)
> POST /api/sub HTTP/1.1
> Host: 127.0.0.1:5000
> User-Agent: curl/7.71.1
> Accept: */*
> Content-Type: application/json
> Content-Length: 23
>
* upload completely sent off: 23 out of 23 bytes
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 21
< Server: Werkzeug/1.0.1 Python/3.8.5
< Date: Tue, 21 Sep 2021 17:39:44 GMT
<
* Closing connection 0
{"difference": "100"}
```

### POST with binary data
```
curl -v --data-binary @cu-in-snow.jpg -H 'Content-Type: image/png' http://127.0.0.1:5000/api/image
*   Trying 127.0.0.1:5000...
* Connected to 127.0.0.1 (127.0.0.1) port 5000 (#0)
> POST /api/image HTTP/1.1
> Host: 127.0.0.1:5000
> User-Agent: curl/7.71.1
> Accept: */*
> Content-Type: image/png
> Content-Length: 515000
>
* We are completely uploaded and fine
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 30
< Server: Werkzeug/1.0.1 Python/3.8.5
< Date: Tue, 21 Sep 2021 17:40:25 GMT
<
* Closing connection 0
{"width": 1613, "height": 856}
```
