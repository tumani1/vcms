from socket import socket
import json


host = 'localhost'
port = 8080
path = "/test/echo"
xmlmessage = json.dumps({'message': 'hi'})

s = socket()
s.connect((host, port))
s.send("POST %s HTTP/1.1\r\n" % path)
s.send("Host: %s\r\n" % host)
s.send("Content-Type: text/json\r\n")
s.send("Content-Length: %d\r\n\r\n" % len(xmlmessage))
s.send(xmlmessage)
for line in s.makefile():
    print line,
s.close()