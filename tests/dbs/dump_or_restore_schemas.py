import os
import subprocess
import argparse
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

DATABASE_SCHEMA_PATH = os.path.join(
    os.path.dirname(__file__),
    'opentrials_api_schema_dump.sql'
)

WAREHOUSE_SCHEMA_PATH = os.path.join(
    os.path.dirname(__file__),
    'warehouse_schema_dump.sql'
)


def dump_schema(postgres_uri, path):
    return subprocess.check_call([
        'pg_dump',
        '--format=plain',
        '--clean',
        '--if-exists',
        '--no-owner',
        '--schema-only',
        '--no-privileges',
        '--file',
        path,
        postgres_uri,
    ])


def restore_schema(postgres_uri, path):
    drop_all_tables(postgres_uri)
    return subprocess.check_call([
        'psql',
        '--quiet',
        '--file',
        path,
        postgres_uri,
    ])


def drop_all_tables(postgres_uri):
    drop_tables_sql = subprocess.Popen([
        'psql',
        '--tuples-only',
        postgres_uri,
        '--command',
        "SELECT 'DROP TABLE \"' || tablename || '\" CASCADE;' FROM pg_tables WHERE schemaname = 'public'",
    ], stdout=subprocess.PIPE)
    output = subprocess.check_output([
        'psql',
        postgres_uri,
    ], stdin=drop_tables_sql.stdout)
    drop_tables_sql.wait()
    return output


def dump_schemas():
    dump_schema(os.environ['DATABASE_URL'], DATABASE_SCHEMA_PATH)
    dump_schema(os.environ['WAREHOUSE_URL'], WAREHOUSE_SCHEMA_PATH)


def restore_schemas():
    restore_schema(os.environ['TEST_DATABASE_URL'], DATABASE_SCHEMA_PATH)
    restore_schema(os.environ['TEST_WAREHOUSE_URL'], WAREHOUSE_SCHEMA_PATH)


parser = argparse.ArgumentParser(
    description='Dump or restore PostgreSQL database schemas'
)
parser.add_argument('action', choices=['dump', 'restore'])
args = parser.parse_args()

if args.action == 'dump':
    dump_schemas()
else:
    restore_schemas()
