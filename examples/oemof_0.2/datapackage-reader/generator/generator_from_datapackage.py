# -*- coding: utf-8 -*-
"""
"""
import os

from oemof.solph import Bus, EnergySystem
try:
    from renpass.facade import Generator
except ImportError:
    raise ImportError(
        """Could not import facades from renpass. Did you install it?

        Please use renpass version > 0.2 from: https://github.com/znes/renpass_gis
        """)


es = EnergySystem.from_datapackage(
    os.path.join(os.path.dirname(os.path.realpath(__file__)),
              'datapackage',
              'datapackage.json'),
    typemap={
        'Generator': Generator,
        'bus': Bus})

for n in es.nodes:
    print(n.label)
