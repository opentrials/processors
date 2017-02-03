# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from .. import base
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):
    """Removes trials alongs with their related entities (ex: documents)
     if they are not related to any other trial or FDA application.

    NOTE: Please run `remove_unknown_documentcloud_docs` processor after this processor.
    """

    remove_trials_without_records(conf, conn)


def remove_trials_without_records(conf, conn):
    """Remove trials without records"""

    # Prepare
    query = """
        SELECT trials.id, trials.identifiers
        FROM trials LEFT JOIN records ON records.trial_id = trials.id
        WHERE records.trial_id IS NULL AND trials.source_id != 'pubmed'
    """

    # Execute
    count = 0
    error_count = 0
    for trial in conn['database'].query(query):
        trial_id = trial['id'].hex
        remover = _TrialRemover(conf, conn['database'], trial_id)
        conn['database'].begin()
        try:
            remover._delete_related_documents()
            remover._delete_related_conditions()
            remover._delete_related_interventions()
            remover._delete_related_organisations()
            remover._delete_related_persons()
            remover._delete_related_locations()
            remover._delete_related_publications()
            remover._delete_related_risk_of_biases()
            remover._delete_trial()
        except Exception:
            base.config.SENTRY.captureException(extra={
                'trial_id': trial_id,
            })
            conn['database'].rollback()
            error_count += 1
        else:
            conn['database'].commit()
            logger.info('Deleted trial without records: %s and its relations',
                        trial['identifiers'])
            count += 1
        if count and not count % 100:
            logger.info('Removed %s trials without records', count)
    logger.info('Removed %s trials without records', count)
    if error_count > 0:
        logger.warning('Failed to remove %s trials without records', error_count)


class _TrialRemover(object):
    def __init__(self, conf, db, trial_id):
        self._conf = conf
        self._db = db
        self.trial_id = trial_id

    def _delete_trial(self):
        self._db['trials'].delete(id=self.trial_id)

    def _delete_related_documents(self):
        for document in self._delete_related_entities('documents'):
            if document['fda_approval_id'] is None:
                self._db['documents'].delete(id=document['id'])
                self._db['files'].delete(id=document['file_id'])

    def _delete_related_conditions(self):
        for condition in self._delete_related_entities('conditions'):
            self._db['conditions'].delete(id=condition['id'])

    def _delete_related_interventions(self):
        for intervention in self._delete_related_entities('interventions'):
            if intervention['fda_application_id'] is None:
                self._db['interventions'].delete(id=intervention['id'])

    def _delete_related_organisations(self):
        for org in self._delete_related_entities('organisations'):
            self._db['organisations'].delete(id=org['id'])

    def _delete_related_persons(self):
        for person in self._delete_related_entities('persons'):
            self._db['persons'].delete(id=person['id'])

    def _delete_related_locations(self):
        for location in self._delete_related_entities('locations'):
            self._db['locations'].delete(id=location['id'])

    def _delete_related_publications(self):
        for pub in self._delete_related_entities('publications'):
            self._db['publications'].delete(id=pub['id'])

    def _delete_related_risk_of_biases(self):
        linked_robs = self._db['risk_of_biases'].find(trial_id=self.trial_id)
        for rob in linked_robs:
            self._db['risk_of_biases_risk_of_bias_criterias'].delete(risk_of_bias_id=rob['id'])
            self._db['risk_of_biases'].delete(id=rob['id'])

    def _delete_related_entities(self, entity_table, entity_join_table_name=None,
                                join_table=None, trial_join_table_name=None):
        """Delete trial's relations through join table

        Args:
            entity_table: name of entity table
            entity_join_table_name: name of the field that holds the id of the related
                                    entity in the join table (default: {entity}_id)
            join_table: name of join table (default: trials_{entities})
            trial_join_table_name: name of the field that holds the id of the
                                    trial in the join table (default: trial_id)

        """
        if join_table is None:
            join_table = ('trials_%s' % entity_table)
        if entity_join_table_name is None:
            entity_join_table_name = ('%s_id' % entity_table[:-1])
        if trial_join_table_name is None:
            trial_join_table_name = 'trial_id'

        related_entities = self._db[join_table].find(**{trial_join_table_name: self.trial_id})
        self._db[join_table].delete(**{trial_join_table_name: self.trial_id})

        for relation in related_entities:
            entity = self._db[entity_table].find_one(id=relation[entity_join_table_name])
            entity_relations = self._db[join_table].find(**{entity_join_table_name: entity['id']})
            entity_relations = [relation for relation in entity_relations]

            # If the related entity is not attached to other trials, delete it too
            if len(entity_relations) == 0:
                yield entity
