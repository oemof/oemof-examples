# -*- coding: utf-8 -*-

"""
General description
-------------------
Example that illustrates how to model min and max runtimes.

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

dummy_el = solph.Sink(
    label="dummy_el", inputs={bel: solph.Flow(variable_costs=10)}
)

pp1 = solph.Source(
    label="plant_min_down_constraints",
    outputs={
        bel: solph.Flow(
            nominal_value=10,
            min=0.5,
            max=1.0,
            variable_costs=10,
            nonconvex=solph.NonConvex(minimum_downtime=4, initial_status=0),
        )
    },
)

pp2 = solph.Source(
    label="plant_min_up_constraints",
    outputs={
        bel: solph.Flow(
            nominal_value=10,
            min=0.5,
            max=1.0,
            variable_costs=10,
            nonconvex=solph.NonConvex(minimum_uptime=2, initial_status=1),
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
    data[[(("bel", "demand_el"), "flow"), (("bel", "dummy_el"), "flow")]] *= -1
    exclude = ["dummy_el", "status"]
    columns = [
        c
        for c in data.columns
        if not any(s in c[0] or s in c[1] for s in exclude)
    ]
    data = data[columns]
    fig, ax = plt.subplots(figsize=(10, 5))
    data.plot(ax=ax, kind="line", drawstyle="steps-post", grid=True, rot=0)
    ax.set_xlabel("Hour")
    ax.set_ylabel("P [MW]")
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.3), ncol=1)
    fig.subplots_adjust(top=0.8)
    plt.show()
