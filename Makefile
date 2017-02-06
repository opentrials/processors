.PHONY: all build list start test up

all: list

build:
	docker build -t opentrials/processors .

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
