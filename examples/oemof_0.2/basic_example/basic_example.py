# -*- coding: utf-8 -*-

"""
General description:
---------------------

A basic example to show how to model a simple energy system with oemof.solph.

The following energy system is modeled:

                input/output  bgas     bel
                     |          |        |       |
                     |          |        |       |
 wind(FixedSource)   |------------------>|       |
                     |          |        |       |
 pv(FixedSource)     |------------------>|       |
                     |          |        |       |
 rgas(Commodity)     |--------->|        |       |
                     |          |        |       |
 demand(Sink)        |<------------------|       |
                     |          |        |       |
                     |          |        |       |
 pp_gas(Transformer) |<---------|        |       |
                     |------------------>|       |
                     |          |        |       |
 storage(Storage)    |<------------------|       |
                     |------------------>|       |

Installation requirements:
---------------------------

This example requires the version v0.2.x of oemof. Install by:

    pip install 'oemof>=0.2,<0.3'

Optional:

    pip install matplotlib

"""

# ****************************************************************************
# ********** PART 1 - Define and optimise the energy system ******************
# ****************************************************************************

###############################################################################
# imports
###############################################################################

# Default logger of oemof
from oemof.tools import logger
from oemof.tools import helpers

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


solver = 'cbc'  # 'glpk', 'gurobi',....
debug = False  # Set number_of_timesteps to 3 to get a readable lp-file.
number_of_time_steps = 24*7*8
solver_verbose = False  # show/hide solver output

# initiate the logger (see the API docs for more information)
logger.define_logging(logfile='oemof_example.log',
                      screen_level=logging.INFO,
                      file_level=logging.DEBUG)

logging.info('Initialize the energy system')
date_time_index = pd.date_range('1/1/2012', periods=number_of_time_steps,
                                freq='H')

energysystem = solph.EnergySystem(timeindex=date_time_index)

# Read data file
filename = os.path.join(os.path.dirname(__file__), 'basic_example.csv')
data = pd.read_csv(filename)

##########################################################################
# Create oemof object
##########################################################################

logging.info('Create oemof objects')
# create natural gas bus
bgas = solph.Bus(label="natural_gas")

# create electricity bus
bel = solph.Bus(label="electricity")

energysystem.add(bgas, bel)

# create excess component for the electricity bus to allow overproduction
energysystem.add(solph.Sink(label='excess_bel', inputs={bel: solph.Flow()}))

# create source object representing the natural gas commodity (annual limit)
energysystem.add(solph.Source(label='rgas', outputs={bgas: solph.Flow(
    nominal_value=29825293, summed_max=1)}))

# create fixed source object representing wind power plants
energysystem.add(solph.Source(label='wind', outputs={bel: solph.Flow(
    actual_value=data['wind'], nominal_value=1000000, fixed=True)}))

# create fixed source object representing pv power plants
energysystem.add(solph.Source(label='pv', outputs={bel: solph.Flow(
    actual_value=data['pv'], nominal_value=582000, fixed=True)}))

# create simple sink object representing the electrical demand
energysystem.add(solph.Sink(label='demand', inputs={bel: solph.Flow(
    actual_value=data['demand_el'], fixed=True, nominal_value=1)}))

# create simple transformer object representing a gas power plant
energysystem.add(solph.Transformer(
    label="pp_gas",
    inputs={bgas: solph.Flow()},
    outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=50)},
    conversion_factors={bel: 0.58}))

# create storage object representing a battery
storage = solph.components.GenericStorage(
    nominal_capacity=10077997,
    label='storage',
    inputs={bel: solph.Flow(variable_costs=10e10)},
    outputs={bel: solph.Flow(variable_costs=10e10)},
    capacity_loss=0.00, initial_capacity=0,
    nominal_input_capacity_ratio=1/6,
    nominal_output_capacity_ratio=1/6,
    inflow_conversion_factor=1, outflow_conversion_factor=0.8,
)

energysystem.add(storage)

##########################################################################
# Optimise the energy system and plot the results
##########################################################################

logging.info('Optimise the energy system')

# initialise the operational model
om = solph.Model(energysystem)

# This is for debugging only. It is not(!) necessary to solve the problem and
# should be set to False to save time and disc space in normal use. For
# debugging the timesteps should be set to 3, to increase the readability of the
# lp-file.
if debug:
    filename = os.path.join(
        helpers.extend_basic_path('lp_files'), 'storage_invest.lp')
    logging.info('Store lp-file in {0}.'.format(filename))
    om.write(filename, io_options={'symbolic_solver_labels': True})

# if tee_switch is true solver messages will be displayed
logging.info('Solve the optimization problem')
om.solve(solver=solver, solve_kwargs={'tee': solver_verbose})

logging.info('Store the energy system with the results.')

# Add results to the energy system
energysystem.results['main'] = processing.results(om)
energysystem.results['meta'] = processing.meta_results(om)

# Store energy system with results
# The default path is the '.oemof' folder in your $HOME directory.
# The default filename is 'es_dump.oemof'.
# You can omit the attributes (as None is the default value) for testing cases.
# You should use unique names/folders for valuable results to avoid overwriting.
energysystem.dump(dpath=None, filename=None)

# ****************************************************************************
# ********** PART 2 - Processing the results *********************************
# ****************************************************************************

logging.info('**** The script can be divided into two parts here.')
logging.info('Restore the energy system and the results.')
energysystem = solph.EnergySystem()
energysystem.restore(dpath=None, filename=None)

# check if the new result object is working for custom components
results = energysystem.results['main']
meta_results = energysystem.results['meta']

storage = energysystem.groups['storage']
print('')
print('********* State of Charge (slice) *********')
print(results[(storage, None)]['sequences']['2012-02-25 08:00:00':
                                            '2012-02-26 15:00:00'])
print('')

custom_storage = views.node(results, 'storage')
electricity_bus = views.node(results, 'electricity')

if plt is not None:
    custom_storage['sequences'].plot(kind='line', drawstyle='steps-post')
    plt.show()
    electricity_bus['sequences'].plot(kind='line', drawstyle='steps-post')
    plt.show()

my_results = electricity_bus['sequences'].sum(axis=0).to_dict()


print('********* Meta results *********')
pp.pprint(meta_results)
print('')
print('********* Main results *********')
pp.pprint(my_results)
