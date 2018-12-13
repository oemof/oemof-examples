# -*- coding: utf-8 -*-

"""
General description
-------------------
This example illustrates the effect of activity_costs.

There are the following components:

    - demand_heat: heat demand (constant, for the sake of simplicity)
    - fireplace: wood firing, burns "for free" if somebody is around
    - boiler: gas firing, consumes (paid) gas


Installation requirements
-------------------------
This example requires version 0.3 of oemof. Install by:

    pip install 'oemof>=0.3'

"""

import numpy as np
import pandas as pd
import pprint as pp
import oemof.solph as solph
from oemof.outputlib import processing, views
from oemof.tools import economics

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

##########################################################################
# Calculate parameters and initialize the energy system and
##########################################################################

periods = 24
time = pd.date_range('1/1/2018', periods=periods, freq='D')

at_home = np.zeros(periods)
at_home[10:16] = 1

demand_heat = np.zeros(periods)
demand_heat[6:22] = 5

es = solph.EnergySystem(timeindex=time)

b_heat = solph.Bus(label='b_heat')

es.add(b_heat)

sink_heat = solph.Sink(
    label='demand',
    inputs={b_heat: solph.Flow(
        fixed=True,
        actual_value=demand_heat,
        nominal_value=1)})

fireplace = solph.Source(
    label='fireplace',
    outputs={b_heat: solph.Flow(nominal_value=10, activity_costs=1.0-at_home)})

boiler = solph.Source(
    label='boiler',
    outputs={b_heat: solph.Flow(nominal_value=10, variable_costs=0.2)})

es.add(sink_heat, fireplace, boiler)

##########################################################################
# Optimise the energy system
##########################################################################

# create an optimization problem and solve it
om = solph.Model(es)

# solve model
om.solve(solver='cbc', solve_kwargs={'tee': True})

##########################################################################
# Check and plot the results
##########################################################################

results = processing.results(om)

# plot data
if plt is not None:
    data = views.node(results, 'b_heat')['sequences']
    ax = data.plot(kind='line', drawstyle='steps-post', grid=True, rot=0)
    ax.set_xlabel('Time')
    ax.set_ylabel('Heat (arb. units)')
    plt.show()
