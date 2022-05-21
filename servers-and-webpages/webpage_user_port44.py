#!/usr/bin/env python3

import time
import json
import random
import datetime
import requests
import os

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

server_URL = "http://localhost:1066"
user_URL = "http://localhost:" + str(port)

# # https://stackoverflow.com/a/39801780/1164295
# web_dir = os.path.join(os.path.dirname(__file__), 'webpages')
# os.chdir(web_dir)


def read_que(filename: str) -> dict:
    with open(filename, "r") as file_handle:
        data = json.load(file_handle)
    return data


def write_que(filename: str, data: dict) -> None:
    with open(filename, "w") as file_handle:
        json.dump(data, file_handle)
    return


def max_current_id(data: dict) -> str:
    """ """
    max_id = 0
    for entry in data["jb"]:
        if max_id < int(entry["id"]):
            max_id = int(entry["id"])
    return max_id


def index_of_min_current_id(data: dict) -> str:
    """ """
    min_id = 1000000000
    for index, entry in enumerate(data["jb"]):
        if min_id > int(entry["id"]):
            min_id = int(entry["id"])
            index_of_min_id = index
    return index_of_min_id


def get_next_jb(data: dict):
    print("que init =", data["jb"])
    if len(data["jb"]) > 0:

        jb_list = data["jb"]
        print("jb_list =", jb_list)

        index_of_next_id = index_of_min_current_id(data)
        print("next_id =", index_of_next_id)

        nextjb = jb_list[index_of_next_id]
        print("next =", nextjb)

        del jb_list[index_of_next_id]

        write_que("que.json", {"jb": jb_list})
    else:
        nextjb = None
    return nextjb


def list_qu(filename: str) -> str:
    data = read_que("que.json")
    msg = "jbs:<BR>"
    for entry in data["jb"]:
        msg += str(entry) + "<BR>"
    return msg


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
            if action == "new":
                if "val" in query_components:
                    val = query_components["val"][0]  # user input
                    print("val =", val)
                    data = read_que("que.json")
                    data["jb"].append(
                        {
                            "id": str(max_current_id(data) + 1),
                            "pr": "norm",
                            "val": str(val),
                        }
                    )
                    print("revised data =", data)
                    write_que("que.json", data)
                    msg = list_qu("que.json")
                else:
                    msg = "missing 'val' argument"

            elif action == "del":
                if "id" in query_components:
                    id_to_del = query_components["id"][0]
                    print("id to del =", id_to_del)
                    data = read_que("que.json")
                    list_of_jobs = data["jb"]
                    indices = []
                    for index, this_job in enumerate(list_of_jobs):
                        if this_job["id"] == id_to_del:
                            indices.append(index)
                    del list_of_jobs[
                        indices[0]
                    ]  # there shouldn't be more than one instance of the index
                    write_que("que.json", {"jb": list_of_jobs})
                else:
                    msg = "missing 'id' argument"

            elif action == "clearq":
                write_que("que.json", {"jb": []})

            elif action == "terminate_current":
                r = requests.post(server_URL, json={"msg": "halt"}, headers=headers)
                print(r.json())

            elif action == "inter":
                val = query_components["val"][0]
                print("val =", val)
                data = read_que("que.json")
                jb = {
                    "id": str(max_current_id(data) + 1),
                    "pr": "inter",
                    "val": str(val),
                }
                print("jb =", jb)
                r = requests.post(server_URL, json=jb, headers=headers)
                print(r.json())

            elif action == "listq":
                msg = list_qu("que.json")

            else:
                print("action =", action)
                # self.path = 'error_unrecognized_action.html'
                msg = "ERROR: unrecognized action"

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
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.wfile.write(bytes("at %s</p>\n" % now, "utf-8"))
        self.wfile.write(bytes("\n", "utf-8"))
        self.wfile.write(bytes("<H2>U</H2>\n", "utf-8"))
        self.wfile.write(
            bytes('<a href="http://localhost:1044">reload page</a>\n', "utf-8")
        )
        self.wfile.write(bytes("  <P>actions for u:</P>\n", "utf-8"))
        self.wfile.write(bytes("    <UL>\n", "utf-8"))
        self.wfile.write(
            bytes(
                '      <LI><a href="http://localhost:1044?action=new&val=6">new</a></LI>\n',
                "utf-8",
            )
        )
        self.wfile.write(
            bytes(
                '      <LI><a href="http://localhost:1044?action=del&id=6">del id from q</a></LI>\n',
                "utf-8",
            )
        )
        self.wfile.write(
            bytes(
                '      <LI><a href="http://localhost:1044?action=inter&val=7">inter</a></LI>\n',
                "utf-8",
            )
        )
        self.wfile.write(
            bytes(
                '      <LI><a href="http://localhost:1044?action=terminate_current">terminate current</a></LI>\n',
                "utf-8",
            )
        )
        self.wfile.write(
            bytes(
                '      <LI><a href="http://localhost:1044?action=clearq">clear q</a></LI>\n',
                "utf-8",
            )
        )
        self.wfile.write(
            bytes(
                '      <LI><a href="http://localhost:1044?action=listq">listq</a></LI>\n',
                "utf-8",
            )
        )
        self.wfile.write(bytes("    </UL>\n", "utf-8"))
        if msg:
            self.wfile.write(bytes("<p>MESSAGE = " + str(msg) + "</p>\n", "utf-8"))
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
