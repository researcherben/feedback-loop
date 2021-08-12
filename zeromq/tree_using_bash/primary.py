#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
# from https://zeromq.org/languages/python/

# for a discussion on reliability, see
# https://zguide.zeromq.org/docs/chapter4/

import zmq
import random

context = zmq.Context()

#  Socket to talk to server
socket_dict = {}

number_of_servers = 10

# REQ sockets can connect to many servers.
# The requests will be interleaved or distributed to both the servers.
# REQ will block on send unless it has successfully received a reply back.

# Any attempt to send another message to the socket (zmq.REQ/zmq.REP),
# without having received a reply/request will result in an error
port_offset = 1000
for server_id in range(number_of_servers):
    socket_dict[server_id] = context.socket(zmq.REQ)
    socket_dict[server_id].connect("tcp://localhost:"+str(port_offset + server_id))

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s …" % request)
    server_id = random.randint(0,number_of_servers-1)
    msg_str = random.choice(['hello', 'greetings', 'bye'])
    socket_dict[server_id].send(b"%s %s" % (str.encode(msg_str), str.encode(str(server_id))))
    #  Get the reply.
    message = socket_dict[server_id].recv()
    print("Received reply %s [ %s ]" % (request, message))
