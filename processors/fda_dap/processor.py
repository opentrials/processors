# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import hashlib
import logging
import requests
import StringIO
import PyPDF2
import boto3
import documentcloud
from .. import base
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):
    source_id = _create_source(conn)
    assert source_id is not None

    processor = FDADAPProcessor(conf, conn)
    for record in base.helpers.iter_rows(conn, 'warehouse', 'fda_dap', orderby='id'):
        try:
            processor.process_record(record, source_id)
        except Exception:
            logger.exception('Failed processing record %s' % record['meta_id'])


def _create_source(conn):
    source = {
        'id': 'fda',
        'name': 'U.S. Food and Drug Administration',
        'type': 'other',
    }
    return base.writers.write_source(conn, source)


class FDADAPProcessor(object):
    def __init__(self, conf, conn):
        self._conf = conf
        self._conn = conn

    def process_record(self, record, source_id):
        fda_approval = self._write_fda_approval(record)

        for document in record['documents']:
            data = self._find_document(document, fda_approval) or {}

            data.update({
                'source_id': 'fda',
                'name': document['name'],
                'type': 'other',
                'fda_approval_id': fda_approval['id'],
            })

            if not data.get('file_id'):
                data['file_id'] = self._upsert_file(document, fda_approval)

            # Save to DB
            base.writers.write_document(self._conn, data)

    def _upsert_file(self, document, fda_approval):
        theFile = {}
        fileModified = False

        # Merge PDFs and upload to S3 if we haven't done it already
        urls = document['urls']
        logging.debug('Downloading PDFs from %s' % ', '.join(urls))
        with DownloadAndMergePDFs(urls) as pdf_file:
            sha1 = self._calculate_sha1(pdf_file)

            existingFile = self._conn['database']['files'].find_one(sha1=sha1)
            if existingFile:
                fileModified = (sha1 != existingFile['sha1'])
                theFile = existingFile

            theFile['sha1'] = sha1

            # Upload to S3 if needed
            if not theFile.get('url') or fileModified:
                pdf_file.seek(0)
                theFile['url'] = self._upload_to_s3(pdf_file, sha1)
                logging.debug('Merged PDF uploaded to: %s' % theFile['url'])

        # Delete file in DocumentCloud if it was modified
        if fileModified and theFile.get('documentcloud_id'):
            dc_id = theFile['documentcloud_id']
            logging.debug('Deleting outdated DocumentCloud doc: %s' % dc_id)
            self._delete_documentcloud_file(theFile['documentcloud_id'])
            del theFile['documentcloud_id']

        # Upload to DocumentCloud
        if not theFile.get('documentcloud_id'):
            dc_title = '-'.join([
                fda_approval['id'],
                fda_approval['type'],
                document['name']
            ])
            dc_id = self._upload_to_documentcloud(theFile['url'], dc_title)
            logging.debug('PDF uploaded to DocumentCloud: %s' % dc_id)
            theFile['documentcloud_id'] = dc_id

        return base.writers.write_file(self._conn, theFile)

    def _write_fda_approval(self, fda_approval):
        '''Creates an FDA Approval and the related FDA Application if
        needed.'''

        fda_application_id = self._ensure_fda_application_exists(fda_approval)

        obj = self._find_fda_approval(fda_approval['id'])

        if not obj:
            obj = {
                'id': fda_approval['id'],
                'fda_application_id': fda_application_id,
            }

        obj.update({
            'supplement_number': fda_approval['supplement_number'],
            'type': fda_approval['approval_type'],
            'action_date': fda_approval['action_date'],
            'notes': fda_approval['notes'],
        })

        self._conn['database']['fda_approvals'].upsert(obj, ['id'], ensure=False)

        return obj

    def _ensure_fda_application_exists(self, fda_approval):
        fda_application = {
            'id': fda_approval['fda_application_num'],
            'organisation': fda_approval['company'],
            'drug_name': fda_approval['drug_name'],
            'active_ingredients': fda_approval['active_ingredients'],
        }
        return base.writers.write_fda_application(self._conn, fda_application, 'fda')

    def _find_document(self, document, fda_approval):
        # FIXME: We're using "name" to identify if the document already exist
        # in our DB. However, "name" is mutable, so it isn't a good candidate
        # for a key. I couldn't find a better one, though.
        return self._conn['database']['documents'].find_one(
            name=document['name'],
            fda_approval_id=fda_approval['id']
        )

    def _find_fda_approval(self, fda_approval_id):
        return self._conn['database']['fda_approvals'].find_one(id=fda_approval_id)

    def _upload_to_s3(self, fd, checksum):
        s3 = boto3.resource(
            's3',
            region_name=self._conf['AWS_S3_REGION'],
            aws_access_key_id=self._conf['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self._conf['AWS_SECRET_ACCESS_KEY']
        )
        bucket_name = self._conf['AWS_S3_BUCKET']
        key = 'documents/fda/%s.pdf' % checksum

        s3_custom_domain = self._conf.get('AWS_S3_CUSTOM_DOMAIN')
        if s3_custom_domain:
            url = '/'.join([
                s3_custom_domain,
                key
            ])
        else:
            url = '/'.join([
                s3.meta.client.meta.endpoint_url,
                bucket_name,
                key,
            ])

        s3.Bucket(bucket_name).upload_fileobj(fd, key)

        return url

    def _calculate_sha1(self, fd):
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()
        for chunk in iter(lambda: fd.read(BLOCKSIZE), b''):
            hasher.update(chunk)
        fd.seek(0)
        return hasher.hexdigest()

    def _upload_to_documentcloud(self, url, title):
        project_title = self._conf['DOCUMENTCLOUD_PROJECT']
        client = self._documentcloud_client()
        project, _ = client.projects.get_or_create_by_title(project_title)

        uploaded = client.documents.upload(
            url,
            title=title,
            project=project.id
        )

        return uploaded.id

    def _delete_documentcloud_file(self, documentcloud_id):
        client = self._documentcloud_client()
        return client.documents.delete(documentcloud_id)

    def _documentcloud_client(self):
        username = self._conf['DOCUMENTCLOUD_USERNAME']
        password = self._conf['DOCUMENTCLOUD_PASSWORD']

        return documentcloud.DocumentCloud(username, password)


class DownloadAndMergePDFs(object):
    def __init__(self, urls):
        self._urls = urls
        self._merger = PyPDF2.PdfFileMerger(strict=False)

    def __enter__(self):
        pdfs = [requests.get(url) for url in self._urls]

        for pdf in pdfs:
            self._merger.append(StringIO.StringIO(pdf.content))

        output = StringIO.StringIO()
        self._merger.write(output)
        output.seek(0)

        return output

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._merger.close()
