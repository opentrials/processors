# Contributing

The project follows the [Open Knowledge International coding standards](https://github.com/okfn/coding-standards).

## Getting Started

```
virtualenv .python -p python2
source .python/bin/activate
make install
cp .env.example .env
editor .env # set your values
set -a; source .env
```

## Building

To build a docker image:

```
$ make build
```

## Testing

To run tests:

```
$ make test
```

## Running

To run a processor:

```
$ make start <name>
```

To run all services:

```
$ make up
```

> To work with docker compose localhost database urls can't be used.
Contributor should config database to accept non localhost connections and
to use `$ ip route | awk '/docker0/ { print $NF }'` output as a host.
