# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid


# TODO: refactor
def upsert(table, keys, data, auto_id=True):
    check = {key: data[key] for key in keys}
    match = table.find_one(**check)
    if match is None:
        if auto_id:
            ident = uuid.uuid4().hex
            data.update({'id': ident})
        table.insert(data, ensure=False)
    else:
        table.update(data, list(check.keys()), ensure=False)
    if auto_id:
        ident = locals().get('ident', None)
        if ident is None:
            ident = match['id']
        return ident
