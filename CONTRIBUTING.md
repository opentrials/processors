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

## Testing

#### Set up testing environment
  1. Create the test databases given as value for `TEST_WAREHOUSE_URL` and `TEST_DATABASE_URL`
  in your `.env` file.

  2. Populate test databases with their corresponding schema:

    General command:

    ```
    $ make restore_schema  TEST_DB_CONNECTION_URL  location/of/schema/file  drop_if_exists(True/False)
    ```

    Example:

    ```
    $ make restore_schema postgres://user:password@host:port/test_warehouse_db_name ./tests/dbs/warehouse_schema_dump.sql True
    ```

#### Run tests:

```
$ make test
```

#### Add tests

  Our testing framework of choice is [pytest](http://doc.pytest.org/en/latest/) combined with [pylama](https://pypi.python.org/pypi/pylama).

  We have several `pytest` fixtures of database entities in `tests/fixtures` that you can use in your tests. Feel free to add more if needed.


#### Update test databases schema

  If your code alters the schema of a database make sure to update its schema file in
  `tests/dbs`.

  General command:

  ```
  $ make dump_schema  DEVELOPMENT_DB_CONNECTION_URL  location/of/schema/file
  ```

  Example:

  ```
  make dump_schema postgres://user:password@host:port/development_database  ./tests/dbs/opentrials_api_schema_dump.sql
  ```

## Running

To run a processor:

```
$ make start <name> [<args>]
```
