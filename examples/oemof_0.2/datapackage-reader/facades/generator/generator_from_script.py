# -*- coding: utf-8 -*-
"""
"""
import pandas as pd
from oemof.solph import Bus, EnergySystem, Model
from oemof.solph.facades import Generator

es = EnergySystem(timeindex=pd.date_range(start='2016', periods=3, freq='H'))

bus = Bus(label='electricity-bus')

generator = Generator(label='electricity-generator1', capacity=1000,
                      marginal_cost=75, bus=bus)

generator = Generator(label='electricity-generator2', capacity=10,
                      marginal_cost=0, bus=bus, profile=[0.1, 0, 0.2])

es.add(bus, generator1, generator2)

m = Model(es)
