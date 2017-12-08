# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
"""
import pandas as pd

# solph imports
from oemof.solph import (EnergySystem, Model, Bus, Flow, Source, Sink,
                         custom, Investment)
from oemof.outputlib import processing, views
from oemof.outputlib.graph_tools import graph

datetimeindex = pd.date_range('1/1/2012', periods=2, freq='H')

es = EnergySystem(timeindex=datetimeindex)

b_0 = Bus(label='b_0')

b_1 = Bus(label='b_1')

b_2 = Bus(label='b_2')

es.add(b_0, b_1, b_2)

es.add(custom.Link(label="line_0",
                   inputs={
                       b_0: Flow(), b_1: Flow()},
                   outputs={
                       b_1: Flow(investment=Investment()),
                       b_0: Flow(investment=Investment())},
                   conversion_factors={
                       (b_0, b_1): 0.99, (b_1, b_0): 0.98}))

es.add(custom.Link(label="line_1",
                   inputs={
                       b_1: Flow(), b_2: Flow()},
                   outputs={
                       b_2: Flow(investment=Investment()),
                       b_1: Flow(investment=Investment())},
                   conversion_factors={
                       (b_1, b_2): 0.99, (b_2, b_1): 0.98}))

es.add(custom.Link(label="line_2",
                   inputs={
                       b_2: Flow(), b_0: Flow()},
                   outputs={
                       b_0: Flow(investment=Investment()),
                       b_2: Flow(investment=Investment())},
                   conversion_factors={
                       (b_2, b_0): 0.99, (b_0, b_2): 0.98}))

es.add(Source(label="gen_0", outputs={
                                b_0: Flow(nominal_value=100,
                                          variable_costs=50)}))

es.add(Source(label="gen_1", outputs={
                                b_1: Flow(nominal_value=100,
                                          variable_costs=25)}))

es.add(Sink(label="load", inputs={
                                b_2: Flow(nominal_value=100,
                                          actual_value=[1, .9],
                                          fixed=True)}))

m = Model(es=es)

m.write('transshipment.lp', io_options={'symbolic_solver_labels': True})

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
print(views.node(results, 'line_1'))

# look at constraints of Links in the pyomo model LinkBlock
m.LinkBlock.pprint()
