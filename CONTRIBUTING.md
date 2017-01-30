# Contributing

The project follows the [Open Knowledge International coding standards](https://github.com/okfn/coding-standards).

## Getting Started

```
virtualenv .python -p python2
source .python/bin/activate
pip install -r requirements.txt
cp .env.example .env
editor .env # set your values
set -a; source .env
```

## Testing

#### Set up testing environment
  1. Create the test databases given as value for `TEST_WAREHOUSE_URL` and `TEST_DATABASE_URL`
  in your `.env` file.

  2. Populate test databases with their corresponding schema:


    ```
    $ make restore_schemas
    ```

#### Run tests:
  1. To run the tests, you need tox installed. We recommend you to install it globally with ```pip install -g tox```

  2. Run the tests:

    ```
    $ tox
    ```

#### Add tests

  Our testing framework of choice is [pytest](http://doc.pytest.org/en/latest/) combined with [pylama](https://pypi.python.org/pypi/pylama).

  We have several `pytest` fixtures of database entities in `tests/fixtures` that you can use in your tests. Feel free to add more if needed.


#### Update test databases schema

  If your code alters the schema of a database make sure to update its schema file in
  `tests/dbs`.

  ```
  $ make dump_schemas
  ```

## Running

To run a processor:

```
$ make start <name> [<args>]
```
