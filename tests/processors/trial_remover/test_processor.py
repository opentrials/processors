# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import uuid
from copy import deepcopy
import processors.trial_remover.processor as processor

class TestTrialRemoverProcessor(object):
    def test_remove_trials_without_records_removes_trials(self, conn, conf, trial):
        assert conn['database']['trials'].find_one(id=trial) is not None

        processor.process(conf, conn)
        assert conn['database']['trials'].find_one(id=trial) is None


    def test_remove_trials_without_records_doesnt_remove_trials_with_record(self,
        conn, conf, trial, record):
        record_attrs = {'trial_id': trial, 'id': record}
        conn['database']['records'].update(record_attrs, ['id'])

        processor.process(conf, conn)
        assert conn['database']['trials'].find_one(id=trial) is not None


    def test_delete_related_entities_removes_relation(self, conn, conf, trial, document):
        trial_document = {'document_id': document, 'trial_id': trial}
        conn['database']['trials_documents'].insert(trial_document)

        processor.process(conf, conn)
        assert conn['database']['trials_documents'].find_one(trial_id=trial) is None


    def test_delete_related_documents_removes_documents_without_other_relations(self,
        conn, conf, trial, document):
        trial_document = {'document_id': document, 'trial_id': trial}
        conn['database']['trials_documents'].insert(trial_document)

        processor.process(conf, conn)
        assert conn['database']['document'].find_one(document_id=document) is None


    def test_delete_related_documents_doesnt_remove_documents_with_other_trials(self,
        conn, conf, trial, document, record):
        trial_object = conn['database']['trials'].find_one(id=trial)
        trial_with_record = deepcopy(trial_object)
        trial_with_record['id'] = uuid.uuid1().hex
        conn['database']['trials'].insert(trial_with_record)
        record_attrs = {
            'id': record,
            'trial_id': trial_with_record['id']
        }
        conn['database']['records'].update(record_attrs, ['id'])
        for test_trial in [trial_object, trial_with_record]:
            conn['database']['trials_documents'].insert({
                'document_id': document,
                'trial_id': test_trial['id']
            })

        processor.process(conf, conn)
        assert conn['database']['documents'].find_one(id=document) is not None


    def test_delete_related_documents_doesnt_remove_documents_with_fda_approvals(self,
        conn, conf, trial, fda_document):
        trial_document = {'document_id': fda_document, 'trial_id': trial}
        conn['database']['trials_documents'].insert(trial_document)

        processor.process(conf, conn)
        assert conn['database']['documents'].find_one(id=fda_document) is not None


    def test_delete_related_documents_removes_related_files(self, conn, conf, trial, document):
        trial_document = {'document_id': document, 'trial_id': trial}
        conn['database']['trials_documents'].insert(trial_document)
        file_id = conn['database']['documents'].find_one(id=document)['file_id']

        processor.process(conf, conn)
        assert conn['database']['files'].find_one(file_id=file_id) is None


@pytest.fixture
def conf():
    return {}
