# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
from importlib import import_module
from . import settings
from .connection import Connection


# Module API

def cli(argv):

    # Establish connection
    conn = Connection(settings.WAREHOUSE_URL, settings.DATABASE_URL)

    # Get and call processor
    process = import_module('processors.%s' % argv[1]).process
    process(conn, *argv[2:])


if __name__ == '__main__':
    cli(sys.argv)
