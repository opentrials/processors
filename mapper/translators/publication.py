# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import datetime

from .. import helpers
from .. import extractors
from ..finder import Finder
from ..pipeline import Pipeline
from . import base
logger = logging.getLogger(__name__)


# Module API

class PublicationTranslator(base.Translator):
    """Publication based translator from warehouse to database.
    """

    # Public

    def __init__(self, warehouse, database, extractor):

        self.__extractor = getattr(extractors, extractor.capitalize())()
        self.__pipeline = Pipeline(source=warehouse, target=database)
        self.__finder = Finder(database)

        if self.__extractor.store != 'warehouse':
            message = 'Translator and extractor are not compatible: %s-%s'
            message = message % (self, self.__extractor)
            raise ValueError(message)

    def translate(self):

        # Translate source
        source_id = self.translate_source(None)

        success = 0
        errors = 0
        for item in self.__pipeline.read(self.__extractor.table):

            self.__pipeline.begin()

            try:
                publication_id = self.translate_publication(item, source_id)

            except Exception as exception:
                errors += 1
                self.__pipeline.rollback()
                logger.warning('Translation error: %s [%s]' % (repr(exception), errors))

            else:
                success += 1
                self.__pipeline.commit()
                logger.debug('Translated - publication: %s [%s]' % (publication_id, success))

            if not success % 100:
                logger.info('Translated %s publications [%s]' % (success, self.__extractor.table))

    def translate_source(self, item):

        source = self.__extractor.extract('source',
            item=item,
        )

        entry, existent = self.__finder.find('sources',
            name=source['name'],
        )

        self.__pipeline.write_entity('sources', entry,
            type=source.get('type', None),
            data=source.get('data', {}),
        )

        if not existent:
            logger.debug('Created - source: %s' % (source['name']))

        return entry['id']

    def translate_publication(self, item, source_id):

        publication = self.__extractor.extract('publication',
            item=item,
        )

        entity, existent = self.__finder.find('publications',
            source_url=publication['source_url'],
        )

        timestamp = datetime.datetime.utcnow()
        self.__pipeline.write_entity('publications', {},
            id=entity['id'],
            source_id=source_id,
            created_at=entity['created_at'] if existent else timestamp,
            updated_at=timestamp,
            source_url=publication['source_url'],
            title=publication['title'],
            abstract=publication['abstract'],
            authors=publication['authors'],
            journal=publication['journal'],
            date=publication['date'],
        )

        for identifier in publication['identifiers']:
            trial_entity, trial_existent = self.__finder.find('trials',
                facts=[helpers.slugify(identifier)],
            )
            if trial_existent:
                self.__pipeline.write_relation('trials_publications',
                    ['trial_id', 'publication_id'],
                    trial_id=trial_entity['id'],
                    publication_id=entity['id'],
                )

        if existent:
            logger.debug('Matched - publication: %s' % publication['title'])
        else:
            logger.debug('Created - publication: %s' % publication['title'])

        return entity['id']
