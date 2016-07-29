# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import os
import re
import uuid
import boto3
import shutil
import logging
import zipfile
import hashlib
import tempfile
import requests
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):

    # Prepare s3 resource
    resource = boto3.resource('s3',
        region_name=conf['AWS_S3_REGION'],
        aws_access_key_id=conf['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=conf['AWS_SECRET_ACCESS_KEY'])

    # Iterate contributions mapping
    for contrib_id, mappings in conf['CONTRIB'].items():

        # Log started for contrib
        logger.info('Started extration from contrib "%s"', contrib_id)

        # Prepare temp directory
        dirpath = tempfile.mkdtemp()

        # Get contribution and download documents
        contrib = conn['explorerdb']['data_contributions'].find_one(id=contrib_id)
        _download_documents(contrib['data_url'], dirpath)

        # Process downloaded documents
        for filename in os.listdir(dirpath):

            # Extract primary_id
            (type, primary_id) = _extract_metadata(filename, mappings)
            if not primary_id:
                logger.warning('Document "%s" is not in contrib mappings', filename)
                continue

            # Retrieve trial
            trial = conn['database']['trials'].find_one(primary_id=primary_id)
            if not trial:
                logger.warning('Document "%s" has no matched trial', filename)
                continue

            # Build document url
            filepath = os.path.join(dirpath, filename)
            checksum = _caclulate_checksum(filepath)
            extension = os.path.splitext(filename)[1]
            bucket = conf['AWS_S3_BUCKET']
            key = 'documents/%s%s' % (checksum, extension)
            url = _generate_url(resource, bucket, key)

            # Get documents table
            table = conn['database']['documents']

            # Skip if document is already saved
            if table.find_one(trial_id=trial['id'], url=url):
                logger.info('Document "%s" is already saved', filename)
                continue

            # Upload document to S3
            resource.Bucket(bucket).upload_file(filepath, key)

            # Write document to database
            table.insert({
                'id': uuid.uuid4().hex,
                'name': '%s [%s]' % (primary_id, type),
                'trial_id': trial['id'],
                'type': type,
                'url': url,
            }, ensure=False)

            # Log success
            logger.info('Document "%s" saved with url "%s"', filename, url)

        # Remove temp directory
        shutil.rmtree(dirpath)

        # Log finished for contrib
        logger.info('Finished extration from contrib "%s"', contrib_id)


# Internal

def _download_documents(url, dirpath):
    """Download documents to dirpath and extract if needed.
    """
    content = requests.get(url).content
    # Archive of documents
    if url.lower().endswith('.zip'):
        arch = zipfile.ZipFile(io.BytesIO(content))
        for name in arch.namelist():
            arch.extract(name, dirpath)
    # Just single document
    else:
        filename = os.path.basepath(url)
        filepath = os.path.join(dirpath, filename)
        with open(filepath, 'wb') as file:
            file.write(content)


def _extract_metadata(filename, mappings):
    """Extract (type, primary_id) from filename using contrib mappings.
    """
    for type, submappings in mappings.items():
        # Mapping per type (like "csr")
        for mapping in submappings:
            # Regex mapping
            if not isinstance(mapping, tuple):
                match = re.match(mapping, filename)
                if match:
                    return (type, match.group('primary_id').upper())
            # Hard-coded mapping
            else:
                if filename == mapping[0]:
                    return (type, mapping[1].upper())
    return (None, None)


def _caclulate_checksum(filepath):
    """Calculate SHA1 checksum for filepath.
    """
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filepath, 'rb') as file:
        buffer = file.read(BLOCKSIZE)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = file.read(BLOCKSIZE)
    return hasher.hexdigest()


def _generate_url(resource, bucket, key):
    url = '{}/{}/{}'.format(resource.meta.client.meta.endpoint_url, bucket, key)
    return url
