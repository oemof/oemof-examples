# -*- coding: utf-8 -*-

"""
General description
-------------------
This example shows how to create an energysystem with oemof objects and
solve it with the solph module. Results are plotted with solph.

Dispatch modelling is a typical thing to do with solph. However cost does not
have to be monetary but can be emissions etc. In this example a least cost
dispatch of different generators that meet an inelastic demand is undertaken.
Some of the generators are renewable energies with marginal costs of zero.

Data
----
input_data.csv

Installation requirements
-------------------------
This example requires the version v0.4.x of oemof and matplotlib. Install by:

    pip install 'oemof.solph>=0.4,<0.5'

Optional to see the plots:

    pip install matplotlib
"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

import os
import pandas as pd
from oemof.solph import (
    Sink,
    Source,
    Transformer,
    Bus,
    Flow,
    Model,
    EnergySystem,
    views,
)

import matplotlib.pyplot as plt


solver = "cbc"

# Create an energy system and optimize the dispatch at least costs.
# ####################### initialize and provide data #####################

datetimeindex = pd.date_range("1/1/2016", periods=24 * 10, freq="H")
energysystem = EnergySystem(timeindex=datetimeindex)
filename = os.path.join(os.getcwd(), "input_data.csv")
data = pd.read_csv(filename, sep=",")

# ######################### create energysystem components ################

# Write variable costs in dictionary
variable_costs_dict = {"pp_coal": 25, "pp_lig": 19, "pp_gas": 40, "pp_oil": 50}
# Get Merit order of variable costs in dictionary
variable_costs_dict = dict(
    sorted(variable_costs_dict.items(), key=lambda item: item[1])
)

# resource buses
bcoal = Bus(label="coal", balanced=False)
bgas = Bus(label="gas", balanced=False)
boil = Bus(label="oil", balanced=False)
blig = Bus(label="lignite", balanced=False)

# electricity bus
bel = Bus(label="bel")

energysystem.add(bcoal, bgas, boil, blig, bel)

# an excess and a shortage variable can help to avoid infeasible problems
energysystem.add(Sink(label="excess_el", inputs={bel: Flow()}))
# shortage_el = Source(label='shortage_el',
#                      outputs={bel: Flow(variable_costs=200)})

# sources
energysystem.add(
    Source(label="wind", outputs={bel: Flow(fix=data["wind"], nominal_value=66.3)})
)

energysystem.add(
    Source(label="pv", outputs={bel: Flow(fix=data["pv"], nominal_value=65.3)})
)

# electricity demand
energysystem.add(
    Sink(
        label="demand_el", inputs={bel: Flow(nominal_value=85, fix=data["demand_el"])},
    )
)

# power plants
energysystem.add(
    Transformer(
        label="pp_coal",
        inputs={bcoal: Flow()},
        outputs={
            bel: Flow(nominal_value=20.2, variable_costs=variable_costs_dict["pp_coal"])
        },
        conversion_factors={bel: 0.39},
    )
)

energysystem.add(
    Transformer(
        label="pp_lig",
        inputs={blig: Flow()},
        outputs={
            bel: Flow(nominal_value=41.8, variable_costs=variable_costs_dict["pp_lig"])
        },
        conversion_factors={bel: 0.41},
    )
)

energysystem.add(
    Transformer(
        label="pp_gas",
        inputs={bgas: Flow()},
        outputs={
            bel: Flow(nominal_value=41, variable_costs=variable_costs_dict["pp_gas"])
        },
        conversion_factors={bel: 0.50},
    )
)

energysystem.add(
    Transformer(
        label="pp_oil",
        inputs={boil: Flow()},
        outputs={
            bel: Flow(nominal_value=5, variable_costs=variable_costs_dict["pp_oil"])
        },
        conversion_factors={bel: 0.28},
    )
)

# ################################ optimization ###########################

# create optimization model based on energy_system
optimization_model = Model(energysystem=energysystem)

optimization_model.receive_duals()

# solve problem
optimization_model.solve(solver=solver, solve_kwargs={"tee": True, "keepfiles": False})

# write back results from optimization object to energysystem
optimization_model.results()

# ################################ results ################################

# subset of results that includes all flows into and from electrical bus
# sequences are stored within a pandas.DataFrames and scalars e.g.
# investment values within a pandas.Series object.
# in this case the entry data['scalars'] does not exist since no investment
# variables are used
data = views.node(optimization_model.results(), "bel")
data["sequences"].info()
print("Optimization successful. Showing some results:")

# see: https://pandas.pydata.org/pandas-docs/stable/visualization.html
node_results_bel = views.node(optimization_model.results(), "bel")
node_results_flows = node_results_bel["sequences"]
bel_duals = node_results_flows.pop((("bel", "None"), "duals"))
node_results_flows = node_results_flows.drop(
    [(("bel", "demand_el"), "flow"), (("bel", "excess_el"), "flow")], 1
)

# Adjust node_results_flows to merit order
merit_order_columns = ["", ""]
for key, item in variable_costs_dict.items():
    for column in node_results_flows.columns:
        if "pv" in str(column):
            merit_order_columns[0] = column
        elif "wind" in str(column):
            merit_order_columns[1] = column
        if key in str(column):
            merit_order_columns.append(column)
node_results_flows = node_results_flows.reindex(columns=merit_order_columns)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
node_result_flows_list = []
for col in node_results_flows.columns:
    node_result_flows_list.append(node_results_flows[col])
ax1.stackplot(
    node_results_flows.index, node_result_flows_list, labels=node_results_flows.columns
)
ax2.plot(bel_duals, label="bel_duals")


ax1.set_title("Sums for optimization period")
ax1.set_ylabel("Power")
ax2.set_ylabel("Dual")
ax2.set_xlabel("Time")
ax1.legend(loc="center left", prop={"size": 8}, bbox_to_anchor=(1, 0.5))
ax2.legend(loc="center left", prop={"size": 8}, bbox_to_anchor=(1, 0.5))
ax2.tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.show()
