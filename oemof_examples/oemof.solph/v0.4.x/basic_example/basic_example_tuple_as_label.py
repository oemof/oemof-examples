# -*- coding: utf-8 -*-

"""
General description
-------------------

You should have understood the basic_example to understand this one.

This is an example to show how the label attribute can be used with tuples to
manage the results of large energy system. Even though, the feature is
introduced in a small example it is made for large system.

In small energy system you normally address the node, you want your results
from, directly. In large systems you may want to group your results and collect
all power plants of a specific region or pv feed-in of all regions.

Therefore you can use named tuples as label. In a named tuple you need to
specify the fields:

>>> label = namedtuple('solph_label', ['region', 'tag1', 'tag2'])

>>> pv_label = label('region_1', 'renewable_source', 'pv')
>>> pp_gas_label = label('region_2', 'power_plant', 'natural_gas')
>>> demand_label = label('region_3', 'electricity', 'demand')

You always have to address all fields but you can use empty strings or None as
place holders.

>>> elec_bus = label('region_4', 'electricity', '')
>>> print(elec_bus)
solph_label(region='region_4', tag1='electricity', tag2='')

>>> elec_bus = label('region_4', 'electricity', None)
>>> print(elec_bus)
solph_label(region='region_4', tag1='electricity', tag2=None)

Now you can filter the results using the label or the instance:

>>> for key, value in results.items():  # Loop results (keys are tuples!)
...     if isinstance(key[0], solph.Sink) & (key[0].label.tag2 == 'demand'):
...         print("elec demand {0}: {1}".format(key[0].label.region,
...                                             value['sequences'].sum()))

elec demand region_1: 3456
elec demand region_2: 2467
...

In the example below a subclass is created to define ones own string output.
By default the output of a namedtuple is `field1=value1, field2=value2,...`:

>>> print(str(pv_label))
solph_label(region='region_1', tag1='renewable_source', tag2='pv')

With the subclass we created below the output is different, because we defined
our own string representation:

>>> new_pv_label = Label('region_1', 'renewable_source', 'pv')
>>> print(str(new_pv_label))
region_1_renewable_source_pv

You still will be able to get the original string using `repr`:

>>> print(repr(new_pv_label))
Label(tag1='region_1', tag2='renewable_source', tag3='pv')

This a helpful adaption for automatic plots etc..

Afterwards you can use `format` to define your own custom string.:
>>> print('{0}+{1}-{2}'.format(pv_label.region, pv_label.tag2, pv_label.tag1))
region_1+pv-renewable_source

Data
----
basic_example.csv


Installation requirements
-------------------------

This example requires the version v0.4.x of oemof. Install by:

    pip install 'oemof.solph>=0.4,<0.5'

Optional to see the plots:

    pip install matplotlib

"""

# ****************************************************************************
# ********** PART 1 - Define and optimise the energy system ******************
# ****************************************************************************

###############################################################################
# imports
###############################################################################
from collections import namedtuple

# Default logger of oemof
from oemof.tools import logger

from oemof import solph

import logging
import os
import pandas as pd
import pprint as pp

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

# Subclass of the named tuple with its own __str__ method.


class Label(namedtuple('solph_label', ['tag1', 'tag2', 'tag3'])):
    __slots__ = ()

    def __str__(self):
        """The string is used within solph as an ID, so it hast to be unique"""
        return '_'.join(map(str, self._asdict().values()))


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
filename = os.path.join(os.getcwd(), 'basic_example.csv')
data = pd.read_csv(filename)

##########################################################################
# Create oemof object
##########################################################################

logging.info('Create oemof objects')

# The bus objects were assigned to variables which makes it easier to connect
# components to these buses (see below).

# create natural gas bus
bgas = solph.Bus(label=Label('bus', 'gas', None))

# create electricity bus
bel = solph.Bus(label=Label('bus', 'electricity', None))

# adding the buses to the energy system
energysystem.add(bgas, bel)

# create excess component for the electricity bus to allow overproduction
energysystem.add(solph.Sink(label=Label('sink', 'electricity', 'excess'),
                            inputs={bel: solph.Flow()}))

# create source object representing the natural gas commodity (annual limit)
energysystem.add(solph.Source(
    label=Label('source', 'gas', 'commodity'), outputs={bgas: solph.Flow(
        nominal_value=29825293, summed_max=1)}))

# create fixed source object representing wind pow er plants
energysystem.add(solph.Source(
    label=Label('ee_source', 'electricity', 'wind'), outputs={bel: solph.Flow(
        fix=data['wind'], nominal_value=1000000)}))

# create fixed source object representing pv power plants
energysystem.add(solph.Source(
    label=Label('source', 'electricity', 'pv'), outputs={bel: solph.Flow(
        fix=data['pv'], nominal_value=582000)}))

# create simple sink object representing the electrical demand
energysystem.add(solph.Sink(
    label=Label('sink', 'electricity', 'demand'), inputs={bel: solph.Flow(
        fix=data['demand_el'], nominal_value=1)}))

# create simple transformer object representing a gas power plant
energysystem.add(solph.Transformer(
    label=Label('power plant', 'electricity', 'gas'),
    inputs={bgas: solph.Flow()},
    outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=50)},
    conversion_factors={bel: 0.58}))

# create storage object representing a battery
storage = solph.components.GenericStorage(
    nominal_storage_capacity=10077997,
    label=Label('storage', '', 'battery'),
    inputs={bel: solph.Flow(nominal_value=10077997/6)},
    outputs={bel: solph.Flow(nominal_value=10077997/6,
                             variable_costs=0.001)},
    loss_rate=0.00, initial_storage_level=None,
    inflow_conversion_factor=1, outflow_conversion_factor=0.8,
)

energysystem.add(storage)

##########################################################################
# Optimise the energy system and plot the results
##########################################################################

logging.info('Optimise the energy system')

# initialise the operational model
model = solph.Model(energysystem)

# This is for debugging only. It is not(!) necessary to solve the problem and
# should be set to False to save time and disc space in normal use. For
# debugging the timesteps should be set to 3, to increase the readability of
# the lp-file.
if debug:
    filename = os.path.join(
        solph.helpers.extend_basic_path('lp_files'), 'basic_example.lp')
    logging.info('Store lp-file in {0}.'.format(filename))
    model.write(filename, io_options={'symbolic_solver_labels': True})

# if tee_switch is true solver messages will be displayed
logging.info('Solve the optimization problem')
model.solve(solver=solver, solve_kwargs={'tee': solver_verbose})

logging.info('Store the energy system with the results.')

# The processing module of the outputlib can be used to extract the results
# from the model transfer them into a homogeneous structured dictionary.

# add results to the energy system to make it possible to store them.
energysystem.results['main'] = solph.processing.results(model)
energysystem.results['meta'] = solph.processing.meta_results(model)

# The default path is the '.oemof' folder in your $HOME directory.
# The default filename is 'es_dump.oemof'.
# You can omit the attributes (as None is the default value) for testing cases.
# You should use unique names/folders for valuable results to avoid
# overwriting.

# store energy system with results
energysystem.dump(dpath=None, filename=None)

# ****************************************************************************
# ********** PART 2 - Processing the results *********************************
# ****************************************************************************

logging.info('**** The script can be divided into two parts here.')
logging.info('Restore the energy system and the results.')
energysystem = solph.EnergySystem()
energysystem.restore(dpath=None, filename=None)

# define an alias for shorter calls below (optional)
results = energysystem.results['main']
print(energysystem.groups.keys())
storage = energysystem.groups["storage__battery"]

print('********* LABEL *********')
print(repr(storage.label))
print(str(storage.label))

# print a time slice of the state of charge
print('')
print('********* State of Charge (slice) *********')
print(results[(storage, None)]['sequences']['2012-02-25 08:00:00':
                                            '2012-02-26 15:00:00'])
print('')
print(str(storage.label))
print(type(storage))
# get all variables of a specific component/bus
# If you use the class the columns/index will be classes.
custom_storage = solph.views.node(results, storage)

# If you use a string the columns/index will be strings.
electricity_bus = solph.views.node(results, "bus_electricity_None")

# plot the time series (sequences) of a specific component/bus
if plt is not None:
    custom_storage['sequences'].plot(kind='line', drawstyle='steps-post')
    plt.show()
    electricity_bus['sequences'].plot(kind='line', drawstyle='steps-post')
    plt.show()

# print the solver results
print('********* Meta results *********')
pp.pprint(energysystem.results['meta'])
print('')

# print the sums of the flows around the electricity bus
print('********* Main results *********')
print(electricity_bus['sequences'].sum(axis=0))
