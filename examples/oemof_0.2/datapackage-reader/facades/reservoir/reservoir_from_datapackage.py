# -*- coding: utf-8 -*-
"""
"""
import os.path as path

from oemof.solph import Bus, EnergySystem
from oemof.solph.facades import Reservoir


es = EnergySystem.from_datapackage(
    path.join('/home/simnh/projects/oemof_examples/examples/oemof_0.2/datapackage-reader/facades/reservoir/'
              'datapackage',
              'datapackage.json'),
    typemap={
        'reservoir': Reservoir,
        'bus': Bus})

for n in es.nodes:
    print(n.label)
