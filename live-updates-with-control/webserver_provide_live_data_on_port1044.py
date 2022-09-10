#!/usr/bin/env python3

import time
import json
import random
import datetime
import requests
import os

import functions_to_query_and_change_state_of_machine as query_and_change_state

# https://docs.python.org/3/library/http.server.html
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler

from urllib.parse import urlparse
from urllib.parse import parse_qs

"""
This web server returns either an HTML file (for GET requests) with a random value
or, for PUT requests, a modified JSON file

To send a dictionary on the command line,
curl --data '{"this":"is a test"}' --header "Content-Type: application/json" http://localhost:1055


from https://pythonbasics.org/webserver/
and https://gist.github.com/nitaku/10d0662536f37a087e1b

how to serve HTML files:
https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/
"""

# hostName = "localhost" # if this is used, then server binds to localhost:port and is only accessible inside a container
hostName = "0.0.0.0"  # an address used to refer to all IP addresses on the same machine
port = 1044

headers = {"charset": "utf-8", "Content-Type": "application/json"}


class MyServer(SimpleHTTPRequestHandler):

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

    # slow chrome load
    # https://stackoverflow.com/a/5273870/1164295
    # didn't work
    # def address_string(self):
    #     host, port = self.client_address[:2]
    #     #return socket.getfqdn(host)
    #     return host

    def do_GET(self):
        # print('content type:',self.headers.get('content-type'))

        # refuse to receive non-json content
        # if self.headers.get("content-type") != "application/json":
        #     self.send_response(400)
        #     self.end_headers()
        #     return

        # read the message and convert it into a python dictionary
        #length = int(self.headers.get("content-length"))

        # print('length:',self.headers.get('content-length'))

        #message = json.loads(self.rfile.read(length))

        #print("recvd message = ", message)

        state = query_and_change_state.query_state()

        try:
            with open("met.json", "r") as file_handle:
                data = json.load(file_handle)
        except FileNotFoundError:
            data = {"key1": "N/A"}
            with open("met.json", "w") as file_handle:
                json.dump(data, file_handle)

        message = {"state": state, "met": data['key1']}

        # send the message back
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(message) + "\n", "utf-8"))


#        self.wfile.write(bytes(json.dumps({'hello': 'world', 'received': 'ok'}),"utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, port), MyServer)
    print("Server started http://%s:%s" % (hostName, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close()
        print("Server stopped.")

# EOF
