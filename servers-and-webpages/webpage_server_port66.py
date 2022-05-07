#!/usr/bin/env python3

import time
import json
import random
import os
import requests
import datetime

# https://docs.python.org/3/library/http.server.html
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler

from urllib.parse import urlparse
from urllib.parse import parse_qs

import runme

"""
This web server returns an HTML file (for GET requests) with a random value

To send a dictionary on the command line,
curl --data '{"this":"is a test"}' --header "Content-Type: application/json" http://localhost:1055

from https://pythonbasics.org/webserver/
and https://gist.github.com/nitaku/10d0662536f37a087e1b

how to server HTML files:
https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/
"""

#hostName = "localhost" # if this is used, then server binds to localhost:port and is only accessible inside a container
hostName = "0.0.0.0" # an address used to refer to all IP addresses on the same machine
serverPort = 1066

# # https://stackoverflow.com/a/39801780/1164295
# web_dir = os.path.join(os.path.dirname(__file__), 'webpages')
# os.chdir(web_dir)

origin_hostName = "localhost"
origin_serverPort = 1044
origin_url = 'http://'+origin_hostName+':'+str(origin_serverPort)

met_hostName = "localhost"
met_serverPort = 1033
met_url = 'http://'+met_hostName+':'+str(met_serverPort)

headers = {"charset": "utf-8", "Content-Type": "application/json"}



class MyServer(SimpleHTTPRequestHandler):

# slow chrome load
# https://stackoverflow.com/a/5273870/1164295
# didn't work
    # def address_string(self):
    #     host, port = self.client_address[:2]
    #     #return socket.getfqdn(host)
    #     return host

    def do_GET(self):
        #print('content type:',self.headers.get('content-type'))

        msg = None

        print("self.path =",self.path)
        # self.path = /
        # query_components = {}
        # or
        # self.path = /?action=yes
        # query_components = {'action': ['yes']}

        # Extract query param
        query_components = parse_qs(urlparse(self.path).query)
        print("query_components =", query_components)

        #if self.path == "/":
        #self.path = '/webpages/server_options.html'


        if 'action' in query_components:
            action = query_components["action"][0]
            print("action =", action)

            if action=="start":
                print("status = ",runme.start())
            elif action=="stop":
                print("status = ",runme.stop())
            else:
                #self.path = 'error_unrecognized_action.html'
                print("action =", action)
                msg = "ERROR: unrecognized action"
        else: # no action specified
            print("no action specified; not going to do anything")
            pass


        if runme.query_state()=="on":
            # get next from que
            print("on!")
            print("sending request to user")
            r = requests.post(origin_url, json={"hello":"world"}, headers=headers)
            data = r.json()
            print("got",data)

            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#            print("now=",now)

            print("sending record to met")
            r = requests.post(met_url, json={"%Y-%m-%d %H:%M:%S":now}, headers=headers)


            if "msg" in data.keys():
                print("msg = ",str(data["msg"]))
            else:
                # TODO: kill this if an interrupt comes in via POST
                # https://blog.miguelgrinberg.com/post/how-to-make-python-wait
                # https://www.google.com/search?q=python+launch+function+in+background+wait+for+response
                print("running")
                res = runme.doit(data["jb"]['val'])
                # TODO: send fake tts per phase to met
                print("res =", res)
                if res:
                    print("sending res to met")
                    r = requests.post(met_url, json={"%Y-%m-%d %H:%M:%S":now, "res": res}, headers=headers)

            """
                r = requests.post(origin_url, json={"hello":"world"}, headers=headers)
                #print(r.text)
                #print(r.json())

                data = r.json()
                print("got",data)

                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("now=",now)

                r = requests.post(met_url, json={"%Y-%m-%d %H:%M:%S":now}, headers=headers)
            """

            # # Writing the HTML contents with UTF-8
            # self.wfile.write(bytes("hello", "utf8"))
            # return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html>\n", "utf-8"))
        self.wfile.write(bytes("    <head>\n", "utf-8"))
        self.wfile.write(bytes("       <title>user 44</title>\n", "utf-8"))
        # https://en.wikipedia.org/wiki/Meta_refresh
#        self.wfile.write(bytes("       <meta http-equiv=\"refresh\" content=\"5\" />\n", "utf-8"))
        self.wfile.write(bytes("    </head>\n", "utf-8"))
        self.wfile.write(bytes("<body>\n", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s<BR>\n" % self.path, "utf-8"))
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.wfile.write(bytes("at %s</p>\n" % now, "utf-8"))
        self.wfile.write(bytes("\n", "utf-8"))
        self.wfile.write(bytes("<H2>S</H2>\n", "utf-8"))

        current_status = runme.query_state()
        self.wfile.write(bytes("<P>status: "+str(current_status)+"</P>\n", "utf-8"))

        self.wfile.write(bytes("  <P>actions for s:</P>\n", "utf-8"))
        self.wfile.write(bytes("    <UL>\n", "utf-8"))
        if current_status=="on":
            self.wfile.write(bytes("      <LI><a href=\"http://localhost:1066?action=stop\">stop</a></LI>\n", "utf-8"))
        if current_status=="off":
            self.wfile.write(bytes("      <LI><a href=\"http://localhost:1066?action=start\">start</a></LI>\n", "utf-8"))
        self.wfile.write(bytes("    </UL>\n", "utf-8"))
        if msg:
            self.wfile.write(bytes("<p>MESSAGE = "+str(msg)+"</p>\n", "utf-8"))
        self.wfile.write(bytes("</body></html>\n\n", "utf-8"))


#        return SimpleHTTPRequestHandler.do_GET(self)


    # POST echoes the message adding a JSON field
    def do_POST(self):
        #print('content type:',self.headers.get('content-type'))

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



        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>server 66</title></head>", "utf-8"))
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
