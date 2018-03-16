# -*- coding: utf-8 -*-
"""
"""
import pandas as pd
from oemof.solph import Bus, EnergySystem, Model
from oemof.solph.facades import Demand, Generator

es = EnergySystem(timeindex=pd.date_range(start='2016', periods=3, freq='H'))

bus = Bus(label='electricity-bus')
bus.commodity = 'electricity'

generator = Generator(label='electricity-generator', capacity=None,
                      investment_cost=800, marginal_cost=75, bus=bus)

demand = Demand(label='electricity-demand', amount=2000,
                profile=[0.01, 0.02, 0.03], bus=bus)

es.add(bus, generator, demand)

m = Model(es)
