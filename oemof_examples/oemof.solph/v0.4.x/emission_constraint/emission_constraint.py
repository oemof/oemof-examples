# -*- coding: utf-8 -*-

"""
General description
-------------------
Example that shows how to add an emission constraint in a model.

Installation requirements
-------------------------
This example requires the version v0.4.x of oemof. Install by:

    pip install 'oemof.solph>=0.4,<0.5'

"""

__copyright__ = "oemof developer group"
__license__ = "MIT"

import pandas as pd
from oemof import solph
from oemof.solph import constraints

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

# create energy system
energysystem = solph.EnergySystem(
    timeindex=pd.date_range("1/1/2012", periods=3, freq="H")
)

# create gas bus
bgas = solph.Bus(label="gas")

# create electricity bus
bel = solph.Bus(label="electricity")

# adding the buses to the energy system
energysystem.add(bel, bgas)

# create fixed source object representing biomass plants
energysystem.add(
    solph.Source(
        label="biomass",
        outputs={
            bel: solph.Flow(
                nominal_value=100,
                variable_costs=10,
                emission_factor=0.01,
                fix=[0.1, 0.2, 0.3],
            )
        },
    )
)

# create source object representing the gas commodity
energysystem.add(
    solph.Source(
        label="gas-source",
        outputs={bgas: solph.Flow(variable_costs=10, emission_factor=0.2)},
    )
)

energysystem.add(
    solph.Sink(
        label="demand",
        inputs={
            bel: solph.Flow(
                nominal_value=200, variable_costs=10, fix=[0.1, 0.2, 0.3]
            )
        },
    )
)

# create simple transformer object representing a gas power plant
energysystem.add(
    solph.Transformer(
        label="pp_gas",
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=200)},
        conversion_factors={bel: 0.58},
    )
)

# initialise the operational model
model = solph.Model(energysystem)

# add the emission constraint
constraints.emission_limit(model, limit=100)

# print out the emission constraint
model.integral_limit_emission_factor_constraint.pprint()
model.integral_limit_emission_factor.pprint()

# solve the model
model.solve()

# print out the amount of emissions from the emission constraint
print(model.integral_limit_emission_factor())

results = solph.processing.results(model)

if plt is not None:
    data = solph.views.node(results, "electricity")["sequences"]
    ax = data.plot(kind="line", grid=True)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("P (MW)")
    plt.show()
