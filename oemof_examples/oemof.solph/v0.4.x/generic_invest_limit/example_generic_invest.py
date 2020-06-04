# -*- coding: utf-8 -*-
"""
Example that shows how to use "Generic Investment Limit".

There are two supply chains. The energy systems looks like that:

              bus_a_0          bus_a_1
               |                 |
source_a_0 --->|---> trafo_a --->|--->demand_a
                                 |
                   source_a_1--->|
                                 |

              bus_b_0          bus_b_1
               |                 |
source_b_0 --->|---> trafo_b --->|--->demand_b
                                 |
                   source_b_1--->|
                                 |

Everything is identical: the costs for the sources, the demand, the efficiency
of the Transformer. And both Transformer have an investment at the output.
The source '*_1' is in both cases very expensive, so that
a investment is probably done in the transformer.
Now, both investments share a third resource, which is called "space" in this
example. (This could be anything, and you could use as many additional
resources as you want.) And this resource is limited. In this case, every
Transformer capacity unit, which might be installed, needs 2 space for
'trafo a', and 1 space per installed capacity for 'trafo b'.
And the total space is limited to 24.
See what happens, have fun ... ;)

Johannes Röder

"""

import os
import pandas as pd
import oemof.solph as solph
import matplotlib.pyplot as plt
from oemof.network.network import Node
from oemof.solph import processing, views
from oemof.solph import helpers
import logging


data = [0, 15, 30, 35, 20, 25, 27, 10, 5, 2, 15, 40, 20, 0, 0]

# select periods
periods = 14

# create an energy system
idx = pd.date_range('1/1/2020', periods=periods, freq='H')
es = solph.EnergySystem(timeindex=idx)
Node.registry = es

# Parameter: costs for the sources
c_0 = 10
c_1 = 100

epc_invest = 500

# commodity a
bus_a_0 = solph.Bus(label='bus_a_0')
bus_a_1 = solph.Bus(label='bus_a_1')

solph.Source(label='source_a_0',
             outputs={bus_a_0: solph.Flow(variable_costs=c_0)})

solph.Source(label='source_a_1',
             outputs={bus_a_1: solph.Flow(variable_costs=c_1)})

solph.Sink(label='demand_a', inputs={
    bus_a_1: solph.Flow(fix=data,  nominal_value=1)})

# commodity b
bus_b_0 = solph.Bus(label='bus_b_0')
bus_b_1 = solph.Bus(label='bus_b_1')
solph.Source(label='source_b_0',
             outputs={bus_b_0: solph.Flow(variable_costs=c_0)})

solph.Source(label='source_b_1',
             outputs={bus_b_1: solph.Flow(variable_costs=c_1)})

solph.Sink(label='demand_b', inputs={
    bus_b_1: solph.Flow(fix=data,  nominal_value=1)})

# transformer a
solph.Transformer(
    label='trafo_a',
    inputs={bus_a_0: solph.Flow()},
    outputs={bus_a_1: solph.Flow(
        nominal_value=None,
        investment=solph.Investment(
            ep_costs=epc_invest,
            space=2,
        ),
        )},
    conversion_factors={bus_a_1: 0.8})

# transformer b
solph.Transformer(
    label='trafo_b',
    inputs={bus_b_0: solph.Flow()},
    outputs={bus_b_1: solph.Flow(
        nominal_value=None,
        investment=solph.Investment(
            ep_costs=epc_invest,
            space=1,
        ),
        )},
    conversion_factors={bus_a_1: 0.8})


# create an optimization problem and solve it
om = solph.Model(es)

# add constraint for generic investment limit
om = solph.constraints.additional_investment_flow_limit(om, "space", limit=24)

# export lp file
filename = os.path.join(
    helpers.extend_basic_path('lp_files'), 'GenericInvest.lp')
logging.info('Store lp-file in {0}.'.format(filename))
om.write(filename, io_options={'symbolic_solver_labels': True})

# solve model
om.solve(solver='cbc', solve_kwargs={'tee': True})

# create result object
results = processing.results(om)

bus1 = views.node(results, 'bus_a_1')["sequences"]
bus2 = views.node(results, 'bus_b_1')["sequences"]

# plot the time series (sequences) of a specific component/bus
if plt is not None:
    bus1.plot(kind='line', drawstyle='steps-mid')
    plt.legend()
    plt.show()
    bus2.plot(kind='line', drawstyle='steps-mid')
    plt.legend()
    plt.show()

space_used = om.invest_limit_space()
print('Space value: ', space_used)
print('Investment trafo_a: ', views.node(results, 'trafo_a')["scalars"][0])
print('Investment trafo_b: ', views.node(results, 'trafo_b')["scalars"][0])
