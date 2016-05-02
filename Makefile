.PHONY: all build install list push start test


all: list

build:
	docker build -t okibot/processors .

install:
	pip install --upgrade -r requirements.dev.txt

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

start:
	python -m processors.base.cli $(filter-out $@,$(MAKECMDGOALS))

test:
	pylama processors
	py.test

%:
	@:
