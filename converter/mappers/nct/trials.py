# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ... import indexers
from .. import helpers


def map_item_trials(source, target, item):

    id = indexers.index_trial(source,
        nct_id=item['nct_id'],
        scientific_title=item['official_title'],
    )

    helpers.upsert(target['trials'], {
        'id': id,
        'primary_register': 'nct',
        'primary_id': item['nct_id'],
        'secondary_ids': {'others': item['secondary_ids'] },
        'registration_date': item['firstreceived_date'],
        'public_title': item['brief_title'],
        'brief_summary': item['brief_summary'] or '',  # TODO: review
        'scientific_title': item['official_title'],
        'description': item['detailed_description'],
        'recruitment_status': item['overall_status'],
        'eligibility_criteria': item['eligibility'],
        'target_sample_size': item['enrollment_anticipated'],
        'first_enrollment_date': item['start_date'],
        'study_type': item['study_type'],
        'study_design': item['study_design'],
        'study_phase': item['phase'],
        'primary_outcomes': item['primary_outcomes'] or [],
        'secondary_outcomes': item['secondary_outcomes'] or [],
    })

    return id
