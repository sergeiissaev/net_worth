#!/usr/bin/env bash
PROJECT=finances

# Default commands
build: docker_build

docker_build:
	docker build . -t $(PROJECT)

docker_run:
	docker run -it --network host -v $(shell pwd):/opt/finances $(PROJECT)

docker_bash:
	docker run -it --network host -v $(shell pwd):/opt/finances $(PROJECT) bash

docker_test:
	docker run -it --network host -v $(shell pwd):/opt/finances $(PROJECT) pytest --cov=finances


deploy:
	docker-compose up -d --build

docker_down:
	docker-compose down
