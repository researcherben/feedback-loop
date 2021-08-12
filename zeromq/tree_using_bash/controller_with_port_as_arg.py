#!/usr/bin/python3

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

#print('arg count = ', len(sys.argv))
if len(sys.argv)!=2:
    print("incorrect argument supplied\nNeed to provide port as integer between 1000 and 9999")

port_as_str = sys.argv[1]
#print('port_as_str =', port_as_str)
try:
    port_as_int = int(port_as_str)
except ValueError as err:
    raise Exception("port needs to be an integer", str(err))

if port_as_int<1000 or port_as_int>9999:
    raise Exception("port needs to be between 1000 and 9999")

# REP will block on recv unless it has received a request.
socket = context.socket(zmq.REP)
socket.bind("tcp://*:"+str(port_as_int))

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    if 'bye' in str(message):
        #  Do some 'work'
        time.sleep(1)
        #  Send reply back to client
        socket.send(b"completed %s" % message)
    else:
        socket.send(b"launched %s" % message)
