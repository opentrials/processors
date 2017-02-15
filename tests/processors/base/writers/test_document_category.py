# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import processors.base.writers as writers


class TestDocumentWriter(object):
    def test_creates_document_category_if_id_not_found(self, conn):
        document_category = {
            'id': 1,
            'name': 'Subcategory',
            'group': 'Category',
        }

        doc_category_id = writers.write_document_category(conn, document_category)

        assert conn['database']['document_categories'].find_one(id=doc_category_id) is not None


    def test_creates_document_category_if_name_and_group_not_found(self, conn):
        document_category = {
            'name': 'Subcategory',
            'group': 'Category',
        }

        doc_category_id = writers.write_document_category(conn, document_category)

        assert conn['database']['document_categories'].find_one(id=doc_category_id) is not None


    def test_updates_document_with_existing_id(self, conn):
        document_category = {
            'id': 1,
            'name': 'Subcategory',
            'group': 'Category',
        }
        conn['database']['document_categories'].insert(document_category)
        update_attrs = {
            'name': 'Updated',
        }
        document_category.update(update_attrs)

        doc_category_id = writers.write_document_category(conn, document_category)
        updated_document = conn['database']['document_categories'].find_one(id=doc_category_id)

        assert updated_document['name'] == update_attrs['name']
