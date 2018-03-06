# -*- coding: utf-8 -*-
"""
General description
-------------------
This example shows how to create an oemof energysystem that can be optimized
using solph from a datapackage by using the oemof datapackge reader.

Data
----
Data is provided in the datapackage directory:

data/elements/
   demands.csv',
   volatile-generators.csv
   combined-heat-and-power-plants.csv
   header.csv
   dispatchable-generators.csv
   storages.csv
   transshipment.csv

data/geometries/
   components.csv
   hubs.csv

data/sequences/
   demand-profiles.csv
   solar-profiles.csv
   wind-profiles.csv


Installation requirements
-------------------------
This example requires the latest version of oemof. Install
by:

    pip install 'oemof<0.3,>=0.2'

14.02.2018 - simon.hilpert@uni-flensubrg.de
"""
import os

from matplotlib import pyplot as plt
import networkx as nx
import pandas as pd

from oemof.graph import create_nx_graph as create_graph
from oemof.solph import EnergySystem, Source, Bus, Transformer, Flow, Sink
from oemof.solph.components import GenericStorage, ExtractionTurbineCHP
from oemof.solph.custom import Link
from oemof.tools.datapackage import FLOW_TYPE


es = EnergySystem.from_datapackage('datapackage/datapackage.json',
        typemap={'volatile-generator': Source,
            'hub': Bus,
            'bus': Bus,
            'storage': GenericStorage,
            'dispatchable-generator': Source,
            'transshipment': Link,
            'extraction-turbine': ExtractionTurbineCHP,
            'backpressure-turbine': Transformer,
            'demand': Sink,
            FLOW_TYPE: Flow})


grph = create_graph(es)
pos = nx.drawing.nx_agraph.graphviz_layout(grph, prog='neato')

nx.draw(grph, pos=pos, **options)

# add edge labels for all edges
if edge_labels is True and plt:
    labels = nx.get_edge_attributes(grph, 'weight')
    nx.draw_networkx_edge_labels(grph, pos=pos, edge_labels=labels)

# show output
if plot is True:
    plt.show()

ext = es.groups['EXT-chp']

[(k,v) for (k,v) in ext.inputs.items()]
