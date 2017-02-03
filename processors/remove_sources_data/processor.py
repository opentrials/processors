# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from .. import base
logger = logging.getLogger(__name__)


def process(conf, conn):
    '''Remove data from sources.

    We can't delete the sources themselves before removing their trials, but we
    can't remove their trials because they might have other sources as well. So
    we need to:

    1. Run this processor to delete all data from the sources except the
       trials;
    2. Run all other sources' processors to update the remaining trials with
       the data from sources we won't remove;
    3. Run trial_remover to remove trials without records;
    4. Run sources_remover to finally remove the sources themselves.
    '''
    db = conn['database']
    source_ids = _parse_sources(conf['REMOVE_SOURCE_IDS'])

    if not source_ids:
        logger.debug('No sources to remove')
        return

    try:
        logger.debug('Removing data from sources %s', source_ids)
        db.begin()
        _delete_records(db, source_ids)
        _delete_conditions(db, source_ids)
        _delete_documents(db, source_ids)
        _delete_interventions(db, source_ids)
        _delete_locations(db, source_ids)
        _update_fda_applications_organisations_source(db, source_ids)
        _delete_organisations(db, source_ids)
        _delete_persons(db, source_ids)
        _delete_publications(db, source_ids)
    except Exception:
        base.config.SENTRY.captureException()
        logger.debug('Rolling back')
        db.rollback()
    else:
        db.commit()
    finally:
        logger.debug('Done')


def _parse_sources(source_ids_text):
    source_ids = (source_ids_text or '').split(',')
    return tuple([source_id.strip() for source_id in source_ids
                  if source_id.strip()])


def _delete_records(db, source_ids):
    count = db['records'].delete(source_id=source_ids)
    msg = 'Deleted {} records'.format(int(count))
    logger.debug(msg)
    return count


def _delete_conditions(db, source_ids):
    return _delete_trial_related_entity(
        db,
        'conditions',
        'condition_id',
        source_ids
    )


def _delete_documents(db, source_id):
    # FIXME: Have to delete files as well
    num = db['documents'].delete(source_id=source_id)
    msg = 'Deleted {} documents'.format(int(num))
    logger.debug(msg)
    return num


def _delete_interventions(db, source_ids):
    return _delete_trial_related_entity(
        db,
        'interventions',
        'intervention_id',
        source_ids
    )


def _delete_locations(db, source_ids):
    return _delete_trial_related_entity(
        db,
        'locations',
        'location_id',
        source_ids
    )


def _update_fda_applications_organisations_source(db, source_ids):
    '''Change organisations source_id to "fda" for fda_applications orgs

    The fda_applications are related to organisations. Some of them already
    existed when we added FDA applications, coming from other sources. We can't
    simply remove them. However, having the fda_applications linked to them
    means that we could get exactly the same data from FDA. So, instead of
    removing them, we just change their source to "fda".
    '''
    query = '''
        UPDATE organisations
        SET source_id = 'fda'
        WHERE organisations.id IN (
            SELECT organisations.id FROM organisations
            INNER JOIN fda_applications
            ON fda_applications.organisation_id = organisations.id
            WHERE organisations.source_id IN :source_ids
        )
    '''
    logger.debug('Updating organisations source_id to "fda"')
    return db.query(query, source_ids=source_ids)


def _delete_organisations(db, source_ids):
    return _delete_trial_related_entity(
        db,
        'organisations',
        'organisation_id',
        source_ids
    )


def _delete_persons(db, source_ids):
    return _delete_trial_related_entity(
        db,
        'persons',
        'person_id',
        source_ids
    )


def _delete_publications(db, source_ids):
    return _delete_trial_related_entity(
        db,
        'publications',
        'publication_id',
        source_ids
    )


def _delete_trial_related_entity(db, entity_table, entity_table_id, source_ids):
    query = '''
        DELETE FROM trials_{entity_table}
        WHERE
        {entity_table_id} IN (
            SELECT id FROM {entity_table}
            WHERE source_id IN :source_ids
        )
    '''.format(entity_table=entity_table, entity_table_id=entity_table_id)
    db.query(query, source_ids=source_ids)
    logger.debug('Deleted trials_%s' % entity_table)

    num_records = db[entity_table].delete(source_id=source_ids)
    msg = 'Deleted {} {}'.format(int(num_records), entity_table)
    logger.debug(msg)

    return num_records
