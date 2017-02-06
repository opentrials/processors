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
            base.config.SENTRY.captureException(extra={
                'meta_id': record['meta_id'],
            })


def _create_source(conn):
    source = {
        'id': 'fda',
        'name': 'U.S. Food and Drug Administration',
        'type': 'other',
        'source_url': 'http://www.fda.gov',
    }
    return base.writers.write_source(conn, source)


class FDADAPProcessor(object):
    def __init__(self, conf, conn):
        self._conf = conf
        self._conn = conn

    def process_record(self, record, source_id):
        fda_approval = self._write_fda_approval(record)
        document_category_id = self._upsert_document_category()

        for document in record['documents']:
            file_id = self._upsert_file(document, fda_approval)
            data = self._find_document(document, fda_approval, file_id) or {}

            data.update({
                'source_id': 'fda',
                'name': document['name'],
                'document_category_id': document_category_id,
                'file_id': file_id,
                'fda_approval_id': fda_approval['id'],
            })

            # Save to DB
            base.writers.write_document(self._conn, data)

    def _upsert_file(self, document, fda_approval):
        file_data = {}
        file_modified = False

        # Merge PDFs and upload to S3 if we haven't done it already
        urls = document['urls']
        logging.debug('Downloading PDFs from %s' % ', '.join(urls))
        with DownloadAndMergePDFs(urls) as pdf_file:
            sha1 = self._calculate_sha1(pdf_file)

            existing_file = self._conn['database']['files'].find_one(sha1=sha1)
            if existing_file:
                file_modified = (sha1 != existing_file['sha1'])
                file_data = existing_file

            file_data['sha1'] = sha1

            # Upload to S3 if needed
            if not file_data.get('source_url') or file_modified:
                # TODO: Maybe delete the previous file? Or maybe we want to
                # keep them as historical records.
                pdf_file.seek(0)
                file_data['source_url'] = self._upload_to_s3(pdf_file, sha1)
                logging.debug('Merged PDF uploaded to: %s' % file_data['source_url'])

        return base.writers.write_file(self._conn, file_data)

    def _upsert_document_category(self):
        document_category = {
            'id': 20,
            'name': 'Other',
        }
        return base.writers.write_document_category(self._conn, document_category)

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

    def _find_document(self, document, fda_approval, file_id):
        return self._conn['database']['documents'].find_one(
            name=document['name'],
            fda_approval_id=fda_approval['id'],
            file_id=file_id
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
