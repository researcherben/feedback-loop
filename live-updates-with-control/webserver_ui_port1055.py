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
port = 1055

met_url="http://0.0.0.0:1033"

headers = {"charset": "utf-8", "Content-Type": "application/json"}

# # https://stackoverflow.com/a/39801780/1164295
# web_dir = os.path.join(os.path.dirname(__file__), 'webpages')
# os.chdir(web_dir)

javascript="""
<script>
  function startLiveUpdate () {
    const text_state = document.getElementById('state');
    const text_state_datetime = document.getElementById('state_datetime')
    const text_met = document.getElementById('met');
    const text_met_datetime = document.getElementById('met_datetime')

    setInterval(function () {
      // By default, fetch() makes a GET request
      fetch('http://localhost:1044/').then(function (response) {
        return response.json();
      }).then(function (data) {
        console.log(data)
          text_state.textContent = data.state;
          text_met.textContent = data.met;
          // https://tecadmin.net/get-current-date-time-javascript/
          var today = new Date();
          // https://stackoverflow.com/a/3605248/1164295
          var date = today.getFullYear()+'-'+('0'+today.getMonth()+1).slice(-2)+'-'+('0'+today.getDate()).slice(-2);
          var time = ('0'+today.getHours()).slice(-2) + ":" + ('0'+today.getMinutes()).slice(-2) + ":" + ('0'+today.getSeconds()).slice(-2);
          var dateTime = date+'_'+time;
          text_state_datetime.textContent = dateTime;
          text_met_datetime.textContent = dateTime;
      }).catch(function (error) {
         console.log(error);
      });
    }, 2000);
  }

  document.addEventListener('DOMContentLoaded', function () {
    startLiveUpdate();
  });
</script>
"""


class MyServer(SimpleHTTPRequestHandler):

    # slow chrome load
    # https://stackoverflow.com/a/5273870/1164295
    # didn't work
    # def address_string(self):
    #     host, port = self.client_address[:2]
    #     #return socket.getfqdn(host)
    #     return host

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
            print('action =',action)
            if action =="turnon":
                result_of_command = query_and_change_state.poweron_machine("my name", met_url, headers)
                print("result:",result_of_command)
            elif action =="new":
                val="23"
                id="5"
                result_of_command = query_and_change_state.doit("my name",val, id,"soon", met_url, headers)
                print("result:",result_of_command)
            elif action =="turnoff":
                result_of_command = query_and_change_state.poweroff_machine("my name", met_url, headers)
                print("result:",result_of_command)

        state = query_and_change_state.query_state()
        print('state =', state)

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
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.wfile.write(bytes("at %s</p>\n" % now, "utf-8"))
        self.wfile.write(bytes("\n", "utf-8"))
        self.wfile.write(bytes("<H2>UI</H2>\n", "utf-8"))
        self.wfile.write(
            bytes('<a href="http://localhost:'+str(port)+'">reload page</a>\n', "utf-8")
        )

        self.wfile.write(bytes('<P>state: <span id="state">N/A</span> as of <span id="state_datetime"></span></P>\n', "utf-8"))
        self.wfile.write(bytes('<P>met: <span id="met">N/A</span> as of <span id="met_datetime"></span></P>\n', "utf-8"))
        self.wfile.write(bytes("  <P>actions available:</P>\n", "utf-8"))
        self.wfile.write(bytes("    <UL>\n", "utf-8"))

        self.wfile.write(
            bytes(
                '      <LI><a href="http://localhost:1055?action=turnon">turn on</a></LI>\n',
                "utf-8",
            )
        )
        self.wfile.write(
            bytes(
                '      <LI><a href="http://localhost:1055?action=new&val=6">new</a></LI>\n',
                "utf-8",
            )
        )
        self.wfile.write(
            bytes(
                '      <LI><a href="http://localhost:1055?action=turnoff">turn off</a></LI>\n',
                "utf-8",
            )
        )
        self.wfile.write(bytes("    </UL>\n", "utf-8"))
        if msg:
            self.wfile.write(bytes("<p>MESSAGE = " + str(msg) + "</p>\n", "utf-8"))

        self.wfile.write(bytes(javascript, "utf-8"))
        self.wfile.write(bytes("</body></html>\n\n", "utf-8"))

        return

    #        return SimpleHTTPRequestHandler.do_GET(self)

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

        print("recvd message = ", message)

        """
        que.json contains

        {"jb": [
            {"id": "3", "pri": "norm", "val": "3"},
            {"id": "2", "pri": "norm", "val": "4"},
            {"id": "1", "pri": "norm", "val": "5"}
        ]}
        """

        data = read_que("que.json")
        next_jb = get_next_jb(data)

        if next_jb:
            # add a property to the object, just to mess with data
            message["jb"] = next_jb
        else:
            message = {"msg": "nothing in que"}

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
