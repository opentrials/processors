# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import re
import logging
from .. import base
import documentcloud
logger = logging.getLogger(__name__)


def process(conf, conn):
    query = '''
        SELECT DISTINCT ON (files.id)
          documents.name,
          files.id,
          files.source_url,
          files.sha1,
          files.documentcloud_id,
          fda_approvals.supplement_number,
          fda_approvals.action_date,
          fda_approvals.fda_application_id,
          fda_approvals.type
        FROM documents
        INNER JOIN files ON documents.file_id = files.id
        INNER JOIN fda_approvals ON documents.fda_approval_id = fda_approvals.id
        WHERE documents.fda_approval_id IS NOT NULL
          AND documents.file_id IS NOT NULL
        ORDER BY files.id
    '''
    processor = _SendFDADocsToDocumentCloudProcessor(conf, conn['database'])
    for the_file in conn['database'].query(query):
        try:
            the_file['id'] = the_file['id'].hex
            processor.process_file(the_file)
            logger.debug('Processed file %s' % the_file['id'])
        except Exception:
            base.config.SENTRY.captureException(extra={
                'file_id': the_file['id'],
            })


class _SendFDADocsToDocumentCloudProcessor(object):
    def __init__(self, conf, db):
        self._conf = conf
        self._db = db

    def process_file(self, the_file):
        if the_file.get('documentcloud_id'):
            doc = self._dc_client.documents.get(the_file['documentcloud_id'])
        else:
            doc = self._upload_file(the_file)

        if doc.file_hash and (doc.file_hash != the_file['sha1']):
            logger.debug('Deleting outdated DocumentCloud doc: %s' % doc.id)
            doc.delete()
            doc = self._upload_file(the_file)

        application_type = re.findall(r'^[a-zA-Z]+',
                                      the_file['fda_application_id'])[0]

        doc.title = self._generate_title(the_file)
        doc.project = self._project
        doc.access = 'public'
        doc.data = {
            'fda_application': the_file['fda_application_id'],
            'application_type': application_type,
            'supplement_number': str(the_file['supplement_number']),
            'name': the_file['name'],
            'type': the_file['type'],
            'action_date': the_file['action_date'].isoformat(),
        }

        doc.save()

        documentcloud_id = doc.id.split('-')[0]
        if the_file.get('documentcloud_id') != documentcloud_id:
            the_file['documentcloud_id'] = documentcloud_id
            self._db['files'].upsert(the_file, ['id'], ensure=False)

    def _upload_file(self, the_file):
        title = self._generate_title(the_file)
        doc = self._dc_client.documents.upload(
            the_file['source_url'],
            title=title,
            project=self._project.id
        )
        logger.debug('PDF uploaded to DocumentCloud: %s' % the_file['source_url'])

        return doc

    def _generate_title(self, the_file):
        return '-'.join([
            the_file['fda_application_id'],
            str(the_file['supplement_number']),
            the_file['type'],
            the_file['name']
        ])

    @property
    def _project(self):
        title = self._conf['DOCUMENTCLOUD_PROJECT']
        project, _ = self._dc_client.projects.get_or_create_by_title(title)

        return project

    @property
    def _dc_client(self):
        username = self._conf['DOCUMENTCLOUD_USERNAME']
        password = self._conf['DOCUMENTCLOUD_PASSWORD']

        return documentcloud.DocumentCloud(username, password)
