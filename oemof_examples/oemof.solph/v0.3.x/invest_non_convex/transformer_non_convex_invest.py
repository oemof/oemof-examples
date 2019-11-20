# -*- coding: utf-8 -*-

"""
General description
-------------------
This example illustrates the difference between a convex and a non-convex
investment within a flow. By using a non-convex investment a threshold for
a minimum dimension of a transformer and "investment fix-costs" can be
implemented.
Note that the attribute 'minimum' of the Investment-class leads to two
different cases whether a convex or a non-convex investment is applied. In
case of a convex investment the minimum represents the capacity which is
forced to be installed. In case of a non-convex investment the installed
capacity of a flow can become zero as well.


The following energy system is modeled:

                   bus_0                bus_1
                     |                   |
                     |                   |
   source_0 -------->|--> transformer -->|
                     |                   |
                     |                   |-----> demand
                     |                   |
   source_1 ---------------------------->|
                     |                   |
                     |                   |

There are two options for fulfilling the demand:

 a) by transformer, which is supplied by a cheap source_0. The transformer is
 just available from a certain size (e.g. 20 kW) and has fix (independent of
 the installed capacity) investment costs.

 b) by source_1, which is very expensive, but no additional transformer needs
 to be installed.


Tutorial
--------
Un-comment and comment the parameter code blocks to check out the
different functionality of the investment class.


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

# demand series
data = [0, 5, 10, 15, 20, 25, 30, 25, 20, 15, 10, 5, 0]

# parameters set I
# todo: set the n_convex parameter to False
# results: due to the additional fix investment costs the investment in
# transformer is done, because there are no fix investment costs
c_0 = 5                 # costs source_0 [€/kW]
c_1 = 150               # costs source_1 [€/kW]
c_invest_var = 100      # costs investement in [€/kW_install]
c_invest_fix = 25000    # costs investment fix [€]
invest_max = 1000       # maximum transformer size [kW]
n_convex = True        # decide if there should be a non-convex investment
invest_min = 10         # minimum transformer size [kW]

# # parameters set II
# # todo: set the investment threshold from 50 to 40
# # results: due to a lower investment threshold the investment is done in case
# # of an investment minimum of 40 (kW)
# c_0 = 5                 # costs source_0 [€/kW]
# c_1 = 150               # costs source_1 [€/kW]
# c_invest_var = 500      # costs investement in [€/kW_install]
# c_invest_fix = 1000    # costs investment fix [€]
# invest_max = 1000       # maximum transformer size [kW]
# n_convex = True       # decide if there should be a non-convex investment
# invest_min = 50         # minimum transformer size [kW]

# # parameters set III
# # todo: set the n_convex parameter to False
# # results: in that case the investment is done, because it is forced. If a
# # minimum value for the investment is given and nonconvex is not set to True,
# # the minimum investment is forced.
# c_0 = 5                 # costs source_0 [€/kW]
# c_1 = 150               # costs source_1 [€/kW]
# c_invest_var = 500      # costs investement in [€/kW_install]
# c_invest_fix = 1000    # costs investment fix [€]
# invest_max = 1000       # maximum transformer size [kW]
# n_convex = True       # decide if there should be a non-convex investment
# invest_min = 50         # minimum transformer size [kW]


# create an energy system
idx = pd.date_range('1/1/2018', periods=len(data) - 1, freq='H')
es = solph.EnergySystem(timeindex=idx)
Node.registry = es

bus_0 = solph.Bus(label='bus_0')
bus_1 = solph.Bus(label='bus_1')

solph.Source(label='source_0',
             outputs={bus_0: solph.Flow(variable_costs=c_0)})

solph.Source(label='source_1',
             outputs={bus_1: solph.Flow(variable_costs=c_1)})

solph.Sink(label='demand', inputs={
    bus_1: solph.Flow(fixed=True, actual_value=data,  nominal_value=1)})

# non-convex investment transformer with offset
trafo = solph.Transformer(
    label='transformer',
    inputs={bus_0: solph.Flow()},
    outputs={bus_1: solph.Flow(
        nominal_value=None,
        investment=solph.Investment(
            ep_costs=c_invest_var, maximum=invest_max, minimum=invest_min,
            nonconvex=n_convex, offset=c_invest_fix),
        )},
    conversion_factors={bus_1: 0.5})

# create an optimization problem and solve it
om = solph.Model(es)

# solve model
om.solve(solver='cbc', solve_kwargs={'tee': False})

# create result object
results = processing.results(om)

bus1 = views.node(results, 'bus_1')["sequences"]

# plot the time series (sequences) of a specific component/bus
if plt is not None:
    bus1.plot(kind='line', drawstyle='steps-mid')
    plt.legend()
    plt.show()

# ###########################################################################
# analyse cost structure of optimization
# ###########################################################################

# costs variant a)
E_transformer = views.node(results, 'transformer')['sequences'][
    (('bus_0', 'transformer'), 'flow')].sum()

P_install = views.node(results, 'transformer')['scalars'][
    (('transformer', 'bus_1'), 'invest')]

if n_convex:
    install_status = views.node(results, 'transformer')['scalars'][
        (('transformer', 'bus_1'), 'invest_status')]
else:
    install_status = 0

C_var = E_transformer * c_0
C_invest = P_install * c_invest_var + install_status * c_invest_fix

C_a = C_var + C_invest

# costs variant b)
E_source_1 = views.node(results, 'source_1')['sequences'][
    (('source_1', 'bus_1'), 'flow')].sum()

C_b = E_source_1 * c_1

# total costs
C_total = C_a + C_b

es.results['meta'] = processing.meta_results(om)
objective = pd.DataFrame.from_dict(es.results['meta']).at[
    'Lower bound', 'objective']

# print results of cost analysis
print('')
print('Option a)')
print('    commodity costs: ', C_var)
print('    investment costs: ', C_invest)
print('Option b)')
print('    commodity costs: ', C_b)
print('')
print('Total Costs recalculation: ', C_total, ' Objective value: ', objective)
