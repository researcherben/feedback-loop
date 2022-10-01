mytag=py_webservices

#
.PHONY: help clean \
	webserver.py \
	background_process_to_update_state_and_metrics.py 

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
	docker run -it --rm -v`pwd`:/scratch -p 1033:1033 -w/scratch $(mytag) /bin/bash

viz_Makefile:
	makefile2dot | dot -Tpng > Makefile_viz.png

webserver.py:
	docker run -it --rm -v`pwd`:/scratch -p 1033:1033 -w/scratch $(mytag) python3 webserver.py

background_process_to_update_state_and_metrics.py:
	docker exec -it `docker ps | grep $(mytag) | cut -d' ' -f1` python3 background_process_to_update_state_and_metrics.py

clean:
	rm -rf __pycache__ *.dat *.json
