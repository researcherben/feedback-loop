mytag=zmq_phusion

# 
.PHONY: help clean webserver typehints flake8 pylint doctest mccabe

help:
	@echo "make help"
	@echo "      this message"
	@echo "==== Targets outside container ===="
	@echo "make docker"
	@echo "      build and run docker"
	@echo "make docker_build"
	@echo "make docker_live"
	@echo "      build and run docker /bin/bash"
	@echo "==== Targets inside container ===="


docker: docker_build docker_live
docker_build:
	docker build -t $(mytag) .

docker_live:
	docker run -it --rm -v`pwd`:/scratch \
	-w /scratch \
	--entrypoint='' \
	$(mytag) /bin/bash

5555:
	docker run -it --rm -v`pwd`:/scratch -p 5555:5555 -p 5556:5556 -w/scratch $(mytag) python3 server_zmq_5555.py

5556: 
	docker exec -it `docker ps | grep zmq_ph | cut -d' ' -f1` python3 server_zmq_5556.py

client:
	docker exec -it `docker ps | grep zmq_ph | cut -d' ' -f1` python3 client_zmq.py
