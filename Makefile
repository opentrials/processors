.PHONY: all build deploy deploy_travis list start test dump_schemas restore_schemas up

all: list

COMMIT := $(shell git rev-parse HEAD)
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
DOCKER_REPO := opentrials/processors

build:
	docker build \
		-t ${DOCKER_REPO}:${COMMIT} \
		--build-arg SOURCE_COMMIT=${COMMIT} \
		.
ifeq ("${BRANCH}", "master")
	docker tag ${DOCKER_REPO}:${COMMIT} ${DOCKER_REPO}:latest
endif

deploy: build
	docker push ${DOCKER_REPO}:${COMMIT}
ifeq ("${BRANCH}", "master")
	docker push ${DOCKER_REPO}:latest
endif

deploy_travis: build
	docker login -e ${DOCKER_EMAIL} -u ${DOCKER_USER} -p ${DOCKER_PASS}
	docker push ${DOCKER_REPO}:${COMMIT}
ifeq ("${BRANCH}", "master")
	docker push ${DOCKER_REPO}:latest
endif

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
