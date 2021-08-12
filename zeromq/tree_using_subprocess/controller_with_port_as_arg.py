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
import subprocess  # https://stackoverflow.com/questions/39187886/what-is-the-difference-between-subprocess-popen-and-subprocess-run/39187984

context = zmq.Context()

#print('arg count = ', len(sys.argv))
if len(sys.argv)!=3:
    print("incorrect argument supplied\nNeed to provide port as integer between 1000 and 9999")

controller_port_as_str = sys.argv[1]
#print('controller_port_as_str =', controller_port_as_str)
try:
    controller_port_as_int = int(controller_port_as_str)
except ValueError as err:
    raise Exception("port needs to be an integer", str(err))

if controller_port_as_int<1000 or controller_port_as_int>9999:
    raise Exception("port needs to be between 1000 and 9999")

num_devices_as_str = sys.argv[2]
try:
    num_devices = int(num_devices_as_str)
except ValueError as err:
    raise Exception("num devices needs to be an integer", str(err))

if num_devices>5:
    print("warning: large number of processes")

# REP will block on recv unless it has received a request.
socket_primary = context.socket(zmq.REP)
socket_primary.bind("tcp://*:"+str(controller_port_as_int))


device_port_list = [controller_port_as_int+x for x in range(1, num_devices+1)]
print("device_port_list for controller",controller_port_as_int,"is",device_port_list)

for device_port in device_port_list:
    process = subprocess.Popen( # https://stackoverflow.com/questions/10965949/can-subprocess-call-be-invoked-without-waiting-for-process-to-finish?rq=1
        ["python3", "device_with_port_as_arg.py", str(device_port)],
        #stdout=PIPE, stderr=PIPE, timeout=proc_timeout,
        stdin=None, stdout=None, stderr=None, close_fds=True # https://stackoverflow.com/questions/3516007/run-process-and-dont-wait
    )
    print("controller",controller_port_as_int,"initiated",device_port)

device_socket_dict = {}
# now we can connect to the initialized devices
for device_port in device_port_list:
    device_socket_dict[device_port] = context.socket(zmq.REQ)
    device_socket_dict[device_port].connect("tcp://localhost:"+str(device_port))

while True:
    #  Wait for next request from client
    message = socket_primary.recv()
    print("Controller %s Received request %s from primary" % (controller_port_as_str, message))

    if 'bye' in str(message):
        #  Do some 'work'
        time.sleep(1)
        #  Send reply back to client
        socket_primary.send(b"Controller %s completed %s" % (str.encode(controller_port_as_str), message))
    else:
        socket_primary.send(b"Controller %s launched %s" % (str.encode(controller_port_as_str), message))
