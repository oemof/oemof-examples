# -*- coding: utf-8 -*-
"""
"""
import os
import os.path

from datapackage import Package

from oemof.solph import Bus, EnergySystem
from oemof.solph.facades import Demand, Generator


path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
             'datapackage',
             'datapackage.json')

p = Package(path)

if p.valid:
    try:
        for r in p.resources:
            [e for e in r.iter(relations=True)]
    except:
        raise ValueError('Your relations / foreign keys are messed up!')

es = EnergySystem.from_datapackage(
    path,
    attributemap={
        Demand: {"demand-profiles": "profile"}},
    typemap={
        'demand': Demand,
        'generator': Generator,
        'bus': Bus})
