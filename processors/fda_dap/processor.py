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
        processor.process_record(record, source_id)


def _create_source(conn):
    source = {
        'id': 'fda',
        'name': 'U.S. Food and Drug Administration',
        'type': 'other',
    }
    return base.writers.write_source(conn, source)


class FDADAPProcessor(object):
    INTERVENTIONS_CACHE = {}

    def __init__(self, conf, conn):
        self._conf = conf
        self._conn = conn

    def process_record(self, record, source_id):
        fda_approval = self._write_fda_approval(record)

        for document in record['documents']:
            document_id = self._generate_document_id(document, fda_approval)
            data = self._find_document(document_id) or {}

            data.update({
                'id': document_id,
                'source_id': 'fda',
                'name': document['name'],
                'type': 'other',
                'fda_approval_id': fda_approval['id'],
            })

            # Merge PDFs and upload to S3
            if data.get('url') is None:
                urls = document['urls']
                logging.debug('Downloading PDFs from %s' % ', '.join(urls))
                with DownloadAndMergePDFs(urls) as pdf_file:
                    data['url'] = self._upload_to_s3(pdf_file)
                    logging.debug('Merged PDF uploaded to: %s' % data['url'])

            # Upload to DocumentCloud
            if data.get('documentcloud_url') is None:
                url = data['url']
                title = '-'.join([
                    fda_approval['id'],
                    fda_approval['type'],
                    document['name']
                ])
                dc_url = self._upload_to_documentcloud(url, data, title)
                logging.debug('PDF uploaded to DocumentCloud: %s' % dc_url)
                data['documentcloud_url'] = dc_url

            # Save to DB
            base.writers.write_document(self._conn, data)

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

    def _generate_document_id(self, document, fda_approval):
        # MD5 is 128 bits, as UUID, so we can use one in place of the other
        name = ''.join([fda_approval['id'],
                        document['name']])
        return hashlib.md5(name.encode('utf-8')).hexdigest()

    def _find_document(self, document_id):
        return self._conn['database']['documents'].find_one(id=document_id)

    def _find_fda_approval(self, fda_approval_id):
        return self._conn['database']['fda_approvals'].find_one(id=fda_approval_id)

    def _upload_to_s3(self, fd):
        s3 = boto3.resource(
            's3',
            region_name=self._conf['AWS_S3_REGION'],
            aws_access_key_id=self._conf['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self._conf['AWS_SECRET_ACCESS_KEY']
        )
        bucket_name = self._conf['AWS_S3_BUCKET']
        checksum = self._calculate_hash(fd)
        key = 'documents/%s.pdf' % checksum

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

    def _calculate_hash(self, fd):
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()
        for chunk in iter(lambda: fd.read(BLOCKSIZE), b''):
            hasher.update(chunk)
        fd.seek(0)
        return hasher.hexdigest()

    def _upload_to_documentcloud(self, url, document, title):
        username = self._conf['DOCUMENTCLOUD_USERNAME']
        password = self._conf['DOCUMENTCLOUD_PASSWORD']
        project_title = self._conf['DOCUMENTCLOUD_PROJECT']

        client = documentcloud.DocumentCloud(username, password)
        project, _ = client.projects.get_or_create_by_title(project_title)

        uploaded = client.documents.upload(
            url,
            title=title,
            project=project.id
        )

        return uploaded.get_published_url()


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
