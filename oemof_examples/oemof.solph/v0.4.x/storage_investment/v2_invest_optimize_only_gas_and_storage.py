# -*- coding: utf-8 -*-

"""
General description
-------------------
This example shows how to perform a capacity optimization for
an energy system with storage. The following energy system is modeled:

                input/output  bgas     bel
                     |          |        |       |
                     |          |        |       |
 wind(FixedSource)   |------------------>|       |
                     |          |        |       |
 pv(FixedSource)     |------------------>|       |
                     |          |        |       |
 gas_resource        |--------->|        |       |
 (Commodity)         |          |        |       |
                     |          |        |       |
 demand(Sink)        |<------------------|       |
                     |          |        |       |
                     |          |        |       |
 pp_gas(Transformer) |<---------|        |       |
                     |------------------>|       |
                     |          |        |       |
 storage(Storage)    |<------------------|       |
                     |------------------>|       |

The example exists in four variations. The following parameters describe
the main setting for the optimization variation 2:

    - optimize gas_resource and storage
    - set installed capacities for wind and pv
    - set investment cost for storage
    - set gas price for kWh

    Results show a higher renewable energy share than in variation 1
    (78% compared to 51%) due to preinstalled renewable capacities.
    Storage is not installed as the gas resource is cheaper.

    Have a look at different parameter settings. There are four variations
    of this example in the same folder.

Installation requirements
-------------------------
This example requires the version v0.4.x of oemof. Install by:

    pip install 'oemof.solph>=0.4,<0.5'

"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

###############################################################################
# Imports
###############################################################################

# Default logger of oemof
from oemof.tools import logger
from oemof.tools import economics
from oemof import solph

import logging
import os
import pandas as pd
import pprint as pp

number_timesteps = 8760

##########################################################################
# Initialize the energy system and read/calculate necessary parameters
##########################################################################

logger.define_logging()
logging.info("Initialize the energy system")
date_time_index = pd.date_range("1/1/2012", periods=number_timesteps, freq="H")

energysystem = solph.EnergySystem(timeindex=date_time_index)

# Read data file
full_filename = os.path.join(os.getcwd(), "storage_investment.csv")
data = pd.read_csv(full_filename, sep=",")

price_gas = 0.04

# If the period is one year the equivalent periodical costs (epc) of an
# investment are equal to the annuity. Use oemof's economic tools.
epc_storage = economics.annuity(capex=1000, n=20, wacc=0.05)

##########################################################################
# Create oemof objects
##########################################################################

logging.info("Create oemof objects")
# create natural gas bus
bgas = solph.Bus(label="natural_gas")

# create electricity bus
bel = solph.Bus(label="electricity")

energysystem.add(bgas, bel)

# create excess component for the electricity bus to allow overproduction
excess = solph.Sink(label="excess_bel", inputs={bel: solph.Flow()})

# create source object representing the natural gas commodity (annual limit)
gas_resource = solph.Source(
    label="rgas", outputs={bgas: solph.Flow(variable_costs=price_gas)}
)

# create fixed source object representing wind power plants
wind = solph.Source(
    label="wind",
    outputs={bel: solph.Flow(fix=data["wind"], nominal_value=1000000)},
)

# create fixed source object representing pv power plants
pv = solph.Source(
    label="pv", outputs={bel: solph.Flow(fix=data["pv"], nominal_value=600000)}
)

# create simple sink object representing the electrical demand
demand = solph.Sink(
    label="demand",
    inputs={bel: solph.Flow(fix=data["demand_el"], nominal_value=1)},
)

# create simple transformer object representing a gas power plant
pp_gas = solph.Transformer(
    label="pp_gas",
    inputs={bgas: solph.Flow()},
    outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=0)},
    conversion_factors={bel: 0.58},
)

# create storage object representing a battery
storage = solph.components.GenericStorage(
    label="storage",
    inputs={bel: solph.Flow(variable_costs=0.0001)},
    outputs={bel: solph.Flow()},
    loss_rate=0.00,
    initial_storage_level=0,
    invest_relation_input_capacity=1 / 6,
    invest_relation_output_capacity=1 / 6,
    inflow_conversion_factor=1,
    outflow_conversion_factor=0.8,
    investment=solph.Investment(ep_costs=epc_storage),
)

energysystem.add(excess, gas_resource, wind, pv, demand, pp_gas, storage)

##########################################################################
# Optimise the energy system
##########################################################################

logging.info("Optimise the energy system")

# initialise the operational model
om = solph.Model(energysystem)

# if tee_switch is true solver messages will be displayed
logging.info("Solve the optimization problem")
om.solve(solver="cbc", solve_kwargs={"tee": True})

##########################################################################
# Check and plot the results
##########################################################################

# check if the new result object is working for custom components
results = solph.processing.results(om)

custom_storage = solph.views.node(results, "storage")
electricity_bus = solph.views.node(results, "electricity")

meta_results = solph.processing.meta_results(om)
pp.pprint(meta_results)

my_results = electricity_bus["scalars"]

# installed capacity of storage in GWh
my_results["storage_invest_GWh"] = (
    results[(storage, None)]["scalars"]["invest"] / 1e6
)

# resulting renewable energy share
my_results["res_share"] = (
    1
    - results[(pp_gas, bel)]["sequences"].sum()
    / results[(bel, demand)]["sequences"].sum()
)

pp.pprint(my_results)
