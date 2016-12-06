# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import sys
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


class SchemaDump(object):
    def __init__(self, db_url, schema_file_path):
        self.db_url = db_url
        self.schema_file_path = schema_file_path
        self.buf = io.BytesIO()

    def dump_schema(self):
        engine = create_engine(self.db_url)
        metadata = MetaData()
        metadata.reflect(engine)

        def dump(sql, *multiparams, **params):
            output = sql.compile(dialect=engine.dialect)
            self.buf.write(str(output).strip())
            self.buf.write(b';\n')

        new_engine = create_engine(self.db_url, strategy='mock', executor=dump)
        metadata.create_all(new_engine, checkfirst=True)

        with io.open(self.schema_file_path, 'wb+') as schema_file:
            schema_file.write(self.buf.getvalue())


class RestoreSchema(object):
    def __init__(self, db_url, schema_file_path, drop_if_exists=False):
        self.db_url = db_url
        self.schema_file_path = schema_file_path
        self.drop_if_exists = drop_if_exists
        self.sql_schema = self.load_raw_sql(schema_file_path)

    def restore_schema(self):
        engine = create_engine(self.db_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        if self.drop_if_exists:
            metadata = MetaData(bind=engine)
            metadata.reflect()
            metadata.drop_all()

        conn = engine.connect()
        transaction = conn.begin()
        try:
            conn.execute(self.sql_schema)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e
        finally:
            session.close()

    def load_raw_sql(self, schema_file_path):
        raw_schema = ''
        with io.open(schema_file_path) as sql_schema:
            raw_schema = sql_schema.read()
        if not raw_schema:
            raise ValueError('Schema file can\'t be empty.')
        return raw_schema


if __name__ == "__main__":
    command = sys.argv[1]
    args = sys.argv[2:]
    if command == 'dump_schema':
        d = SchemaDump(*args)
        d.dump_schema()
    elif command == 'restore_schema':
        d = RestoreSchema(*args)
        d.restore_schema()
