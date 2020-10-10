
In one terminal, use

    make docker_live

to get the master started. In that container, start the server 

    python3 server_zmq.py

Then, in a separate terminal, use

    docker exec -it `docker ps | grep zmq_phusion | cut -d' ' -f1` /bin/bash

to enter the running container; then start the client using

    python3 client_zmq.py


