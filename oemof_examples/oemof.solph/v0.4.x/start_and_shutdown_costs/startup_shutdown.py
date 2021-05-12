# -*- coding: utf-8 -*-

"""
General description
-------------------
Example that illustrates how to model startup and shutdown costs attributed
to a binary flow.

Installation requirements
-------------------------
This example requires the version v0.4.x of oemof. Install by:

    pip install 'oemof.solph>=0.4,<0.5'

"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

import os
import pandas as pd
from oemof import solph
from oemof.network.network import Node

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


# read sequence data
full_filename = os.path.join(os.getcwd(), "data.csv")
data = pd.read_csv(full_filename, sep=",")

# select periods
periods = len(data) - 1

# create an energy system
idx = pd.date_range("1/1/2017", periods=periods, freq="H")
es = solph.EnergySystem(timeindex=idx)
Node.registry = es

# power bus and components
bel = solph.Bus(label="bel")

demand_el = solph.Sink(
    label="demand_el",
    inputs={bel: solph.Flow(fix=data["demand_el"], nominal_value=10)},
)

# pp1 and pp2 are competing to serve overall 12 units load at lowest cost
# summed costs for pp1 = 12 * 10 * 10.25 = 1230
# summed costs for pp2 = 4*5 + 4*5 + 12 * 10 * 10 = 1240
# => pp1 serves the load despite of higher variable costs since
#    the start and shutdown costs of pp2 change its marginal costs
pp1 = solph.Source(
    label="power_plant1",
    outputs={bel: solph.Flow(nominal_value=10, variable_costs=10.25)},
)

# shutdown costs only work in combination with a minimum load
# since otherwise the status variable is "allowed" to be active i.e.
# it permanently has a value of one which does not allow to set the shutdown
# variable which is set to one if the status variable changes from one to zero
pp2 = solph.Source(
    label="power_plant2",
    outputs={
        bel: solph.Flow(
            nominal_value=10,
            min=0.5,
            max=1.0,
            variable_costs=10,
            nonconvex=solph.NonConvex(startup_costs=5, shutdown_costs=5),
        )
    },
)

# create an optimization problem and solve it
om = solph.Model(es)

# debugging
# om.write('problem.lp', io_options={'symbolic_solver_labels': True})

# solve model
om.solve(solver="cbc", solve_kwargs={"tee": True})

# create result object
results = solph.processing.results(om)

# plot data
if plt is not None:
    # plot electrical bus
    data = solph.views.node(results, "bel")["sequences"]
    data[(("bel", "demand_el"), "flow")] *= -1
    columns = [
        c
        for c in data.columns
        if not any(s in c for s in ["status", "startup", "shutdown"])
    ]
    data = data[columns]
    ax = data.plot(kind="line", drawstyle="steps-post", grid=True, rot=0)
    ax.set_xlabel("Hour")
    ax.set_ylabel("P (MW)")
    plt.show()
