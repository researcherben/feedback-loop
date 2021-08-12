

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
	docker build -t zmq_phusion .

docker_live:
	docker run -it --rm -v`pwd`:/scratch \
	-w /scratch \
	--entrypoint='' \
	zmq_phusion /bin/bash
