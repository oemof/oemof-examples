# -*- coding: utf-8 -*-
"""
"""
import os.path as path

from oemof.solph import Bus, EnergySystem
try:
    from renpass.facades import Generator
except ImportError:
    raise ImportError("Could not import facades from renpass. Did you install it?")


es = EnergySystem.from_datapackage(
    path.join(os.path.dirname(os.path.realpath(__file__)),
              'datapackage',
              'datapackage.json'),
    typemap={
        'Generator': Generator,
        'bus': Bus})

for n in es.nodes:
    print(n.label)
