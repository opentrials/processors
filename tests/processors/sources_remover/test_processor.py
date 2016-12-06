# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import processors.sources_remover.processor as processor


class TestSourcesRemoverProcessor(object):
    def test_deletes_the_sources(self, conn, fda_source, nct_source):
        sources = [fda_source, nct_source]
        conf = {
            'REMOVE_SOURCE_IDS': ', '.join(sources),
        }

        processor.process(conf, conn)

        sources = [source for source in conn['database']['source'].all()]
        assert sources == []


    def test_rollbacks_if_received_exception(self):
        sources = [
            'source_id1',
            'source_id2',
            'source_id3',
        ]
        conf = {
            'REMOVE_SOURCE_IDS': ', '.join(sources),
        }
        conn = _conn_stub()
        conn['database']['sources'].delete.side_effect = Exception()

        processor.process(conf, conn)

        conn['database'].begin.assert_called()
        conn['database'].rollback.assert_called()


    def test_does_nothing_if_therere_no_sources(self):
        conf = {}
        conn = _conn_stub()

        processor.process(conf, conn)

        conn['database'].begin.assert_not_called()


def _conn_stub():
    conn = {
        'database': mock.MagicMock(),
    }
    conn['database']['sources'] = mock.Mock()
    return conn
