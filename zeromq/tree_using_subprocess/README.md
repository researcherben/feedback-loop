
In one terminal, use

    make docker_live

to get the master started. In that container, start the server

    ./kill_every_process_named.sh python3; time python3 primary.py; ./kill_every_process_named.sh python3

To enter the running container, use

    docker exec -it `docker ps | grep zmq_phusion | cut -d' ' -f1` /bin/bash



"A DEALER socket is one that can connect to multiple peers, and uses LRU (least recently used, aka round-robin) to decide which peer gets each message. If you do not want this behavior, then you do not want a DEALER socket with multiple peers."
source: https://stackoverflow.com/a/19432748/1164295
