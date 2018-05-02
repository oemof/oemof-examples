# -*- coding: utf-8 -*-
"""
Example depends on renpass v0.2: https://github.com/znes/renpass_gis

"""
import pandas as pd
from oemof.solph import Bus, EnergySystem, Model

try:
    from renpass.facades import Demand, Generator
except ImportError:
    raise ImportError("Could not import facades from renpass. Did you install it?")

es = EnergySystem(timeindex=pd.date_range(start='2016', periods=3, freq='H'))

bus = Bus(label='electricity-bus')
bus.commodity = 'electricity'

generator = Generator(label='electricity-generator', capacity=None,
                      investment_cost=800, marginal_cost=75, bus=bus)

demand = Demand(label='electricity-demand1', amount=2000,
                profile=[0.01, 0.02, 0.03], bus=bus)

demand = Demand(label='electricity-demand2', amount=1000,
                profile=[0.5, 0.6, 0.8], bus=bus)

es.add(bus, generator, demand)

m = Model(es)
