# -*- coding: utf-8 -*-
"""
General description
-------------------
This example shows how to create an oemof energysystem from a datapackage by
using the oemof datapackge reader.

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

from oemof.energy_system import EnergySystem
from oemof.solph.models import BaseModel
from oemof.graph import create_nx_graph as create_graph

# read energy system
es = EnergySystem.from_datapackage('datapackage/datapackage.json')

# create graph for energysystem nodes and flows
graph = create_graph(es)
pos = nx.drawing.nx_agraph.graphviz_layout(graph, prog='neato')
nx.draw(graph, pos=pos, with_labels=True)
plt.show()

m = BaseModel(energysystem=es)

ext = es.groups['EXT-chp']
[(k,v) for (k,v) in ext.outputs.items()]
