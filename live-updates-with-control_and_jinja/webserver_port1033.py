#!/usr/bin/env python3

import time
import os
import json
import random
import datetime

import jinja2

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
port = 1033
server_URL = "http://"+hostName+":"+str(port)

res_filename = "res.dat" # each line is JSON

#headers = {"charset": "utf-8", "Content-Type": "application/json"}

file_loader = jinja2.FileSystemLoader('templates')
env = jinja2.Environment(loader=file_loader)

index_html = env.get_template('index.html')
met_html = env.get_template('met.html')
ui_html = env.get_template('ui.html')


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

        # https://pymotw.com/3/urllib.parse/
        print(urlparse(self.path).path)

        # Extract query param
        query_components = parse_qs(urlparse(self.path).query)
        print("query_components =", query_components)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if str(self.path).startswith("/met"):
            if "action" in query_components:
                action = query_components["action"][0]
                if action == "clear":
                    if os.path.exists(res_filename):
                        os.remove(res_filename)
                else:
                    print("action =", action)
                    # self.path = 'error_unrecognized_action.html'
                    msg = "ERROR: unrecognized action"

            if os.path.exists(res_filename):
                with open(res_filename, "r") as file_handle:
                    log_data_list = file_handle.read().split("\n")
            else:
                log_data_list=[]

            output = met_html.render(request_str = self.path,
                                    this_page_URL=server_URL+"/met",
                                    log_data_list=log_data_list,
                                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.wfile.write(bytes(output, "utf-8"))


        elif str(self.path).startswith("/ui"):

            output = ui_html.render(request_str = self.path,
                                    this_page_URL=server_URL+"/ui",
                                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.wfile.write(bytes(output, "utf-8"))

        else: # "/" or any other path
            output = index_html.render(request_str = self.path,
                                     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.wfile.write(bytes(output, "utf-8"))

        return




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

        with open(res_filename, "a") as file_handle:
            file_handle.write(str(message) + "\n")

        # send the message back
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>33</title></head>", "utf-8"))
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
