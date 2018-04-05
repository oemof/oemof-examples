# -*- coding: utf-8 -*-
"""
"""
import os
import os.path

from datapackage import Package

from oemof.solph import Bus, EnergySystem, Model
from oemof.solph.facades import Demand, Generator


path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
             'datapackage',
             'datapackage.json')

p = Package(path)

if p.valid:
    for r in p.resources:
        #[e for e in r.iter(relations=True)]
        r.check_relations()

es = EnergySystem.from_datapackage(
    path,
    attributemap={
        Demand: {"demand-profiles": "profile"}},
    typemap={
        'demand': Demand,
        'generator': Generator,
        'bus': Bus})

print(es.nodes[1].profile)

print(es.flows())

m = Model(es)
m.solve()
