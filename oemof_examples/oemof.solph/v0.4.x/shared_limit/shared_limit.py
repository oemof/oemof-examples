# -*- coding: utf-8 -*-

"""
General description
-------------------
Example that shows how to add an `shared_limit` constraint to a model.


The following energy system is modeled with four time steps:

s1 --> b1 --> | --> d1
              | <-> storage1

s2a -->|--> b2 --> | --> d2
s2b -->|           | <-> storage2

- The storages, storage1 and storage2, have no losses at all.
- The demands, d1 and d2, are active at steps 3 and 4, respectively.
- The supplies, s1, s2a, and s2b are active at steps 1, 2, and 3, respectively.
  Usage of supply s2a is significantly cheaper then the usage of s2b.

In step 1, s1 has to be used to store in storage1 and fulfill d1 later in step 3.
Despite being the cheaper option, d2 cannot be fully covered by s2a because
storage1 and storage2 have a shared limit.
So, in step 3 -- when d1 was active -- the rest needed to fulfill d2
is stored in storage2 coming from the (now active but more expansive) s2b.

Installation requirements
-------------------------
This example requires the version v0.4.x of oemof. Install by:
    pip install 'oemof>=0.4,<0.5'
"""

__copyright__ = "oemof developer group"
__license__ = "MIT"

import pandas as pd
import oemof.solph as solph

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

pd.plotting.register_matplotlib_converters()

# create energy system
energysystem = solph.EnergySystem(
                    timeindex=pd.date_range('1/1/2012', periods=4, freq='H'))

# create buses
b1 = solph.Bus(label="b1")
b2 = solph.Bus(label="b2")

# adding the buses to the energy system
energysystem.add(b1, b2)

energysystem.add(solph.Source(label='s1',
                              outputs={b1: solph.Flow(
                                  max=[0, 1, 0, 0],
                                  nominal_value=5)}))
energysystem.add(solph.Source(label='s2a',
                              outputs={b2: solph.Flow(
                                  nominal_value=5,
                                  max=[1, 0, 0, 0])}))
energysystem.add(solph.Source(label='s2b',
                              outputs={b2: solph.Flow(
                                  max=[0, 0, 1, 0],
                                  nominal_value=5,
                                  variable_costs=10)}))

energysystem.add(solph.Sink(label='d1',
                            inputs={b1: solph.Flow(
                                nominal_value=5,
                                fix=[0, 0, 1, 0])}))
energysystem.add(solph.Sink(label='d2',
                            inputs={b2: solph.Flow(
                                nominal_value=5,
                                fix=[0, 0, 0, 1])}))

# create simple transformer object representing a gas power plant
storage1 = solph.components.GenericStorage(
    label="storage1",
    nominal_storage_capacity=5,
    inputs={b1: solph.Flow()},
    outputs={b1: solph.Flow()})
storage2 = solph.components.GenericStorage(
    label="storage2",
    nominal_storage_capacity=5,
    inputs={b2: solph.Flow()},
    outputs={b2: solph.Flow()})

energysystem.add(storage1, storage2)

# initialise the operational model
model = solph.Model(energysystem)

components = [storage1, storage2]

# add the shared limit constraint
solph.constraints.shared_limit(model,
                               model.GenericStorageBlock.storage_content,
                               "limit_storage", components,
                               [0.5, 1.25], upper_limit=7)

model.solve()

results = solph.processing.results(model)

if plt is not None:
    plt.figure()
    plt.plot(results[(storage1, None)]['sequences'],
             label="storage1")
    plt.plot(results[(storage2, None)]['sequences'],
             label="storage2")
    plt.plot(results[('limit_storage', 'limit_storage')]['sequences'],
             label="weighted sum")
    plt.grid()
    plt.legend()

    plt.show()
