
## Terminal 1

Launch the container and the "origin" server

    docker run -it --rm -v`pwd`:/scratch -p 1044:1044 -p 1033:1033 -w/scratch py_webservices python3 webpage44.py


## Terminal 2

Using the same container, launch the met server

    docker exec -it `docker ps | grep py_web | cut -d' ' -f1` python3 webpage33.py

## Terminal 3

Using the same container, start the application

    docker exec -it `docker ps | grep py_web | cut -d' ' -f1` python3 runme.py


## Web browser

Open a browser tab

    localhost:1044

and

    localhost:1033


# Troubleshooting

Verify port forwarding to host using

    docker port `docker ps | grep py_web | cut -d' ' -f1`
    1033/tcp -> 0.0.0.0:1033
    1044/tcp -> 0.0.0.0:1044

Connect to the same container

    docker exec -it `docker ps | grep py_web | cut -d' ' -f1` /bin/bash
