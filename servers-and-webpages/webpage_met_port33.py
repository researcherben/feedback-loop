#!/usr/bin/env python3

import time
import os
import json
import random
import datetime

from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.parse import urlparse
from urllib.parse import parse_qs

"""
This web server returns an HTML file (for GET requests) with a random value

To send a dictionary on the command line,
curl --data '{"this":"is a test"}' --header "Content-Type: application/json" http://localhost:1055

from https://pythonbasics.org/webserver/
and https://gist.github.com/nitaku/10d0662536f37a087e1b

how to server HTML files:
https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/
"""

# hostName = "localhost" # if this is used, then server binds to localhost:port and is only accessible inside a container
hostName = "0.0.0.0"  # an address used to refer to all IP addresses on the same machine
port = 1033

res_filename = "res.dat"

headers = {"charset": "utf-8", "Content-Type": "application/json"}


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # print('content type:',self.headers.get('content-type'))

        msg = None

        print("self.path =", self.path)
        # self.path = /
        # query_components = {}
        # or
        # self.path = /?action=yes
        # query_components = {'action': ['yes']}

        # Extract query param
        query_components = parse_qs(urlparse(self.path).query)
        print("query_components =", query_components)

        # if self.path == "/":
        # self.path = '/webpages/user_options.html'

        if "action" in query_components:
            action = query_components["action"][0]
            if action == "clear":
                if os.path.exists(res_filename):
                    os.remove(res_filename)
            else:
                print("action =", action)
                # self.path = 'error_unrecognized_action.html'
                msg = "ERROR: unrecognized action"

        data = []
        if os.path.exists(res_filename):
            with open(res_filename, "r") as file_handle:
                data = file_handle.read().split("\n")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes("<html>\n<head>\n<title>\nmet 33\n</title>\n</head>\n", "utf-8")
        )
        self.wfile.write(bytes("<body>\n", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s<BR>\n" % self.path, "utf-8"))
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.wfile.write(bytes("at %s</p>\n" % now, "utf-8"))
        self.wfile.write(bytes("<H2>M</H2>\n", "utf-8"))
        self.wfile.write(
            bytes(
                '<a href="http://localhost:1033">reload page</a> to view current logs\n',
                "utf-8",
            )
        )
        self.wfile.write(bytes("<p>actions</p>\n", "utf-8"))
        self.wfile.write(bytes("<UL>\n", "utf-8"))
        self.wfile.write(
            bytes(
                '  <LI><a href="http://localhost:1033?action=clear">clear history</a></LI>\n',
                "utf-8",
            )
        )
        self.wfile.write(bytes("</UL>\n", "utf-8"))
        self.wfile.write(bytes("<P>Log entries:</P>\n", "utf-8"))
        for line in data:
            self.wfile.write(bytes(line + "<BR>\n", "utf-8"))
        if msg:
            self.wfile.write(bytes("<p>MESSAGE = " + str(msg) + "</p>\n", "utf-8"))
        self.wfile.write(bytes("</body>\n</html>\n", "utf-8"))

    # POST echoes the message adding a JSON field
    def do_POST(self):
        # print('content type:',self.headers.get('content-type'))

        # refuse to receive non-json content
        if self.headers.get("content-type") != "application/json":
            self.send_response(400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary
        length = int(self.headers.get("content-length"))

        # print('length:',self.headers.get('content-length'))

        message = json.loads(self.rfile.read(length))

        print("message = ", message)

        with open("res.dat", "a") as file_handle:
            file_handle.write(str(message) + "\n")

        # send the message back
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>33</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes(json.dumps(message) + "\n", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


#        self.wfile.write(bytes(json.dumps({'hello': 'world', 'received': 'ok'}),"utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, port), MyServer)
    print("Server started http://%s:%s" % (hostName, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close()
        print("Server stopped.")
