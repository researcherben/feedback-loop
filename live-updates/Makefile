mytag=py_webservices

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
	@echo "make webpages"


docker: docker_build docker_live
docker_build:
	docker build -t $(mytag) .

docker_live:
	docker run -it --rm -v`pwd`:/scratch -p 1066:1066 -p 1044:1044 -p 1033:1033 -w/scratch $(mytag) /bin/bash

viz_Makefile:
	makefile2dot | dot -Tpng > Makefile_viz.png

user:
	docker run -it --rm -v`pwd`:/scratch -p 1066:1066 -p 1044:1044 -p 1033:1033 -w/scratch  $(mytag) python3 provide_live_data_on_port1044.py


background:
	docker exec -it `docker ps | grep py_web | cut -d' ' -f1` python3 background_process_to_update_state_and_metrics.py



clean:
	rm -rf __pycache__ *.dat
