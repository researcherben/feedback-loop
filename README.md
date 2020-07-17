# about

create feedback loops with distinct applications

## brainstorming options
how to implement feedback loops with modular components
 * files on disk as messaging queues
 * Docker container per module with API calls
 * rabbitMQ with RPC pattern; see https://www.rabbitmq.com/getstarted.html and https://www.rabbitmq.com/tutorials/tutorial-six-python.html
 * sockets; see https://docs.python.org/3/howto/sockets.html and https://realpython.com/python-sockets/ and https://www.geeksforgeeks.org/socket-programming-python/
 * pure Python RPC; see https://www.tutorialspoint.com/python_network_programming/python_remote_procedure_call.htm

Notes:
 * Sockets, RPC, API all lack message queue
 * For comparison of Message queue software, see https://stackoverflow.com/questions/731233/activemq-or-rabbitmq-or-zeromq-or ; old thread from 2015: https://news.ycombinator.com/item?id=9634801
 * REST API is stateless

## How to choose between REST API and RPC
https://cloud.google.com/blog/products/application-development/rest-vs-rpc-what-problems-are-you-trying-to-solve-with-your-apis
https://etherealbits.com/2012/12/debunking-the-myths-of-rpc-rest/
https://apihandyman.io/do-you-really-know-why-you-prefer-rest-over-rpc/
https://apisyouwonthate.com/blog/picking-the-right-api-paradigm
https://www.smashingmagazine.com/2016/09/understanding-rest-and-rpc-for-http-apis/
"If an API is mostly actions, maybe it should be RPC.
 If an API is mostly CRUD and is manipulating related data, maybe it should be REST."


## rabbitMQ with Python and Docker

send-recv queue minimal demo:
https://github.com/dmaze/docker-rabbitmq-example
may want to use "depends_on" in docker-compose; see https://stackoverflow.com/a/61524908/1164295
