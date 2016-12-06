# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import uuid


@pytest.fixture
def file_fixture(conn):
    sha1 = uuid.uuid1().hex
    file_record = {
        'id': uuid.uuid1().hex,
        'sha1': sha1,
        'source_url': ('http://example.org/file_%s.pdf' % sha1),
    }
    file_id = conn['database']['files'].insert(file_record)
    return file_id


@pytest.fixture
def fda_file(conn):
    sha1 = uuid.uuid1().hex
    file_record = {
        'id':  uuid.uuid1().hex,
        'sha1': sha1,
        'source_url': ('http://datastore.opentrials.net/documents/fda/file_%s.pdf' % sha1),
        'documentcloud_id': 3154193,
        'pages': [],
    }
    file_id = conn['database']['files'].insert(file_record)
    return file_id
