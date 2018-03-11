# -*- coding: utf-8 -*-
"""
"""
import os
import pandas as pd
from oemof.solph import Bus, EnergySystem, Model
from oemof.solph.facades import Demand, Generator, Storage, Connector, CHP
from oemof.outputlib import processing, views

es = EnergySystem(timeindex=pd.date_range(start='2018', periods=4, freq='H'))

b0 = Bus(label='b0')

b1 = Bus(label='b1')

connection  = Connector(label='connector', loss=0.05, capacity=1000,
                        from_bus=b0, to_bus=b1)

supply = Generator(label='generator', capacity=100, opex=10, bus=b0)

wind = Generator(label='wind', capacity=100, dispatchable=False,
                 profile=[0.2] * 4, bus=b1)

storage = Storage(label='storage', capacity=1000, power=100, bus=b0)

demand = Demand(label='demand', amount=200, profile=[0.2] * 4, bus=b0)

# add components to energy system
es.add(b0, b1, supply, wind, demand, storage, connection)

# construct model from energy system
m = Model(es)

# solve the model
m.solve(solve_kwargs={'tee': True})

# get results
results = processing.results(m)

# write results to csv
for n in es.nodes:
    if isinstance(n, Bus):
        sequences =  views.node(results, n)['sequences']
        # convert tuple index to multi index
        idx = [tuple([col[0][0], col[0][1], col[1]])
               for col in sequences.columns]
        sequences.columns = pd.MultiIndex.from_tuples(idx)

        sequences.columns.get_level_values(2).unique()
        flows = sequences.xs('flow', level=2, axis=1)

        directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'results')

        if not os.path.exists(directory):
            os.makedirs(directory)

        path = os.path.join(directory, n.label +'-flows.csv')

        flows.to_csv(path)

m.write(os.path.join(directory, 'facades.lp'), io_options={'symbolic_solver_labels': True})
