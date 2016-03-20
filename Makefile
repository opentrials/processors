.PHONY: all build deploy develop lint list test


all: list

build:
	docker build -t opentrialsrobot/processors .

deploy:
	$${CI?"Deployment is avaiable only on CI/CD server"}
	docker login \
    -e $$OPENTRIALS_DOCKER_EMAIL \
    -u $$OPENTRIALS_DOCKER_USER \
    -p $$OPENTRIALS_DOCKER_PASS
	tutum login \
	-u $$OPENTRIALS_DOCKER_USER \
	-p $$OPENTRIALS_DOCKER_PASS
	docker push opentrialsrobot/processors
	python scripts/deploy-stacks.py

develop:
	pip install --upgrade -r requirements.dev.txt

lint:
	# TODO: return linting for mapper
	pylama exporter
	# pylama mapper

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

test:
	py.test
