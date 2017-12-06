# -*- coding: utf-8 -*-
"""
"""
import pandas as pd

# solph imports
from oemof.solph import (EnergySystem, Model, Bus, Flow, Source, Sink, custom)
from oemof.outputlib import processing, views
from oemof.outputlib.graph_tools import graph


datetimeindex = pd.date_range('1/1/2012', periods=2, freq='H')

es = EnergySystem(timeindex=datetimeindex)


# electricity and heat
b_el0 = custom.ElectricalBus(label="b_el0", v_min=-1, v_max=1)

b_el1 = custom.ElectricalBus(label="b_el1", v_min=-1, v_max=1)

b_el2 = custom.ElectricalBus(label="b_el2", v_min=-1, v_max=1)

es.add(b_el0, b_el1, b_el2)

es.add(custom.ElectricalLine(label="line1",
                             inputs={b_el0: Flow()},
                             outputs={b_el1: Flow(nominal_value=60,
                                                  min=-1, max=1)},
                             reactance=0.0001))
es.add(custom.ElectricalLine(label="line2",
                             inputs={b_el1: Flow()},
                             outputs={b_el2: Flow(nominal_value=60,
                                                  min=-1, max=1)},
                             reactance=0.0001))
es.add(custom.ElectricalLine(label="line3",
                             inputs={b_el2: Flow()},
                             outputs={b_el0: Flow(nominal_value=60,
                                                  min=-1, max=1)},
                             reactance=0.0001))

es.add(Source(label="gen_0", outputs={b_el0: Flow(nominal_value=100,
                                                  variable_costs=50)}))

es.add(Source(label="gen_1", outputs={b_el1: Flow(nominal_value=100,
                                                  variable_costs=25)}))

es.add(Sink(label="load", inputs={b_el2: Flow(nominal_value=100,
                                              actual_value=[1, 1],
                                              fixed=True)}))

m = Model(es=es)


m.solve(solver='cbc',
        solve_kwargs={'tee': True, 'keepfiles': False})


m.results()

graph = graph(es, m, plot=True, layout='neato', node_size=3000,
              node_color={
                  'b_el0': '#cd3333',
                  'b_el1': '#7EC0EE',
                  'b_el2': '#eeac7e'})


results = processing.results(m)
data = views.node(results, 'b_el0')



