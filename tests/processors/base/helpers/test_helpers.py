# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

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
