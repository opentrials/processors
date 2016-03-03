.PHONY: all build deploy develop lint list test


all: list

build:
	docker build -t opentrialsrobot/warehouse .

deploy:
	$${CI?"Deployment is avaiable only on CI/CD server"}
	docker login \
    -e $$OPENTRIALS_DOCKER_EMAIL \
    -u $$OPENTRIALS_DOCKER_USER \
    -p $$OPENTRIALS_DOCKER_PASS
	tutum login \
	-u $$OPENTRIALS_DOCKER_USER \
	-p $$OPENTRIALS_DOCKER_PASS
	docker push opentrialsrobot/warehouse
	python stacks/deploy.py

develop:
	pip install --upgrade -r requirements.dev.txt

lint:
	pylama exporter
	pylama mapper
	pylama processor

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

test:
	py.test
