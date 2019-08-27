# -*- coding: utf-8 -*-

"""
"""
import pandas as pd

import oemof.solph as solph
from oemof.solph import constraints
from oemof.outputlib import processing, views
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

energysystem = solph.EnergySystem(
                    timeindex=pd.date_range('1/1/2012', periods=3, freq='H'))

bgas = solph.Bus(label="gas")

bel = solph.Bus(label="electricity", balanced=False)

energysystem.add(bel, bgas)

energysystem.add(solph.Source(label='biomass',
                              outputs={
                                bel: solph.Flow(nominal_value=100,
                                                variable_costs=10,
                                                emission_factor=0.01,
                                                actual_value=[0.1, 0.2, 0.3],
                                                fixed=True)}))

energysystem.add(solph.Source(label='gas-source',
                              outputs={
                                bel: solph.Flow(variable_costs=10,
                                                emission_factor=0.2)}))

energysystem.add(solph.Transformer(
    label="pp_gas",
    inputs={
        bgas: solph.Flow()},
    outputs={
        bel: solph.Flow(nominal_value=200)},
    conversion_factors={
        bel: 0.58}))


model = solph.Model(energysystem)

# add the emission constraint
constraints.emission_limit(model, limit=100)

model.integral_limit_emission_factor.pprint()

model.solve()

print(model.integral_limit_emission_factor())

results = processing.results(model)

if plt is not None:
    data = views.node(results, 'electricity')['sequences']
    ax = data.plot(kind='line', grid=True)
    ax.set_xlabel('Time (h)')
    ax.set_ylabel('P (MW)')
    plt.show()
