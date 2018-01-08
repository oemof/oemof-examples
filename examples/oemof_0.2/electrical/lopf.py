# -*- coding: utf-8 -*-
"""
General description
-------------------
This script shows how to do a linear optimal powerflow (lopf) calculation
based on custom oemof components. The example is based on the PyPSA
simple lopf example.

Note: As oemof currently does not support models with one timesteps, therefore
there are two.

Installation requirements
-------------------------
This example requires the latest version of oemof and matplotlib. Install by:

    pip install oemof
    pip install matplotlib

12.12.2017 - simon.hilpert@uni-flensburg.de
"""
import pandas as pd

# solph imports
from oemof.solph import (EnergySystem, Model, Flow, Source, Sink, custom,
                         Investment)
from oemof.outputlib import processing, views
from oemof.outputlib.graph_tools import graph

datetimeindex = pd.date_range('1/1/2017', periods=2, freq='H')

es = EnergySystem(timeindex=datetimeindex)

b_el0 = custom.ElectricalBus(label="b_0", v_min=-1, v_max=1)

b_el1 = custom.ElectricalBus(label="b_1", v_min=-1, v_max=1)

b_el2 = custom.ElectricalBus(label="b_2", v_min=-1, v_max=1)

es.add(b_el0, b_el1, b_el2)

es.add(custom.ElectricalLine(label="line0",
                             inputs={b_el0: Flow()},
                             outputs={b_el1: Flow(investment=Investment(),
                                                  min=-1, max=1)},
                             reactance=0.0001))

es.add(custom.ElectricalLine(label="line1",
                             inputs={b_el1: Flow()},
                             outputs={b_el2: Flow(nominal_value=60,
                                                  min=-1, max=1)},
                             reactance=0.0001))

es.add(custom.ElectricalLine(label="line2",
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

m = Model(energysystem=es)

# m.write('lopf.lp', io_options={'symbolic_solver_labels': True})

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
