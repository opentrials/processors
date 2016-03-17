# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from .. import base
logger = logging.getLogger(__name__)


class JprnMapper(base.Mapper):

    # Public

    table = 'jprn'
    primary_key = 'unique_trial_number'

    def map(self):

        # Map sources
        source_id = map_source()

        for item in helpers.table_read(self.warehouse[self.table]):

            # Map trials
            trial_id = self.map_item_trial(item)

            # Map records
            self.map_item_record(item, trial_id, source_id)

            # Map other entities
            self.map_item_problems(item, trial_id)
            self.map_item_interventions(item, trial_id)
            self.map_item_locations(item, trial_id)
            self.map_item_organisations(item, trial_id)
            self.map_item_persons(item, trial_id)

            # Log and sleep
            logger.debug('Mapped: %s' % item[self.primary_key])
            time.sleep(0.1)

    def map_source(self):

        source_id = self.index('source',
            name='jprn',
            type='register',
        )

        self.write('sources', ['id'],
            id=source_id,
            name='jprn',
            type='register',
            data={},
        )

        return source_id

    def map_item_trial(self, item):

        trial_id = self.index('trial',
            nct_id=None,
            euctr_id=None,
            isrctn_id=None,
            scientific_title=item['official_scientific_title_of_the_study'],
        )

        self.write('trials', ['id'],

            # General
            id=trial_id,
            primary_registerc='jprn',
            primary_idc=item['unique_trial_number'],
            secondary_idsc={},  # TODO: use item['secondary_study_id_*'] and item['org_issuing_secondary_study_id_*']
            registration_datec=item['date_of_registration'],
            public_titlec=item['title_of_the_study'],
            brief_summaryc='N/A',  # TODO: review
            scientific_titlec=item['official_scientific_title_of_the_study'],
            descriptionc=None,  # TODO: review

            # Recruitment
            recruitment_statusc=item['recruitment_status'],
            eligibility_criteriac={
                'inclusion': item['key_inclusion_criteria'],
                'exclusion': item['key_exclusion_criteria'],
            },
            target_sample_size=item['target_sample_size'],
            first_enrollment_date=item['anticipated_trial_start_date'],  # TODO: review

            # Study design
            study_type=item['study_type'] or 'N/A',  # TODO: review
            study_design=item['basic_design'] or 'N/A',  # TODO: review
            study_phase=item['developmental_phase'] or 'N/A',  # TODO: review

            # Outcomes
            primary_outcomes=item['primary_outcomes'] or [],
            secondary_outcomes=item['key_secondary_outcomes'] or [],

        )

    def map_item_record(self, item, trial_id, source_id):

        self.write('records', ['id'],
            id=item['meta_id'],
            source_id=source_id,
            type='trial',
            data={'unique_trial_number': item['unique_trial_number']},  # TODO: serialization issue
        )

        self.write('trials_records', ['trial_id', 'record_id'],
            trial_id=trial_id,
            record_id=item['meta_id'],
            role='primary',
            context={},
        )

    def map_item_problems(self, item, trial_id):
        # TODO: item['condition'] - free text some time
        pass

    def map_item_interventions(self, item, trial_id):
        # TODO: item['interventions'] - array of free texts
        pass

    def map_item_locations(self, item, trial_id):
        # TODO: fix on scraper item['region'] when possible
        pass

    def map_item_organisations(self, item, trial_id):

        organisations = []
        organisations.append({
            'name': item['name_of_primary_sponsor'],
            'role': 'primary_sponsor',
        })
        organisations.append({
            'name': item['source_of_funding'],
            'role': 'funder',
        })

        for organisation in organisations:

            organisation_id = self.index('organisation',
                name=organisation['name'],
                type=None,
            )

            self.write('organisations', ['id'],
                id=organisation_id,
                name=organisation['name'],
                type=None,
                data={},
            )

            self.write('trials_organisations', ['trial_id', 'organisation_id'],
                trial_id=trial_id,
                organisation_id=organisation_id,
                role=organisation['role'],
                context={},
            )

    def map_item_persons(self, item, trial_id):

        persons = []
        persons.append({
            'name': item['research_name_of_lead_principal_investigator'],
            'role': 'principal_investigator',
            'context': {
                'research_name_of_lead_principal_investigator': item['research_name_of_lead_principal_investigator'],
                'research_organization': item['research_organization'],
                'research_division_name': item['research_division_name'],
                'research_address': item['research_address'],
                'research_tel': item['research_tel'],
                'research_homepage_url': item['research_homepage_url'],
                'research_email': item['research_email'],
            },
        })
        persons.append({
            'name': item['public_name_of_contact_person'],
            'role': 'public_queries',
            'context': {
                'public_name_of_contact_person': item['public_name_of_contact_person'],
                'public_organization': item['public_organization'],
                'public_division_name': item['public_division_name'],
                'public_address': item['public_address'],
                'public_tel': item['public_tel'],
                'public_homepage_url': item['public_homepage_url'],
                'public_email': item['public_email'],
            },
        })

        for person in persons:

            person_id = self.index('person',
                name=person['name'],
            )

            self.write('persons', ['id'],
                id=person_id,
                name=person['name'],
                type=None,
                data={},
            )

            self.write('trials_persons', ['trial_id', 'person_id'],
                trial_id=trial_id,
                person_id=person_id,
                role=person['role'],
                context=person['context']
            )


if __name__ == '__main__':

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    mapper = JprnMapper(warehouse, database)
    mapper.map()
