.PHONY: all build install lint list push test


all: list

build:
	docker build -t okibot/processors .

install:
	pip install --upgrade -r requirements.dev.txt

lint:
	pylama exporter
	pylama mapper

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

push:
	$${CI?"Push is avaiable only on CI/CD server"}
	docker login \
    -e $$OPENTRIALS_DOCKER_EMAIL \
    -u $$OPENTRIALS_DOCKER_USER \
    -p $$OPENTRIALS_DOCKER_PASS
	docker push okibot/processors
	python scripts/push-stacks.py

test:
	py.test
