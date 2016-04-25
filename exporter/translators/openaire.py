# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from sqlalchemy import create_engine
from datapackage import pull_datapackage
from dotenv import load_dotenv; load_dotenv('.env')

from .. import settings
from . import base
logger = logging.getLogger(__name__)


# Module API

class OpenaireTranslator(base.Translator):

    # Public

    def __init__(self, warehouse, database):
        self.__warehouse = warehouse
        self.__database = database

    def translate(self):

        # Engine
        engine = create_engine(settings.DATABASE_URL)

        # View/table
        query = """
            create table export_openaire as
            select t.id, t.scientific_title,
            array_agg(distinct r.primary_id) filter(where r.primary_id is not null) as identifiers,
            array_agg(distinct p.name) filter(where p.name is not null) as problems,
            array_agg(distinct i.name) filter(where i.name is not null) as interventions
            from trials as t
            left outer join trialrecords as r on t.id = r.trial_id
            left outer join trials_problems as tp on t.id = tp.trial_id left outer join problems as p on p.id = tp.problem_id
            left outer join trials_interventions as ti on t.id = ti.trial_id left outer join interventions as i on i.id = ti.intervention_id
            group by t.id;
        """
        engine.execute(query)

        # Import
        pull_datapackage(
            descriptor='target/openaire/datapackage.json', name='export',
            backend='sql', engine=engine, prefix='export_')

        # Log
        logger.info('Exported datapackage for OpenAIRE.')
