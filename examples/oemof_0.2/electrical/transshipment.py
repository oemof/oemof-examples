# -*- coding: utf-8 -*-
"""
General description:
---------------------
This script shows how use the custom component `solph.custom.Link` to build
a simple transshipment model.


Installation requirements:
---------------------------
This example requires the latest version of oemof. Install by:

    pip install oemof

12.12.2017
simon.hilpert@uni-flensburg.de
"""
import pandas as pd

# solph imports
from oemof.solph import (EnergySystem, Model, Bus, Flow, Source, Sink,
                         custom, Investment)
from oemof.outputlib import processing, views
from oemof.outputlib.graph_tools import graph

datetimeindex = pd.date_range('1/1/2017', periods=2, freq='H')

es = EnergySystem(timeindex=datetimeindex)

b_0 = Bus(label='b_0')

b_1 = Bus(label='b_1')

es.add(b_0, b_1)

es.add(custom.Link(label="line_0",
                   inputs={
                       b_0: Flow(), b_1: Flow()},
                   outputs={
                       b_1: Flow(investment=Investment()),
                       b_0: Flow(investment=Investment())},
                   conversion_factors={
                       (b_0, b_1): 0.95, (b_1, b_0): 0.9}))


es.add(Source(label="gen_0", outputs={
                                b_0: Flow(nominal_value=100,
                                          variable_costs=50)}))

es.add(Source(label="gen_1", outputs={
                                b_1: Flow(nominal_value=100,
                                          variable_costs=50)}))

es.add(Sink(label="load_0", inputs={
                                b_0: Flow(nominal_value=150,
                                          actual_value=[0, 1],
                                          fixed=True)}))

es.add(Sink(label="load_1", inputs={
                                b_1: Flow(nominal_value=150,
                                          actual_value=[1, 0],
                                          fixed=True)}))

m = Model(es=es)

# m.write('transshipment.lp', io_options={'symbolic_solver_labels': True})

m.solve(solver='cbc',
        solve_kwargs={'tee': True, 'keepfiles': False})

m.results()

graph = graph(es, m, plot=True, layout='neato', node_size=3000,
              node_color={
                  'b_0': '#cd3333',
                  'b_1': '#7EC0EE',
                  'b_2': '#eeac7e'})

results = processing.results(m)

print(views.node(results, 'gen_0'))
print(views.node(results, 'gen_1'))

views.node(results, 'line_0')['sequences'].plot(kind='bar')

# look at constraints of Links in the pyomo model LinkBlock
m.LinkBlock.pprint()
