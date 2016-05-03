# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
from importlib import import_module
from . import config
from .connection import Connection


# Module API

def cli(argv):

    # Prepare conf object
    conf = {}
    for name, value in vars(config).items():
        if name.isupper():
            conf[name] = value

    # Prepare conn object
    conn = Connection(config.WAREHOUSE_URL, config.DATABASE_URL)

    # Get and call processor
    process = import_module('processors.%s' % argv[1]).process
    process(conf, conn, *argv[2:])


if __name__ == '__main__':
    cli(sys.argv)
