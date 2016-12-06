# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import uuid
from copy import deepcopy
import processors.fda_linker.processor as processor


class TestFDALinkerProcessor(object):
    @pytest.mark.parametrize('list_of_identifiers,unique_identifiers', [
        ([{'nct': 'NCT00020500'}, {'nct': 'NCT00020500'}], [{'nct': 'NCT00020500'}]),
        ([], []),
    ])
    def test_select_unique_identifiers(self, list_of_identifiers, unique_identifiers):
        assert processor.select_unique_identifiers(list_of_identifiers) == unique_identifiers


    def test_process_links_documents_and_trials(self, conn, fda_document, first_trial, second_trial):
        document_record = conn['database']['documents'].find_one(id=fda_document)
        file_attrs = {
            'pages': ['There is one NCT09090800 and one NCT24681012.'],
            'id': document_record['file_id'],
        }
        conn['database']['files'].update(file_attrs, ['id'])
        processor.process({}, conn)
        linked = conn['database']['trials_documents'].find(document_id=fda_document)
        linked_trials = [uuid.UUID(record['trial_id']).hex for record in linked]

        assert sorted(linked_trials) == sorted([first_trial, second_trial])


    def test_process_updates_link_if_existent(self, conn, fda_document, first_trial):
        document_record = conn['database']['documents'].find_one(id=fda_document)
        file_attrs = {
            'pages': ['NCT09090800 once', 'NCT09090800 twice'],
            'id': document_record['file_id'],
        }
        conn['database']['files'].update(file_attrs, ['id'])
        processor.process({}, conn)
        linked = conn['database']['trials_documents'].find(document_id=fda_document)
        linked_trials = [uuid.UUID(record['trial_id']).hex for record in linked]

        assert linked_trials == [first_trial]


@pytest.fixture
def first_trial(conn, trial, record):
    trial_object = conn['database']['trials'].find_one(id=trial)
    record_object = conn['database']['records'].find_one(id=record)
    new_trial = deepcopy(trial_object)
    trial_attrs = {
        'identifiers': {'nct': 'NCT09090800'},
        'id': uuid.uuid1().hex,
    }
    new_trial.update(trial_attrs)
    new_record = deepcopy(record_object)
    new_record.update(trial_attrs)
    new_record.update({'trial_id': trial_attrs['id']})

    new_trial_id = conn['database']['trials'].insert(new_trial)
    new_record_id = conn['database']['records'].insert(new_record)
    return new_trial_id


@pytest.fixture
def second_trial(conn, trial, record):
    trial_object = conn['database']['trials'].find_one(id=trial)
    record_object = conn['database']['records'].find_one(id=record)
    new_trial = deepcopy(trial_object)
    trial_attrs = {
        'identifiers': {'nct': 'NCT24681012'},
        'id': uuid.uuid1().hex,
    }
    new_trial.update(trial_attrs)
    new_record = deepcopy(record_object)
    new_record.update(trial_attrs)
    new_record.update({'trial_id': trial_attrs['id']})

    new_trial_id = conn['database']['trials'].insert(new_trial)
    new_record_id = conn['database']['records'].insert(new_record)
    return new_trial_id
