# -*- coding: utf-8 -*-

"""
General description
-------------------
Example that illustrates how to use custom component `GenericCHP` can be used.
In this case it is used to model a back pressure turbine.

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
full_filename = os.path.join(os.getcwd(), "generic_chp.csv")
data = pd.read_csv(full_filename, sep=",")

# select periods
periods = len(data) - 1

# create an energy system
idx = pd.date_range("1/1/2017", periods=periods, freq="H")
es = solph.EnergySystem(timeindex=idx)
Node.registry = es

# resources
bgas = solph.Bus(label="bgas")

rgas = solph.Source(label="rgas", outputs={bgas: solph.Flow()})

# heat
bth = solph.Bus(label="bth")

# dummy source at high costs that serves the residual load
source_th = solph.Source(
    label="source_th", outputs={bth: solph.Flow(variable_costs=1000)}
)

demand_th = solph.Sink(
    label="demand_th",
    inputs={bth: solph.Flow(fix=data["demand_th"], nominal_value=200)},
)

# power
bel = solph.Bus(label="bel")

demand_el = solph.Sink(
    label="demand_el",
    inputs={bel: solph.Flow(variable_costs=data["price_el"])},
)

# back pressure turbine with same parameters as btp
# (for back pressure characteristics Q_CW_min=0 and back_pressure=True)
bpt = solph.components.GenericCHP(
    label="back_pressure_turbine",
    fuel_input={
        bgas: solph.Flow(H_L_FG_share_max=[0.19 for p in range(0, periods)])
    },
    electrical_output={
        bel: solph.Flow(
            P_max_woDH=[200 for p in range(0, periods)],
            P_min_woDH=[80 for p in range(0, periods)],
            Eta_el_max_woDH=[0.53 for p in range(0, periods)],
            Eta_el_min_woDH=[0.43 for p in range(0, periods)],
        )
    },
    heat_output={bth: solph.Flow(Q_CW_min=[0 for p in range(0, periods)])},
    Beta=[0.0 for p in range(0, periods)],
    back_pressure=True,
)
# create an optimization problem and solve it
om = solph.Model(es)

# debugging
# om.write('generic_chp.lp', io_options={'symbolic_solver_labels': True})

# solve model
om.solve(solver="cbc", solve_kwargs={"tee": True})

# create result object
results = solph.processing.results(om)

# plot data
if plt is not None:
    # plot PQ diagram from component results
    data = results[(bpt, None)]["sequences"]
    ax = data.plot(kind="scatter", x="Q", y="P", grid=True)
    ax.set_xlabel("Q (MW)")
    ax.set_ylabel("P (MW)")
    plt.show()

    # plot thermal bus
    data = solph.views.node(results, "bth")["sequences"]
    ax = data.plot(kind="line", drawstyle="steps-post", grid=True)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Q (MW)")
    plt.show()
