# -*- coding: utf-8 -*-

"""
General description
-------------------
This example illustrates the difference between a convex and a non-convex
investment for a storage. By using a non-convex investment a threshold for
a minimum dimension of a storage and "investment fix-costs" can be
implemented.
Note that the attribute 'minimum' of the Investment-class leads to two
different cases whether a convex or a non-convex investment is applied. In
case of a convex investment the minimum represents the capacity which is
forced to be installed. In case of a non-convex investment the installed
capacity of a flow can become zero as well.


The following energy system is modeled:

                             bus_1
                               |
                               |
   source_vol ---------------->|
    (volatile)                 |
                               |-----> demand (constant value)
                               |
   source_1 ------------------>|
    (expensive)                |
                               |<----> storage
                               |
                               |
                               |-----> excess
                               |

There are two options for fulfilling the demand:

 a) by source_vol, which is supplied by a volatile source. The energy of the
 volatile source is for free and can be stored in a storage which should be
 dimensioned.

 b) by source_1, which is very expensive.

Results
---------------------
Convex-storage investment without minimum capacity:
    Optimal storage capacity:       16.960558
    Energy excess:                  9.616988775
    Objective value:                52157.179018500006

Non-convex-storage investment with minimum capacity of 30:
    Optimal storage capacity:       0.0
    Energy excess:                  76.76253236
    Objective value:                53783.565973000004

Convex-storage investment with minimum capacity of 30:
    Optimal storage capacity:       30.0
    Energy excess:                  0.0
    Objective value:                55107.31272300001

With the given parameter set, the best solution is the storage without a
minimum capacity.

If a minimum capacity of 30 is applied (nonconvex=True, minimum=30), the total
cost increase, and the most cost-efficient solution is without a storage.
The (optimal) solution with a storage capacity of 16.96 is not part of the
solution space anymore and the total costs increase (53783.56).

If a minimum capacity is set and nonconvex is set to False (linear storage
model), the best solution is building the smallest possible storage capacity of
30. The total costs (objective value) in this case is worst (55107).

*Have fun and play around!*

Installation requirements
-------------------------
This example requires the version v0.3.x of oemof. Install by:

    pip install 'oemof>=0.3,<0.4'

"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

import pandas as pd
import oemof.solph as solph
from oemof.network import Node
from oemof.outputlib import processing, views

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

# data series
data_demand = [10 for i in range(167)]
data_source = pd.read_csv('data_source.csv')

# create an energy system
idx = pd.date_range('1/1/2018', periods=96, freq='H')
es = solph.EnergySystem(timeindex=idx)
Node.registry = es

bus_1 = solph.Bus(label='bus_1')

solph.Source(label='source_vol', outputs={bus_1: solph.Flow(
    variable_costs=0, fixed=True, actual_value=data_source['pv'],
    nominal_value=15)})

solph.Source(label='source_1',
             outputs={bus_1: solph.Flow(variable_costs=100)})

solph.Sink(label='demand', inputs={
    bus_1: solph.Flow(fixed=True, actual_value=data_demand, nominal_value=1)})

solph.Sink(label='excess', inputs={bus_1: solph.Flow()})

solph.components.GenericStorage(
    label='storage',
    investment=solph.Investment(
        ep_costs=300,
        # nonconvex=True,
        nonconvex=False,
        offset=0,
        maximum=100000,
        # minimum=30,
    ),
    invest_relation_input_capacity=1/4,
    invest_relation_output_capacity=1/4,
    inputs={bus_1: solph.Flow()},
    outputs={bus_1: solph.Flow()},
    loss_rate=0,
    inflow_conversion_factor=1,
    outflow_conversion_factor=1)

# #########################################################################
# Optimise the energy system
# #########################################################################

om = solph.Model(es)

om.solve(solver='cbc', solve_kwargs={'tee': False})

# ##########################################################################
# Check and plot results
# ##########################################################################

results = processing.results(om)

bus1 = views.node(results, 'bus_1')["sequences"]

# plot the time series (sequences) of a specific component/bus
if plt is not None:
    bus1.plot(kind='line', drawstyle='steps-mid')
    plt.legend()
    plt.show()

E_demand = views.node(results, 'bus_1')['sequences'][
    (('bus_1', 'demand'), 'flow')].sum()

E_source_vol = views.node(results, 'bus_1')['sequences'][
    (('source_vol', 'bus_1'), 'flow')].sum()

E_excess = views.node(results, 'bus_1')['sequences'][
    (('bus_1', 'excess'), 'flow')].sum()

E_source_1 = views.node(results, 'bus_1')['sequences'][
    (('source_1', 'bus_1'), 'flow')].sum()

print('')
print('Energy source_vol: ', E_source_vol)
print('Energy source_1: ', E_source_1)
print('Energy demand: ', E_demand)
print('Energy excess: ', E_excess)
print('')
print('Energy source total: ', E_source_vol + E_source_1)
print('Energy sink total: ', E_demand + E_excess)
print('')

C_storage = views.node(results, 'storage')['scalars'][
    (('storage', 'None'), 'invest')]

print('')
print('Size of Storage: ', C_storage)

es.results['meta'] = processing.meta_results(om)
objective = pd.DataFrame.from_dict(es.results['meta']).at[
    'Lower bound', 'objective']

print('')
print('Objective value: ', objective)
