# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import base
logger = logging.getLogger(__name__)


class EuctrExtractor(base.Extractor):

    # Public

    table = 'euctr'
    primary_key = 'eudract_number_with_country'

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
            name='euctr',
            type='register',
        )

        self.write('sources', ['id'],
            id=source_id,
            name='euctr',
            type='register',
            data={},
        )

        return source_id

    def map_item_trial(self, item):

        trial_id = self.index('trial',
            nct_id=None,
            euctr_id=item['eudract_number'],
            isrctn_id=None,
            scientific_title=item['full_title_of_the_trial'],
        )

        self.upsert('trials', ['id'],

            # General
            id = trial_id,
            primary_register='euctr',
            primary_id=item['eudract_number_with_country'],
            secondary_ids={
                'nct': item['us_nct_clinicaltrialsgov_registry_number'],
                'who': item['who_universal_trial_reference_number_utrn'],
                'isrctn': item['isrctn_international_standard_randomised_controlled_trial_numbe'],  # TODO: why number, scraper has number
            },
            registration_date=item['date_on_which_this_record_was_first_entered'],
            public_title=item['title_of_the_trial_for_lay_people_in'] or '',  # TODO: review
            brief_summary=item['trial_main_objective_of_the_trial'] or '',  # TODO: review
            scientific_title=item['full_title_of_the_trial'],
            description=None,  # TODO: review

            # Recruitment
            recruitment_status=item['trial_status'],  # TODO: review
            eligibility_criteria={
                'inclusion': item['trial_principal_inclusion_criteria'],
                'exclusion': item['trial_principal_exclusion_criteria'],
            },
            target_sample_size=item['subject_in_the_whole_clinical_trial'],  # TODO: review
            first_enrollment_date=item['date_on_which_this_record_was_first_entered'],  # TODO: fix on scraper level

            # Study design
            # TODO: discover on scraper level
            study_type='N/A',
            study_design='N/A',
            study_phase='N/A',

            # Outcomes
            # TODO: discover on scraper level
            primary_outcomes=[],
            secondary_outcomes=[],

        )

        return trial_id


    def map_item_record(self, item, trial_id, source_id):

        self.write('records', ['id'],
            id=item['meta_id'],
            source_id=source_id,
            type='trial',
            data={'eudract_number_with_country': item['eudract_number_with_country']},  # TODO: serialization issue
        )

        self.write('trials_records', ['trial_id', 'record_id'],
            trial_id=trial_id,
            record_id=item['meta_id'],
            role='primary',
            context={},
        )

    def map_item_problems(self, item, trial_id):
        # TODO: discover item['trial_medical_conditions_being_investigated']
        pass

    def map_item_interventions(self, item, trial_id):

        for intervention in item['imps'] or []:

            if 'product_name' not in intervention:
                continue

            intervention_id = self.index('intervention',
                name=intervention['product_name'],
                type=None,
            )

            self.write('interventions', ['id'],
                id=intervention_id,
                name=intervention['product_name'],
                type=None,
                data={},
            )

            self.write('trials_interventions', ['trial_id', 'intervention_id'],
                trial_id=trial_id,
                intervention_id=intervention_id,
                role=None,
                context=intervention,
            )

    def map_item_locations(self, item, trial_id):
        # TODO: discover on scraper level
        pass

    def map_item_organisations(self, item, trial_id):
        for sponsor in item['sponsors'] or []:

            if 'name_of_sponsor' not in intervention:
                continue

            organisation_id = self.index('organisation',
                name=sponsor['name_of_sponsor'],
                type=None,
            )

            self.write('organisations', ['id'],
                id=organisation_id,
                name=sponsor['name_of_sponsor'],
                type=None,
                data={},
            )

            self.write('trials_organisations', ['trial_id', 'organisation_id'],
                trial_id=trial_id,
                organisation_id=organisation_id,
                role='sponsor',
                context=sponsor,
            )

    def map_item_persons(self, item, trial_id):
        # TODO: discover on scraper level
        pass


if __name__ == '__main__':

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    mapper = EuctrMapper(warehouse, database)
    mapper.map()
