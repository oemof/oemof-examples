# -*- coding: utf-8 -*-
"""
"""
import os
import os.path

from oemof.solph import Bus, EnergySystem
from oemof.solph.facades import Generator


es = EnergySystem.from_datapackage(
    path.join(os.path.dirname(os.path.realpath(__file__)),
              'datapackage',
              'datapackage.json'),
    typemap={
        'bus': Bus})

print(es.groups['gen0'].__dict__)
