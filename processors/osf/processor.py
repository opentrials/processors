# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import time
import logging
import requests
import datetime
from .. import base
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):

    # Log started
    logger.info('Started trials export')

    # Export trials
    # http://jamdb.readthedocs.io/en/latest/index.html
    count = 0
    limit = 100
    token_ttl_seconds = 30*60  # api has limit 60*60 seconds
    token_issued_time = datetime.datetime.now()
    session = requests.Session()
    for trials in _read_trial_groups(conn, limit=limit):

        # Get trial ids for logging errors
        trial_ids = [trial['id'] for trial in trials]

        try:

            # Ensure authenticated
            if (datetime.datetime.now() - token_issued_time).seconds > token_ttl_seconds:
                del session.headers['Authorization']
            if 'Authorization' not in session.headers:
                url = '%s/auth' % conf['OSF_URL']
                res = session.post(url, json={
                  'data': {
                    'type': 'users',
                    'attributes': {
                      'provider': 'osf',
                      'access_token': conf['OSF_KEY'],
                    }
                  }
                })
                # Check status
                # 200 - ok
                if res.status_code not in [200]:
                    raise RuntimeError('Can\'t authenticate')
                token = res.json()['data']['attributes']['token']
                token_issued_time = datetime.datetime.now()
                session.headers.update({'Authorization': token})
                logger.info('Successfully authenticated')

            # Ensure collection exists
            url = '%s/namespaces/%s/collections'
            url = url % (conf['OSF_URL'], conf['OSF_NAMESPACE'])
            res = session.post(url, json={
                'data': {
                    'id': 'trials',
                    'type': 'collections',
                    'attributes': {},
                }
            })
            # Check status
            # 201 - created
            # 409 - conflict (already exists)
            if res.status_code == 201:
                logger.info('Created collection "trials"')
            elif res.status_code not in [409]:
                raise RuntimeError('Can\'t create "trials" collection')

            # Export trials
            # We use bulk post
            # https://github.com/CenterForOpenScience/jamdb/blob/master/features/document/create.feature#L244
            url = '%s/namespaces/%s/collections/trials/documents'
            url = url % (conf['OSF_URL'], conf['OSF_NAMESPACE'])
            data = []
            for trial in trials:
                data.append({
                    'id': trial['id'],
                    'type': 'documents',
                    'attributes': json.loads(json.dumps(
                        trial, cls=base.helpers.JSONEncoder)),
                })
            res = session.post(url, json={'data': data}, headers={
                'Content-Type': 'application/vnd.api+json; ext="bulk"',
            })
            # Check status
            # 201 - created
            # 409 - conflict (already exists)
            if res.status_code not in [201, 409]:
                raise RuntimeError('Can\'t create "trial" documents: %s/%s', res.json(), trial_ids)
            count += len(trials)
            logger.info('Exported %s trials', count)

        except Exception:
            base.config.SENTRY.captureException()
            time.sleep(5*60)
            continue

    # Log finished
    logger.info('Finished trials export')


# Internal

def _read_trial_groups(conn, limit=100):
    """Yields lists of trials with max limit length.
    """
    QUERY = """
        SELECT
        t.id::text,
        t.brief_summary,
        t.description,
        t.first_enrollment_date,
        t.gender,
        t.has_published_results,
        t.identifiers,
        t.public_title,
        t.recruitment_status,
        t.registration_date,
        t.scientific_title,
        t.target_sample_size,
        coalesce(json_agg(l.*) FILTER (WHERE l.id is not NULL), '[]') as locations,
        coalesce(json_agg(c.*) FILTER (WHERE c.id is not NULL), '[]'::json) as conditions,
        coalesce(json_agg(i.*) FILTER (WHERE i.id is not NULL), '[]'::json) as interventions,
        coalesce(json_agg(g.*) FILTER (WHERE g.id is not NULL), '[]'::json) as organisations,
        coalesce(json_agg(p.*) FILTER (WHERE p.id is not NULL), '[]'::json) as persons
        FROM trials t
        LEFT JOIN trials_locations as tl ON t.id = tl.trial_id LEFT JOIN locations l ON l.id = tl.location_id
        LEFT JOIN trials_conditions as tc ON t.id = tc.trial_id LEFT JOIN conditions c ON c.id = tc.condition_id
        LEFT JOIN trials_interventions as ti ON t.id = ti.trial_id LEFT JOIN interventions i ON i.id = ti.intervention_id
        LEFT JOIN trials_organisations as tg ON t.id = tg.trial_id LEFT JOIN organisations g ON g.id = tg.organisation_id
        LEFT JOIN trials_persons as tp ON t.id = tp.trial_id LEFT JOIN persons p ON p.id = tp.person_id
        GROUP BY t.id
        ORDER BY t.id
        LIMIT {limit}
        OFFSET {offset}
    """
    offset = 0
    while True:
        query = QUERY.format(limit=limit, offset=offset)
        trials = list(conn['database'].query(query))
        if not trials:
            break
        yield trials
        offset += limit
