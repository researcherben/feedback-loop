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

import functions_to_query_and_change_state_of_machine as query_and_change_state

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

logs_filename = "logs.dat" # each line is JSON
state_filename="machine_state.json"
met_json = "met.json"

headers = {"charset": "utf-8", "Content-Type": "application/json"}

file_loader = jinja2.FileSystemLoader('templates')
env = jinja2.Environment(loader=file_loader)

index_html = env.get_template('index.html')
logging_html = env.get_template('logs.html')
ui_html = env.get_template('ui.html')

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

    # Disable logging DNS lookups
# https://stackoverflow.com/a/6761844/1164295
    def address_string(self):
        # https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler.client_address
        return str(self.client_address[0])

# https://stackoverflow.com/a/5273870/1164295
# https://bugs.python.org/issue6085
    # def address_string(self):
    #     host, port = self.client_address[:2]
    #     #return socket.getfqdn(host)
    #     return host

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

    def do_GET(self):
        # print('content type:',self.headers.get('content-type'))

        # ignore request to favicon
        if self.path.endswith('favicon.ico'):
            return

        msg = None
        # Extract query param
        query_components = parse_qs(urlparse(self.path).query)


        if str(self.path).startswith("/logs"):
            print_request(self)
            if "action" in query_components.keys():
                action = query_components["action"][0]
                print("action=",action)
                if action == "clear":
                    if os.path.exists(logs_filename):
                        os.remove(logs_filename)
                else:
                    # self.path = 'error_unrecognized_action.html'
                    msg = "ERROR: unrecognized action"

            if os.path.exists(logs_filename):
                with open(logs_filename, "r") as file_handle:
                    log_data_list = file_handle.read().split("\n")
            else:
                log_data_list=[]

            output = logging_html.render(request_str = self.path,
                                    this_page_URL=server_URL+"/logs",
                                    logs_URL=server_URL+"/recent_logs",
                                    log_data_list=log_data_list,
                                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(output, "utf-8"))


        elif str(self.path).startswith("/ui"):
            print_request(self)
            if "action" in query_components.keys():

                action = query_components["action"][0]
                print('action =',action)
                if action =="turnon":
                    result_of_command = query_and_change_state.poweron_machine(
                                   "my name", logs_filename, state_filename)
                    print("result:",result_of_command)
                elif action =="new":
                    val="23"
                    id="5"
                    result_of_command = query_and_change_state.doit(
                        "my name",val, id,"soon",logs_filename, state_filename)
                    print("result:",result_of_command)
                elif action =="turnoff":
                    result_of_command = query_and_change_state.poweroff_machine("my name", logs_filename, state_filename)
                    print("result:",result_of_command)


            output = ui_html.render(request_str = self.path,
                                    server_URL=server_URL,
                                    this_page_URL=server_URL+"/ui",
                                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes(output, "utf-8"))

        elif str(self.path).startswith("/recent_logs"):
            message = ["hello","world"]
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(message) + "\n", "utf-8"))


        elif str(self.path).startswith("/livemetrics"):

            state = query_and_change_state.query_state(state_filename)

            try:
                with open(met_json, "r") as file_handle:
                    data = json.load(file_handle)
            except FileNotFoundError:
                data = {"key1": "not in database"}
                with open(met_json, "w") as file_handle:
                    json.dump(data, file_handle)

            message = {"state": state, "met": data['key1']}

            # send the message back
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(message) + "\n", "utf-8"))


        else: # "/" or any other path
            print_request(self)
            output = index_html.render(request_str = self.path,
                                     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(output, "utf-8"))

        return




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
