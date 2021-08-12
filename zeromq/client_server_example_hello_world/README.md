
In one terminal, use

```bash
make docker
```

to get the master started. In that container, launch `screen` and then start the server

```bash
python3 server_zmq_5555.py 
```

Then, in a separate terminal, use

```bash
docker exec -it `docker ps | grep zmq_phusion | cut -d' ' -f1` /bin/bash
```

to enter the running container; then start the client using

```bash
python3 client_zmq.py
```


> "A DEALER socket is one that can connect to multiple peers, and uses LRU (least recently used, aka round-robin) to decide which peer gets each message. If you do not want this behavior, then you do not want a DEALER socket with multiple peers."
source: https://stackoverflow.com/a/19432748/1164295
