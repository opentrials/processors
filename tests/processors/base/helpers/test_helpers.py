# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import uuid
import collections
import pytest
import processors.base.helpers as helpers


class TestValidateIdentifier(object):
    @pytest.mark.parametrize('identifier', [
        'NCT00020500',
        'U2016-0100-0042',
        'ISRCTN02018090',
        'EUCTR2013-030180-02',
        'EUCTR2010-070109-20/IT',
        'TAKEDA-AD-4833_409 (PHARMO)',
    ])
    def test_valid_identifiers(self, identifier):
        assert helpers.validate_identifier(identifier)

    @pytest.mark.parametrize('identifier', [
        'NCT00000000',
        'U0000-0000-0000',
        'ISRCTN00000000',
        'EUCTR0000-000000-00',
        'EUCTR0000-000000-00/IT',
    ])
    def test_identifiers_with_only_zeros_are_invalid(self, identifier):
        assert not helpers.validate_identifier(identifier)

    def test_empty_identifiers_are_invalid(self):
        assert not helpers.validate_identifier('')


class TestFindListOfIdentifiers(object):
    @pytest.mark.parametrize('text,identifiers', [
        ('NCT00000000', []),
        ('NCT00020500', [{'nct': 'NCT00020500'}]),
        ('NCT00020500 ISRCTN00000000', [{'nct': 'NCT00020500'}]),
        ('NCT00020500 ISRCTN02018090', [{'nct': 'NCT00020500'}, {'isrctn': 'ISRCTN02018090'}]),
        ('Lorem ipsum NCT00020500 dolor sit amet', [{'nct': 'NCT00020500'}]),
    ])
    def test_returns_only_valid_identifiers(self, text, identifiers):
        assert sorted(helpers.find_list_of_identifiers(text)) == sorted(identifiers)

    @pytest.mark.parametrize('text,identifiers', [
        ('NCT 12345678', [{'nct': 'NCT12345678'}]),
        ('ISRCTN    12345678', [{'isrctn': 'ISRCTN12345678'}]),
        ('TAKEDA01-02-TL-375-033', [{'takeda': 'TAKEDA01-02-TL-375-033'}]),
    ])
    def test_allows_whitespace_in_identifiers(self, text, identifiers):
        assert sorted(helpers.find_list_of_identifiers(text)) == sorted(identifiers)


class TestGetCleanedIdentifiers(object):
    @pytest.mark.parametrize('identifiers', [
        {'actrn': 'ACTRN12615001075572p'},
        {'chictr': 'ChiCTR123'},
        {'drks': 'DRKS123'},
        {'euctr': 'EUCTR1234-123456-12'},
        {'gsk': 'GSK123'},
        {'irct': 'IRCT123'},
        {'isrctn': 'ISRCTN71203361'},
        {'jprn': 'JPRN-UMIN123456789'},
        {'jprn': 'UMIN123456789'},
        {'kct': 'KCT123'},
        {'nct': 'NCT12345678'},
        {'ntr': 'NTR123'},
        {'pactr': 'PACTR123'},
        {'per': 'PER123'},
        {'rbr': 'RBR123'},
        {'rpcec': 'RPCEC123'},
        {'takeda': 'TAKEDA123'},
        {'tctr': 'TCTR123'},
        {'who': 'U1111-1115-2414'},
    ])
    def test_good_identifiers(self, identifiers):
        assert helpers.clean_identifiers(identifiers) == identifiers

    @pytest.mark.parametrize('identifiers', [
        {'bad_source': 'U123'},
        {'nct': 'ACTRN123'},
        {'actrn': '123ACTRN'},
        {'takeda': False},
        {'jprn': None},
        {'isrctn': 'ISRCTN12345678, ISRCTN12345678'},
        {'nct': ''},
        {'nct': 'NCT00000000'},
        {'isrctn': 'ISRCTN00000000'},
    ])
    def test_bad_identifiers(self, identifiers):
        assert helpers.clean_identifiers(identifiers) == {}

    def test_ignores_case(self):
        identifiers = {'nct': 'nCt12345678'}
        assert helpers.clean_identifiers(identifiers) == identifiers


class TestValidateRemoteURL(object):
    @pytest.mark.parametrize('url', [
        'https://onlinelibrary.wiley.com/doi/10.1002/14651858.CD009005/full',
        'http://www.ncbi.nlm.nih.gov/pubmed/18502614',
        'ftp://ftp.funet.fi/pub/standards/RFC/rfc959.txt',
    ])
    def test_valid_url(self, url):
        assert helpers.validate_remote_url(url)

    @pytest.mark.parametrize('url', [
        'ncbi.nlm.nih.gov/pubmed/18502614',
        'somewhere',
        'somewhere.com',
        None,
        True,
    ])
    def test_invalid_url(self, url):
        assert not helpers.validate_remote_url(url)

class TestSafePrepend(object):
    @pytest.mark.parametrize('prepend_string, string, expected', [
        ('EUCTR', '123456', 'EUCTR123456'),
        ('EUCTR', 'EUCTR123456', 'EUCTR123456'),
        ('EUCTR', None, None),
    ])
    def test_safe_prepend(self, prepend_string, string, expected):
        assert helpers.safe_prepend(prepend_string, string) == expected

class TestLocationNormalizer(object):
    @pytest.mark.parametrize("test_input,expected", [
        # Locations normalized by ISO-3166 name standards
        ("Brazil", "Brazil"),
        ("United States of America","United States"),

        # Locations normalized by ISO-3166 acronym standards
        ("US","United States"),
        ("UK","United Kingdom"),

        # Locations normalized by Levenshtein distance (name)
        ("Chnia","China"),
        ("The Netherlands","Netherlands"),
        ("thauland","Thailand"),

        # Locations not normalized (corner cases)
        ("Asia(except Japan)","Asia(except Japan)"),
        ("Outside","Outside"),
        (None, None)])


    def test_location_normalizer(self, test_input, expected):
        assert helpers.get_canonical_location_name(test_input) == expected


class TestFindTrial(object):
    def test_returns_None_None_if_trial_isnt_found(self, conn):
        mock_trial = {
            'identifiers': {},
            'public_title': 'the title',
            'source_id': 'nct',
        }
        assert helpers.find_trial(conn, mock_trial) == (None, None)

    @mock.patch('processors.base.helpers.find_trial_by_identifiers')
    @mock.patch('processors.base.helpers.find_trial_by_public_title', side_effect=Exception())
    def test_it_finds_via_identifiers_first(self, _, find_trial_by_identifiers_mock):
        record_id = '00000000-0000-0000-0000-000000000000'
        conn = {}
        trial_dict = {
            'identifiers': {'nct': 'NCT000001'},
            'public_title': 'the title',
            'source_id': 'nct',
        }
        find_trial_by_identifiers_mock.return_value = trial_dict

        trial_found, method = helpers.find_trial(conn, trial_dict)

        assert trial_found == trial_dict
        assert method == 'identifiers'

    @mock.patch('processors.base.helpers.find_trial_by_public_title')
    @mock.patch('processors.base.helpers.find_trial_by_identifiers', return_value=None)
    def test_it_finds_via_public_title_if_not_found_by_identifiers(self, _, find_trial_by_public_title_mock):
        record_id = '00000000-0000-0000-0000-000000000000'
        conn = {}
        trial_dict = {
            'identifiers': {},
            'public_title': 'the title',
            'source_id': 'nct',
        }
        find_trial_by_public_title_mock.return_value = trial_dict

        trial_found, method = helpers.find_trial(conn, trial_dict)

        assert trial_found == trial_dict
        assert method == 'public_title'

    @mock.patch('processors.base.helpers.find_trial_by_public_title', return_value=None)
    @mock.patch('processors.base.helpers.find_trial_by_identifiers', return_value=None)
    def test_it_calls_itself_recursively_with_ignore_record_id_as_None_if_couldnt_find_trial(self, find_trial_by_identifiers_mock, find_trial_by_public_title_mock):
        record_id = '00000000-0000-0000-0000-000000000000'
        conn = {}
        trial_dict = {
            'identifiers': {},
            'public_title': 'the title',
            'source_id': 'nct',
        }

        # Save reference to be able to test recursive function
        original_find_trial = helpers.find_trial
        with mock.patch('processors.base.helpers.find_trial', return_value=(None, None)) as find_trial_mock:
            trial_found, deduplication_method = original_find_trial(conn, trial_dict, record_id)
            find_trial_mock.assert_called_with(conn, trial_dict, ignore_record_id=None)

        assert trial_found is None
        assert deduplication_method is None


class TestFindTrialByPublicTitle(object):
    def test_returns_trial(self, conn, trial, record, nct_source):
        trial_attrs = conn['database']['trials'].find_one(id=trial)
        conn['database']['records'].update(
            {
                'id': record,
                'source_id': nct_source,
                'trial_id': trial_attrs['id'],
                'public_title': trial_attrs['public_title'],
            },
            ['id']
        )

        found_trial = helpers.find_trial_by_public_title(conn, trial_attrs['public_title'], 'euctr')

        assert found_trial is not None
        assert found_trial['id'] == trial_attrs['id']

    def test_it_ignores_trials_from_received_source(self, conn, trial, record, nct_source):
        trial_attrs = conn['database']['trials'].find_one(id=trial)
        conn['database']['records'].update(
            {
                'id': record,
                'source_id': nct_source,
                'trial_id': trial_attrs['id'],
                'public_title': trial_attrs['public_title'],
            },
            ['id']
        )

        found_trial = helpers.find_trial_by_public_title(conn, trial_attrs['public_title'], nct_source)
        assert found_trial is None

    def test_it_ignores_records_without_trials(self, conn, record, nct_source):
        public_title = 'the title'
        conn['database']['records'].update(
            {
                'id': record,
                'source_id': nct_source,
                'trial_id': None,
                'public_title': public_title,
            },
            ['id']
        )

        found_trial = helpers.find_trial_by_public_title(conn, public_title, 'euctr')
        assert found_trial is None

    def test_it_ignores_the_received_record_id(self, conn, trial, record, nct_source):
        trial_attrs = conn['database']['trials'].find_one(id=trial)
        conn['database']['records'].update(
            {
                'id': record,
                'source_id': nct_source,
                'trial_id': trial_attrs['id'],
                'public_title': trial_attrs['public_title'],
            },
            ['id']
        )

        found_trial = helpers.find_trial_by_public_title(conn, trial_attrs['public_title'], 'euctr', record)
        assert found_trial is None


class TestFindTrialByIdentifiers(object):
    def test_returns_None_if_trial_isnt_found(self, conn):
        identifiers = {}
        assert helpers.find_trial_by_identifiers(conn, identifiers) is None

    def test_returns_None_if_trial_isnt_found(self, conn, record):
        record_dict = conn['database']['records'].find_one(id=record)
        assert record_dict['trial_id'] is None
        assert helpers.find_trial_by_identifiers(conn, record_dict['identifiers']) is None

    def test_returns_None_if_record_id_is_ignored(self, conn, record):
        record_dict = conn['database']['records'].find_one(id=record)
        assert helpers.find_trial_by_identifiers(conn, record_dict['identifiers'], record_dict['id']) is None

    def test_returns_trial_ignoring_the_ignored_record_id(self, conn, record, trial):
        trial1_dict = conn['database']['trials'].find_one(id=trial)
        trial2_dict = trial1_dict.copy()
        trial2_dict.update({
            'id': uuid.uuid1().hex,
        })
        conn['database']['trials'].insert(trial2_dict)
        record1_dict = conn['database']['records'].find_one(id=record)
        record2_dict = record1_dict.copy()
        record2_dict.update({
           'id': uuid.uuid1().hex,
           'trial_id': trial2_dict['id'],
           'source_url': record2_dict['source_url'] + 'foo',
        })
        conn['database']['records'].insert(record2_dict)
        conn['database']['records'].update(
            {'id': record, 'trial_id': trial},
            ['id']
        )

        trial_found = helpers.find_trial_by_identifiers(conn, record2_dict['identifiers'], record1_dict['id'])

        assert trial_found is not None
        assert uuid.UUID(trial_found['id']) == uuid.UUID(trial2_dict['id'])

    def test_returns_trial(self, conn, record, trial):
        conn['database']['records'].update(
            {'id': record, 'trial_id': trial},
            ['id']
        )
        record_dict = conn['database']['records'].find_one(id=record)

        trial_found = helpers.find_trial_by_identifiers(conn, record_dict['identifiers'])

        assert trial_found is not None
        assert uuid.UUID(trial_found['id']) == uuid.UUID(trial)

    def test_it_loops_over_all_identifiers_to_find_trial(self, conn, record, trial):
        conn['database']['records'].update(
            {'id': record, 'trial_id': trial},
            ['id']
        )
        record_dict = conn['database']['records'].find_one(id=record)
        identifiers = record_dict['identifiers']
        ordered_identifiers = collections.OrderedDict(
            [['source_id', 'identifier']] + identifiers.items()
        )

        trial_found = helpers.find_trial_by_identifiers(conn, ordered_identifiers)
        assert trial_found is not None
