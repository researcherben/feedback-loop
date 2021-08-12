#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
# from https://zeromq.org/languages/python/

# for a discussion on reliability, see
# https://zguide.zeromq.org/docs/chapter4/

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket_dict = {}

# REQ sockets can connect to many servers.
# The requests will be interleaved or distributed to both the servers.
# REQ will block on send unless it has successfully received a reply back.

# Any attempt to send another message to the socket (zmq.REQ/zmq.REP), without having received a reply/request will result in an error
socket_dict[0] = context.socket(zmq.REQ)
socket_dict[0].connect("tcp://localhost:5555")
socket_dict[1] = context.socket(zmq.REQ)
socket_dict[1].connect("tcp://localhost:5556")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s …" % request)
    socket_dict[0].send(b"Hello")
    socket_dict[1].send(b"Bello")

    #  Get the reply.
    message = socket_dict[0].recv()
    print("Received reply %s [ %s ]" % (request, message))
    message = socket_dict[1].recv()
    print("Received reply %s [ %s ]" % (request, message))
