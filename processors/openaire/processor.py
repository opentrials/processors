# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from datapackage import pull_datapackage
logger = logging.getLogger(__name__)


# Module API

def process(conn):

    # View/table
    query = """
        create table export_openaire_jp as
        select t.id, t.primary_register, t.primary_id, t.secondary_ids,
        t.scientific_title, t.public_title, t.description, t.brief_summary,
        t.registration_date, t.target_sample_size,
        array_agg(distinct r.primary_id) filter(where r.primary_id is not null) as identifiers,
        array_to_json(array_agg(json_build_object('url', r.source_url, 'sourceID', s.id, 'sourceName', s.name))) as jsonProv
        from trials as t
        left outer join trialrecords as r on t.id = r.trial_id
        left outer join sources as s on r.source_id = s.id
        group by t.id, t.primary_register, t.primary_id, t.secondary_ids,
        t.scientific_title, t.public_title, t.description, t.brief_summary,
        t.registration_date, t.target_sample_size;
    """
    conn.database.engine.execute(query)

    # Import
    pull_datapackage(
        descriptor='target/openaire/datapackage.json', name='export',
        backend='sql', engine=conn.database.engine, prefix='export_')

    # Log
    logger.info('Exported datapackage for OpenAIRE.')
