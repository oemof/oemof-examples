# -*- coding: utf-8 -*-

"""
General description:
---------------------
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
    Storage is not installed as the gas resource is cheapter.

    Have a look at different parameter settings. There are four variations
    of this example in the same folder.

Installation requirements:
---------------------------
This example requires oemof v0.2. Install by:

    pip install oemof

"""

###############################################################################
# Imports
###############################################################################

# Default logger of oemof
from oemof.tools import logger
from oemof.tools import helpers
from oemof.tools import economics

import oemof.solph as solph
from oemof.outputlib import processing, views

import logging
import os
import pandas as pd
import pprint as pp

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

number_timesteps = 8760
debug = True
silent = False

##########################################################################
# Initialize the energy system and read/calculate necessary parameters
##########################################################################

logger.define_logging()
logging.info('Initialize the energy system')
date_time_index = pd.date_range('1/1/2012', periods=number_timesteps,
                                freq='H')

energysystem = solph.EnergySystem(timeindex=date_time_index)

# Read data file
full_filename = os.path.join(os.path.dirname(__file__),
    'storage_investment.csv')
data = pd.read_csv(full_filename, sep=",")

price_gas = 0.04

# If the period is one year the equivalent periodical costs (epc) of an
# investment are equal to the annuity. Use oemof's economic tools.
epc_storage = economics.annuity(capex=1000, n=20, wacc=0.05)

##########################################################################
# Create oemof objects
##########################################################################

logging.info('Create oemof objects')
# create natural gas bus
bgas = solph.Bus(label="natural_gas")

# create electricity bus
bel = solph.Bus(label="electricity")

energysystem.add(bgas, bel)

# create excess component for the electricity bus to allow overproduction
excess = solph.Sink(label='excess_bel', inputs={bel: solph.Flow()})

# create source object representing the natural gas commodity (annual limit)
gas_resource = solph.Source(label='rgas', outputs={bgas: solph.Flow(
    variable_costs=price_gas)})

# create fixed source object representing wind power plants
wind = solph.Source(label='wind', outputs={bel: solph.Flow(
    actual_value=data['wind'], fixed=True,
    nominal_value=1000000)})

# create fixed source object representing pv power plants
pv = solph.Source(label='pv', outputs={bel: solph.Flow(
    actual_value=data['pv'], fixed=True,
    nominal_value=600000)})

# create simple sink object representing the electrical demand
demand = solph.Sink(label='demand', inputs={bel: solph.Flow(
    actual_value=data['demand_el'], fixed=True, nominal_value=1)})

# create simple transformer object representing a gas power plant
pp_gas = solph.Transformer(
    label="pp_gas",
    inputs={bgas: solph.Flow()},
    outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=0)},
    conversion_factors={bel: 0.58})

# my_list = [0.1] * number_timesteps

# create storage object representing a battery
storage = solph.components.GenericStorage(
    label='storage',
    # min=my_list,
    inputs={bel: solph.Flow(variable_costs=0.0001)},
    outputs={bel: solph.Flow()},
    capacity_loss=0.00, initial_capacity=0,
    nominal_input_capacity_ratio=1/6,
    nominal_output_capacity_ratio=1/6,
    inflow_conversion_factor=1, outflow_conversion_factor=0.8,
    investment=solph.Investment(ep_costs=epc_storage),
)

energysystem.add(excess, gas_resource, wind, pv, demand, pp_gas, storage)

##########################################################################
# Optimise the energy system
##########################################################################

logging.info('Optimise the energy system')

# initialise the operational model
om = solph.Model(energysystem)
# if debug is true an lp-file will be written
if debug:
    filename = os.path.join(
        helpers.extend_basic_path('lp_files'), 'storage_invest.lp')
    logging.info('Store lp-file in {0}.'.format(filename))
    om.write(filename, io_options={'symbolic_solver_labels': True})

# if tee_switch is true solver messages will be displayed
logging.info('Solve the optimization problem')
om.solve(solver='cbc', solve_kwargs={'tee': True})

# Check dump and restore
energysystem.dump()
energysystem = solph.EnergySystem(timeindex=date_time_index)
energysystem.restore()

##########################################################################
# Check and plot the results
##########################################################################

# check if the new result object is working for custom components
results = processing.results(om)

custom_storage = views.node(results, 'storage')
electricity_bus = views.node(results, 'electricity')

if not silent:
    meta_results = processing.meta_results(om)
    pp.pprint(meta_results)

    my_results = electricity_bus['scalars']
    my_results['storage_invest_GWh'] = results[(storage, None)]['scalars']['invest']/1e6
    my_results['res_share'] = 1 - results[(pp_gas, bel)]['sequences'].sum()/results[(bel, demand)]['sequences'].sum()
    pp.pprint(my_results)


if plt is not None and not silent:
    custom_storage['sequences'].plot(kind='line', drawstyle='steps-post')
    plt.show()

    electricity_bus['sequences'].plot(kind='line', drawstyle='steps-post')
    plt.show()

