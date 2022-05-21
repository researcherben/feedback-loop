#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#
# from https://zeromq.org/languages/python/

import time
import zmq
import sys

context = zmq.Context()

print("arg count = ", len(sys.argv))
if len(sys.argv) != 2:
    print("incorrect argument supplied")

port_as_str = sys.argv[1]
print("port_as_str =", port_as_str)

# REP will block on recv unless it has received a request.
socket = context.socket(zmq.REP)
socket.bind("tcp://*:" + port_as_str)

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"World")
