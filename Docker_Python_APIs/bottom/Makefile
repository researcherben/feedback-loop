

#
.PHONY: help clean webserver typehints flake8 pylint doctest mccabe

help:
	@echo "make help"
	@echo "      this message"
	@echo "==== Targets outside container ===="
	@echo "make docker"
	@echo "      build and run docker"
	@echo "make dockerlive"
	@echo "      build and run docker /bin/bash"
	@echo "==== Targets inside container ===="
	@echo "make flask"
	@echo "      start webserver"

ifdef FILE_NAME
	@echo 'FILE_NAME is defined' $(FILE_NAME)
else
	@echo 'FILE_NAME is undefined'
endif

docker:
	docker build -t bottom_phusion .
	docker run -it --rm \
           -v`pwd`:/scratch \
           bottom_phusion

dockerlive:
	docker build -t bottom_phusion .
	docker run -it --rm -v`pwd`:/scratch \
           --entrypoint='' \
           bottom_phusion /bin/bash
