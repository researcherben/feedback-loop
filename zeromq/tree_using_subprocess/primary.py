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
#from subprocess import PIPE  # https://docs.python.org/3/library/subprocess.html
import subprocess  # https://stackoverflow.com/questions/39187886/what-is-the-difference-between-subprocess-popen-and-subprocess-run/39187984

context = zmq.Context()


number_of_controllers = 10
port_offset = 1000
port_step = 100
num_devices = 3
if port_step<=num_devices:
    print("warning: port collision")
proc_timeout = 10 # seconds to wait for subprocess

controller_ports_list = [x + port_offset for x in list(range(0,number_of_controllers*port_step,port_step))]
print("primary's controller_ports_list =",controller_ports_list)

for controller_port in controller_ports_list:
    process = subprocess.Popen( # https://stackoverflow.com/questions/10965949/can-subprocess-call-be-invoked-without-waiting-for-process-to-finish?rq=1
        ["python3", "controller_with_port_as_arg.py", str(controller_port), str(num_devices)],
        #stdout=PIPE, stderr=PIPE, timeout=proc_timeout,
        stdin=None, stdout=None, stderr=None, close_fds=True # https://stackoverflow.com/questions/3516007/run-process-and-dont-wait
    )
    print("primary initiated",controller_port,"with",num_devices)


#  Socket to talk to server
controller_socket_dict = {}

# REQ sockets can connect to many servers.
# The requests will be interleaved or distributed to both the servers.
# REQ will block on send unless it has successfully received a reply back.

# Any attempt to send another message to the socket (zmq.REQ/zmq.REP),
# without having received a reply/request will result in an error
for controller_port in controller_ports_list:
    controller_socket_dict[controller_port] = context.socket(zmq.REQ)
    controller_socket_dict[controller_port].connect("tcp://localhost:"+str(controller_port))

#  Do 10 requests, waiting each time for a confirmation
for request in range(10):
    print("Primary Sending request %s ..." % request)
    server_id = random.choice(controller_ports_list)
    msg_str = random.choice(['hello', 'greetings', 'bye'])
    controller_socket_dict[server_id].send(b"%s %s" % (str.encode(msg_str), str.encode(str(server_id))))
    #  Get the reply.
    message = controller_socket_dict[server_id].recv()
    print("Primary Received reply %s [ %s ]" % (request, message))
