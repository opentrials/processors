.PHONY: all build deploy list start test up

all: list

COMMIT := $(shell git rev-parse HEAD)
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
DOCKER_REPO := 'opentrials/processors'

build:
	docker build \
		-t ${DOCKER_REPO}:${COMMIT} \
		--build-arg SOURCE_COMMIT=${COMMIT} \
		.
ifeq ("${BRANCH}", "master")
	docker tag ${DOCKER_REPO}:${COMMIT} ${DOCKER_REPO}:latest
endif

deploy: build
	docker push ${DOCKER_REPO}

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

start:
	python -m processors.base.cli $(filter-out $@,$(MAKECMDGOALS))

test:
	tox

dump_schemas:
	python tests/dbs/dump_or_restore_schemas.py dump

restore_schemas:
	python tests/dbs/dump_or_restore_schemas.py restore

up:
	docker-compose up

%:
	@:
