# -*- coding: utf-8 -*-

"""
General description:
---------------------

This example is not a real use case of an energy system but an example to show
how a variable combined heat and power plant (chp) works in contrast to a fixed
chp (eg. block device). Both chp plants distribute power and heat to a separate
heat and power Bus with a heat and power demand. The plot shows that the fixed
chp plant produces heat and power excess and therefore needs more natural gas.

"""

import logging
import os
import pandas as pd
import matplotlib.pyplot as plt
from oemof.tools import helpers
import oemof.solph as solph
from oemof import outputlib


def run_variable_chp_example(number_timesteps=192,
                             filename="variable_chp.csv", solver='cbc',
                             debug=True, tee_switch=True):

    logging.info('Initialize the energy system')

    # create time index for 192 hours in May.
    date_time_index = pd.date_range('5/5/2012', periods=number_timesteps,
                                    freq='H')
    energysystem = solph.EnergySystem(timeindex=date_time_index)

    # Read data file with heat and electrical demand (192 hours)
    full_filename = os.path.join(os.path.dirname(__file__), filename)
    data = pd.read_csv(full_filename, sep=",")

    ##########################################################################
    # Create oemof.solph objects
    ##########################################################################

    logging.info('Create oemof.solph objects')

    # container for instantiated nodes
    noded = {}

    # create natural gas bus
    noded['bgas'] = solph.Bus(label="natural_gas")

    # create commodity object for gas resource
    noded['rgas'] = solph.Source(
        label='rgas', outputs={noded['bgas']: solph.Flow(variable_costs=50)})

    # create two electricity buses and two heat buses
    noded['bel'] = solph.Bus(label="electricity")
    noded['bel2'] = solph.Bus(label="electricity_2")
    noded['bth'] = solph.Bus(label="heat")
    noded['bth2'] = solph.Bus(label="heat_2")

    # create excess components for the elec/heat bus to allow overproduction
    noded['excess_bth_2'] = solph.Sink(
        label='excess_bth_2', inputs={noded['bth2']: solph.Flow()})
    noded['excess_therm'] = solph.Sink(
        label='excess_therm', inputs={noded['bth']: solph.Flow()})
    noded['excess_bel_2'] = solph.Sink(
        label='excess_bel_2', inputs={noded['bel2']: solph.Flow()})
    noded['excess_elec'] = solph.Sink(
        label='excess_elec', inputs={noded['bel']: solph.Flow()})

    # create simple sink object for electrical demand for each electrical bus
    noded['demand_elec'] = solph.Sink(
        label='demand_elec', inputs={noded['bel']: solph.Flow(
            actual_value=data['demand_el'], fixed=True, nominal_value=1)})
    noded['demand_el_2'] = solph.Sink(
        label='demand_el_2', inputs={noded['bel2']: solph.Flow(
            actual_value=data['demand_el'], fixed=True, nominal_value=1)})

    # create simple sink object for heat demand for each thermal bus
    noded['demand_therm'] = solph.Sink(
        label='demand_therm', inputs={noded['bth']: solph.Flow(
            actual_value=data['demand_th'], fixed=True, nominal_value=741000)})
    noded['demand_therm_2'] = solph.Sink(
        label='demand_th_2', inputs={noded['bth2']: solph.Flow(
            actual_value=data['demand_th'], fixed=True, nominal_value=741000)})

    # This is just a dummy transformer with a nominal input of zero
    noded['fixed_chp_gas'] = solph.Transformer(
        label='fixed_chp_gas',
        inputs={noded['bgas']: solph.Flow(nominal_value=0)},
        outputs={noded['bel']: solph.Flow(), noded['bth']: solph.Flow()},
        conversion_factors={noded['bel']: 0.3, noded['bth']: 0.5})

    # create a fixed transformer to distribute to the heat_2 and elec_2 buses
    noded['fixed_chp_gas_2'] = solph.Transformer(
        label='fixed_chp_gas_2',
        inputs={noded['bgas']: solph.Flow(nominal_value=10e10)},
        outputs={noded['bel2']: solph.Flow(), noded['bth2']: solph.Flow()},
        conversion_factors={noded['bel2']: 0.3, noded['bth2']: 0.5})

    # create a fixed transformer to distribute to the heat and elec buses
    noded['variable_chp_gas'] = solph.components.ExtractionTurbineCHP(
        label='variable_chp_gas',
        inputs={noded['bgas']: solph.Flow(nominal_value=10e10)},
        outputs={noded['bel']: solph.Flow(), noded['bth']: solph.Flow()},
        conversion_factors={noded['bel']: 0.3, noded['bth']: 0.5},
        conversion_factor_full_condensation={noded['bel']: 0.5}
        )

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    energysystem.add(*noded.values())

    om = solph.Model(energysystem)

    if debug:
        filename = os.path.join(
            helpers.extend_basic_path('lp_files'), 'variable_chp.lp')
        logging.info('Store lp-file in {0}.'.format(filename))
        om.write(filename, io_options={'symbolic_solver_labels': True})

    logging.info('Solve the optimization problem')
    om.solve(solver=solver, solve_kwargs={'tee': tee_switch})

    optimisation_results = outputlib.processing.results(om)

#    myresults = outputlib.views.node(optimisation_results, 'natural_gas')
#    myresults = myresults['sequences'].sum(axis=0).to_dict()
#    myresults['objective'] = outputlib.processing.meta_results(om)['objective']

    return optimisation_results, om

results, om = run_variable_chp_example()
myresults = outputlib.views.node(results, 'natural_gas')
myresults = myresults['sequences'].sum(axis=0).to_dict()
myresults['objective'] = outputlib.processing.meta_results(om)['objective']

logging.info('Plot the results')

cdict = {
    (('variable_chp_gas', 'electricity'), 'flow'): '#42c77a',
    (('fixed_chp_gas_2', 'electricity_2'), 'flow'): '#20b4b6',
    (('fixed_chp_gas', 'electricity'), 'flow'): '#20b4b6',
    (('fixed_chp_gas', 'heat'), 'flow'): '#20b4b6',
    (('variable_chp_gas', 'heat'), 'flow'): '#42c77a',
    (('heat', 'demand_therm'), 'flow'): '#5b5bae',
    (('heat_2', 'demand_th_2'), 'flow'): '#5b5bae',
    (('electricity', 'demand_elec'), 'flow'): '#5b5bae',
    (('electricity_2', 'demand_el_2'), 'flow'): '#5b5bae',
    (('heat', 'excess_therm'), 'flow'): '#f22222',
    (('heat_2', 'excess_bth_2'), 'flow'): '#f22222',
    (('electricity', 'excess_elec'), 'flow'): '#f22222',
    (('electricity_2', 'excess_bel_2'), 'flow'): '#f22222',
    (('fixed_chp_gas_2', 'heat_2'), 'flow'): '#20b4b6'}

##########################################################################
# Plotting
##########################################################################

plt.rc('legend', **{'fontsize': 13})
plt.rcParams.update({'font.size': 13})

fig = plt.figure(figsize=(18, 9))
fig.subplots_adjust(left=0.07, bottom=0.12, right=0.86, top=0.93,
                    wspace=0.03, hspace=0.2)

# subplot of electricity bus (fixed chp) [1]
ax = fig.add_subplot(3, 2, 1)
electricity_2 = outputlib.views.node(results, 'electricity_2')
electricity_2 = electricity_2['sequences'].reset_index()

ix = (('fixed_chp_gas_2', 'electricity_2'), 'flow')
electricity_2[ix].plot(
    kind='bar', linewidth=0, stacked=True, width=1, ax=ax, color=cdict[ix])

ix = [(('electricity_2', 'demand_el_2'), 'flow'),
      (('electricity_2', 'excess_bel_2'), 'flow')]
electricity_2[ix].plot(
    ax=ax, linewidth=4, kind='line', drawstyle='steps-mid',
    colors=[cdict[k] for k in electricity_2[ix].columns])

ax.set_ylabel('Power in MW')
ax.set_xlabel('')
ax.get_xaxis().set_visible(False)
ax.set_title("Electricity output (fixed chp)")
ax.legend_.remove()

# subplot of electricity bus (variable chp) [2]
ax = fig.add_subplot(3, 2, 2)
electricity = outputlib.views.node(results, 'electricity')
electricity = electricity['sequences'].reset_index()

ix = (('variable_chp_gas', 'electricity'), 'flow')
electricity[ix].plot(
    kind='bar', linewidth=0, stacked=True, width=1, ax=ax, color=cdict[ix])

ix = [(('electricity', 'demand_elec'), 'flow'),
      (('electricity', 'excess_elec'), 'flow')]
electricity[ix].plot(
    ax=ax, linewidth=4, kind='line', drawstyle='steps-mid',
    colors=[cdict[k] for k in electricity[ix].columns])

ax.get_yaxis().set_visible(False)
ax.set_xlabel('')
ax.get_xaxis().set_visible(False)
ax.set_title("Electricity output (variable chp)")
ax.legend_.remove()

# subplot of heat bus (fixed chp) [3]
ax = fig.add_subplot(3, 2, 3)
heat_2 = outputlib.views.node(results, 'heat_2')
heat_2 = heat_2['sequences'].reset_index()

ix = (('fixed_chp_gas_2', 'heat_2'), 'flow')
heat_2[ix].plot(
    kind='bar', linewidth=0, stacked=True, width=1, ax=ax, color=cdict[ix])

ix = [(('heat_2', 'demand_th_2'), 'flow'),
      (('heat_2', 'excess_bth_2'), 'flow')]
heat_2[ix].plot(
    ax=ax, linewidth=4, kind='line', drawstyle='steps-mid',
    colors=[cdict[k] for k in heat_2[ix].columns])
ax.set_ylabel('Power in MW')
ax.set_ylim([0, 600000])
ax.get_xaxis().set_visible(False)
ax.set_title("Heat output (fixed chp)")
ax.legend_.remove()

# subplot of heat bus (variable chp) [4]
ax = fig.add_subplot(3, 2, 4)
heat = outputlib.views.node(results, 'heat')
heat = heat['sequences'].reset_index()

ix = (('variable_chp_gas', 'heat'), 'flow')
heat[ix].plot(
    kind='bar', linewidth=0, stacked=True, width=1, ax=ax, color=cdict[ix])

ix = [(('heat', 'demand_therm'), 'flow'),
      (('heat', 'excess_therm'), 'flow')]
heat[ix].plot(
    ax=ax, linewidth=4, kind='line', drawstyle='steps-mid',
    colors=[cdict[k] for k in heat[ix].columns])
ax.get_yaxis().set_visible(False)
ax.set_ylabel('Power in MW')
ax.set_ylim([0, 600000])
ax.get_xaxis().set_visible(False)
ax.set_title("Heat output (variable chp)")
ax.legend_.remove()

# subplot of efficiency (fixed chp) [5]
fix_chp_gas2 = outputlib.views.node(results, 'fixed_chp_gas_2')
ngas = fix_chp_gas2['sequences'][(('natural_gas', 'fixed_chp_gas_2'), 'flow')]
elec = fix_chp_gas2['sequences'][(('fixed_chp_gas_2', 'electricity_2'), 'flow')]
heat = fix_chp_gas2['sequences'][(('fixed_chp_gas_2', 'heat_2'), 'flow')]
e_ef = elec.div(ngas)
h_ef = heat.div(ngas)
df = pd.DataFrame(pd.concat([h_ef, e_ef], axis=1))
my_ax = df.plot(drawstyle='steps-mid', ax=fig.add_subplot(3, 2, 5), linewidth=2)
my_ax.set_ylabel('efficiency')
my_ax.set_ylim([0, 0.55])
my_ax.set_xlabel('Date')
my_ax.set_title('Efficiency (fixed chp)')
my_ax.legend_.remove()

# subplot of efficiency (variable chp) [6]
var_chp_gas = outputlib.views.node(results, 'variable_chp_gas')
ngas = var_chp_gas['sequences'][(('natural_gas', 'variable_chp_gas'), 'flow')]
elec = var_chp_gas['sequences'][(('variable_chp_gas', 'electricity'), 'flow')]
heat = var_chp_gas['sequences'][(('variable_chp_gas', 'heat'), 'flow')]
e_ef = elec.div(ngas)
h_ef = heat.div(ngas)
e_ef.name = 'electricity           '
h_ef.name = 'heat'
df = pd.DataFrame(pd.concat([h_ef, e_ef], axis=1))
my_ax = df.plot(drawstyle='steps-mid', ax=fig.add_subplot(3, 2, 6), linewidth=2)
my_ax.set_ylim([0, 0.55])
my_ax.get_yaxis().set_visible(False)
my_ax.set_xlabel('Date')
my_ax.set_title('Efficiency (variable chp)')
my_box = my_ax.get_position()
my_ax.set_position([my_box.x0, my_box.y0, my_box.width * 1, my_box.height])
my_ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)

plt.show()
