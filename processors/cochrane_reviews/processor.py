# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import requests
import logging
from functools import reduce
from operator import add
from itertools import groupby
from .. import base
from . import extractors as extractors_module
logger = logging.getLogger(__name__)


def process(conf, conn):
    studies = conn['warehouse']['cochrane_reviews'].distinct('study_id')
    study_ids = [study['study_id'] for study in studies]

    for study_id in study_ids:
        try:
            study_reviews = conn['warehouse']['cochrane_reviews'].find(study_id=study_id)

            for file_name, rev_records in groupby(study_reviews, lambda r: r['file_name']):
                rev_records = list(rev_records)
                latest_rev = sorted(rev_records, key=lambda x: x['meta_updated'])[-1]
                references = reduce(add, [rev['refs'] for rev in rev_records])

                for reference in references:
                    identifiers = extract_ref_identifiers(reference)
                    matching_trials = []
                    for id_name, id_value in identifiers.items():
                        found_trials = match_by_identifier(conn, id_name, id_value)
                        matching_trials.extend(found_trials)

                    if len(matching_trials) == 0:
                        matching_trials.extend(match_by_reference(conn, reference))

                    unique_trials = set(matching_trials)
                    if len(unique_trials) == 1:
                        trial_id = matching_trials[0]
                        extractors = base.helpers.get_variables(
                            extractors_module, lambda x: x.startswith('extract_'))
                        base.processors.process_risk_of_biases(conn, extractors,
                                                               latest_rev, trial_id)
                        break
                    elif len(unique_trials) > 1:
                        logger.debug(('Several matching trials found for reference %s.'
                                     ' Matched trials ids: %s.'), reference, unique_trials)
        except Exception:
            base.config.SENTRY.captureException(extra={
                'study_id': study_id,
            })


def match_by_identifier(conn, id_name, id_value):
    """Choose method of identification based on identifier"""

    if id_name == 'pubmed_id':
        matched_trials = match_by_pubmed_id(conn, id_value)
    elif id_name == 'nct_id':
        matched_trials = match_by_nct_id(conn, id_value)
    else:
        raise NotImplementedError("Don't know how to match by '{0}'".format(id_name))

    return matched_trials


def match_by_reference(conn, reference):
    """Search reference in the database"""

    ref_title = reference['title'].strip()
    matching_trials = conn['database'].query("""SELECT id
                                                FROM trials
                                                WHERE scientific_title=:title
                                                OR public_title=:title;
                                             """, title=ref_title)
    trial_ids = [trial['id'] for trial in matching_trials]
    if len(trial_ids) == 0:
        matching_pubs = conn['database']['publications'].find(title=ref_title)
        for pub in matching_pubs:
            matches = conn['database']['trials_publications'].find(publication_id=pub['id'])
            trial_ids.extend([match['trial_id'] for match in matches])

    return trial_ids


def match_by_pubmed_id(conn, pubmed_id):
    """Find correspondent trial based on pubmed_id"""

    # FIXME: Match directly to `database` publications after `pubmed_id` is added
    matching_pubs = conn['warehouse']['pubmed'].find(pmid=pubmed_id)
    trial_ids = []

    for match in matching_pubs:
        db_pubs = conn['database']['publications'].find(source_url=match['meta_source'])
        for pub in db_pubs:
            matches = conn['database']['trials_publications'].find(publication_id=pub['id'])
            trial_ids.extend([match['trial_id'] for match in matches])

    return trial_ids


def match_by_nct_id(conn, nct_id):
    """Find correspondent trial based on nct_id"""

    query_criteria = {'nct': 'NCT' + nct_id}
    trial = base.helpers.find_trial_by_identifiers(conn, query_criteria)
    if trial:
        return [trial['id']]
    else:
        return []


def extract_ref_identifiers(reference):
    """Extract identifiers from reference"""

    reference_ids = {}
    useful_ids = {'NCT': 'nct_id', 'PUBMED': 'pubmed_id', 'PMID': 'pubmed_id'}
    for _id in useful_ids:
        id_pattern = r'{0}\s*(\d+)'.format(_id)
        for value in reference.values():
            try:
                match = re.search(id_pattern, value).group(1)
                break
            except (AttributeError, TypeError):
                match = None
        if not match:
            for identifier in reference['identifiers']:
                if _id in identifier.values():
                    match = identifier['value'].strip()
                else:
                    try:
                        match = re.search(id_pattern, identifier['value']).group(1)
                        break
                    except AttributeError:
                        match = None
        if match:
            reference_ids[useful_ids[_id]] = match

    if not reference_ids:
        pubmed_id = scrape_pubmed_id(reference)
        if pubmed_id:
            reference_ids[useful_ids['PUBMED']] = pubmed_id

    return reference_ids


def scrape_pubmed_id(reference):
    """Try to find PUBMED ID for reference on PubMed"""

    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    terms = []
    for field in ['title', 'authors', 'year']:
        field_slug = base.helpers.slugify_string(reference[field])
        terms.append(field_slug.replace('_', ' '))

    query_terms = ['({0})'.format(term) for term in terms]
    query_string = ' AND '.join(query_terms)
    search_params = {'term': query_string, 'retmode': 'json'}
    search_result = requests.get(base_url, params=search_params)
    pmids = search_result.json()['esearchresult'].get('idlist', [])
    if len(pmids) == 1:
        return pmids[0]
    else:
        return None
