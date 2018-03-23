# -*- coding: utf-8 -*-
"""
"""
import os

from oemof.solph import Bus, EnergySystem
from oemof.solph.facades import Generator


es = EnergySystem.from_datapackage(
    path.join(os.path.dirname(os.path.realpath(__file__)),
              'datapackage',
              'datapackage.json'),
    typemap={
        'Generator': Generator,
        'bus': Bus})

for n in es.nodes:
    print(n.label)
