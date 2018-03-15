# -*- coding: utf-8 -*-
"""
This script has been used to create the meta data file `datapackage.json`
based on existing tabular data structures. You can copy and adapt this code
to create a basic meta data file for
your datapackage. Run this package in data package root directory:

    `python scripts/get_metadata_from_csv.py`

"""
import os
import json
from datapackage import infer, Package, Resource

elements_path = 'data/elements'

# only use data directory
descriptor = infer('data/**/*.csv')

# create Package based on infer above
p = Package(descriptor)


# save the datapackage
p.save('datapackage.json')
