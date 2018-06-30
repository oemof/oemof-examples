# -*- coding: utf-8 -*-
"""
"""
import os.path as path

from oemof.solph import Bus, EnergySystem
try:
    from renpass.facades import Demand, Reservoir
except ImportError:
    raise ImportError(
        """Could not import facades from renpass. Did you install it?

        Please use renpass version > 0.2 from: https://github.com/znes/renpass_gis
        """)


es = EnergySystem.from_datapackage(
    path.join(path.dirname(path.realpath(__file__)),
              'datapackage',
              'datapackage.json'),
    typemap={
        'reservoir': Reservoir,
        'bus': Bus})

for n in es.nodes:
    print(n.label)
