#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import random

"""
This web server returns an HTML file (for GET requests) with a random value

To send a dictionary on the command line,
curl --data '{"this":"is a test"}' --header "Content-Type: application/json" http://localhost:1055

from https://pythonbasics.org/webserver/
and https://gist.github.com/nitaku/10d0662536f37a087e1b

how to server HTML files:
https://linuxhint.com/use-python-simplehttpserver/
"""

#hostName = "localhost" # if this is used, then server binds to localhost:port and is only accessible inside a container
hostName = "0.0.0.0" # an address used to refer to all IP addresses on the same machine
serverPort = 1033


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        #print('content type:',self.headers.get('content-type'))

        val = random.randint(3,10)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("<p>val = "+str(val)+"</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


    # POST echoes the message adding a JSON field
    def do_POST(self):
        #print('content type:',self.headers.get('content-type'))

        val = random.randint(3,10)

        # refuse to receive non-json content
        if self.headers.get('content-type') != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))

        #print('length:',self.headers.get('content-length'))

        message = json.loads(self.rfile.read(length))

        print("message = ", message)


        # send the message back

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>33</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes(json.dumps(message)+"\n","utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))



#        self.wfile.write(bytes(json.dumps({'hello': 'world', 'received': 'ok'}),"utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close()
        print("Server stopped.")
