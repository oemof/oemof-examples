# -*- coding: utf-8 -*-
"""
"""
import os
import os.path

from oemof.solph import Bus, EnergySystem
from oemof.solph.facades import Demand, Generator

es = EnergySystem.from_datapackage(
    os.path.join(os.path.dirname(os.path.realpath(__file__)),
                 'datapackage',
                 'datapackage.json'),
    attributemap={
        Demand: {"demand-profiles": "profile"}},
    typemap={
        'demand': Demand,
        'generator': Generator,
        'bus': Bus})
