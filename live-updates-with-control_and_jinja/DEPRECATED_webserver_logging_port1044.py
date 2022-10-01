#!/usr/bin/env python3

import time
import os
import json
import random
import datetime


from http.server import BaseHTTPRequestHandler, HTTPServer

# https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse
from urllib.parse import urlparse
# https://docs.python.org/3/library/urllib.parse.html#urllib.parse.parse_qs
from urllib.parse import parse_qs


"""
This web server returns an HTML file (for GET requests) with a random value

To send a dictionary on the command line,
curl --data '{"this":"is a test"}' --header "Content-Type: application/json" http://localhost:1033

from https://pythonbasics.org/webserver/
and https://gist.github.com/nitaku/10d0662536f37a087e1b

how to serve HTML files:
https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/
"""

# hostName = "localhost" # if this is used, then server binds to localhost:port and is only accessible inside a container
hostName = "0.0.0.0"  # an address used to refer to all IP addresses on the same machine
port = 1044
server_URL = "http://"+hostName+":"+str(port)

logs_filename = "logs.dat" # each line is JSON

headers = {"charset": "utf-8", "Content-Type": "application/json"}

def print_request(self):
    print("\nself.path =", self.path)
    # self.path = /
    # query_components = {}
    # or
    # self.path = /?action=yes
    # query_components = {'action': ['yes']}

    print('content type:',self.headers.get('content-type'))

    # https://pymotw.com/3/urllib.parse/
    print(urlparse(self.path).path)

    query_components = parse_qs(urlparse(self.path).query)
    print("query_components =", query_components)
    return

class MyServer(BaseHTTPRequestHandler):

    def end_headers(self):
        """
        allow HTML page to violate CORS

        https://gist.github.com/acdha/925e9ffc3d74ad59c3ea
        see also
        https://stackoverflow.com/a/21957017/1164295
        """
        self.send_header('Access-Control-Allow-Origin', '*')
        #self.send_header('Access-Control-Allow-Methods', 'PUT')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(MyServer, self).end_headers()



    def do_POST(self):
        """
        for receiving log data
        """
        print_request(self)

        # refuse to receive non-json content
        if self.headers.get("content-type") != "application/json":
            self.send_response(400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary
        length = int(self.headers.get("content-length"))

        print('length:',self.headers.get('content-length'))

        message = json.loads(self.rfile.read(length))

        print("message = ", message)

        with open(logs_filename, "a") as file_handle:
            file_handle.write(str(message) + "\n")

        # send the message back
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>POSTED JSON</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request received by server was %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes(json.dumps(message) + "\n", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


#        self.wfile.write(bytes(json.dumps({'hello': 'world', 'received': 'ok'}),"utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, port), MyServer)
    print("Server started %s" % (server_URL))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close()
        print("Server stopped.")
