# -*- coding: utf-8 -*-
"""
General description
-------------------
Example that illustrates how to model min and max runtimes.

Installation requirements
-------------------------
This example requires the latest version of oemof. Install by:

    pip install oemof

"""

import pandas as pd
import oemof.solph as solph
from oemof.network import Node
from oemof.outputlib import processing, views
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


# read sequence data
file_name = 'data'
data = pd.read_csv(file_name + '.csv', sep=",")

# select periods
periods = len(data)-1

# create an energy system
idx = pd.date_range('1/1/2017', periods=periods, freq='H')
es = solph.EnergySystem(timeindex=idx)
Node.registry = es

# power bus and components
bel = solph.Bus(label='bel')

demand_el = solph.Sink(
    label='demand_el',
    inputs={bel: solph.Flow(
        fixed=True, actual_value=data['demand_el'], nominal_value=10)})

dummy_el = solph.Sink(
    label='dummy_el',
    inputs={bel: solph.Flow(variable_costs=10)})

pp1 = solph.Source(
    label='cheap_plant_min_down_constraints',
    outputs={
        bel: solph.Flow(
            nominal_value=10, min=0.5, max=1.0, variable_costs=10,
            nonconvex=solph.NonConvex(
                minimum_downtime=4, initial_status=0))})

pp2 = solph.Source(
    label='expensive_plant_min_up_constraints',
    outputs={
        bel: solph.Flow(
            nominal_value=10, min=0.5, max=1.0, variable_costs=10,
            nonconvex=solph.NonConvex(
                minimum_uptime=2, initial_status=1))})

# create an optimization problem and solve it
om = solph.Model(es)

# debugging
#om.write('problem.lp', io_options={'symbolic_solver_labels': True})

# solve model
om.solve(solver='cbc', solve_kwargs={'tee': True})

# create result object
results = processing.results(om)

# plot data
if plt is not None:
    # plot electrical bus
    data = views.node(results, 'bel')['sequences']
    data[[(('bel', 'demand_el'), 'flow'), (('bel', 'dummy_el'), 'flow')]] *= -1
    exclude = ['dummy_el', 'status']
    columns = [c for c in data.columns
               if not any(s in c[0] or s in c[1] for s in exclude)]
    data = data[columns]
    ax = data.plot(kind='line', drawstyle='steps-post', grid=True, rot=0)
    ax.set_xlabel('Hour')
    ax.set_ylabel('P (MW)')
    plt.show()
