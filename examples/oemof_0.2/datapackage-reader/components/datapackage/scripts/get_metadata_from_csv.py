# -*- coding: utf-8 -*-
"""
This script has been used to create the meta data file `datapackage.json`
based on existing tabular data structures (elements, sequences, geometries,
etc.). You can copy and adapt this code to create a basic meta data file for
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

# remove all elements as single resources
for e in os.listdir(elements_path):
    p.remove_resource(e.split('.')[0])

# reoder path to set header.csv on top
paths = [os.path.join(elements_path, e)
         for e in os.listdir(elements_path)]
paths.remove('data/elements/header.csv')
paths.insert(0, 'data/elements/header.csv')

# add ONE resource with paths to splitted elements (and the correct dialect!)
r = Resource({
    "mediatype": "text/csv",
    "missingValues": [
        ""
        ],
    "name": "elements",
    "format": "csv",
    "encoding": "utf-8",
    "path": paths,
    "profile": "tabular-data-resource",
      "fields": [{"type": "string",
                  "name": "name",
                  "format": "default"},
                 {"type": "string",
                  "name": "type",
                  "format": "default"},
                 {"type": "object",
                  "name": "node_parameters",
                  "format": "default"},
                 {"type": "string",
                  "name": "predecessors",
                  "format": "default"},
                 {"type": "string",
                  "name": "successors",
                  "format": "default"},
                 {"type": "object",
                  "name": "edge_parameters",
                  "format": "default"}],
    "dialect": {
        "caseSensitiveHeader": False,
        "skipInitialSpace": True,
        "header": True,
        "delimiter": ";",
        "doubleQuote": True,
        "quoteChar": "'"
        }})

# add the elements resource
p.add_resource(r.descriptor)

# save the datapackage
p.save('datapackage.json')
