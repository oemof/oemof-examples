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

from oemof.tools import logger
import oemof.solph as solph
from oemof import outputlib
try:
    from oemof.outputlib import plot as oemof_plot
except ImportError as e:
    print("\n\nYou have to use the branch 'features/plotting_module' to run"
          " this example\n\n")
    oemof_plot = None
    raise e


def shape_legend(node, reverse=False, **kwargs):
    handels = kwargs['handles']
    labels = kwargs['labels']
    axes = kwargs['ax']
    parameter = {}

    new_labels = []
    for label in labels:
        label = label.replace('(', '')
        label = label.replace('), flow)', '')
        label = label.replace(node, '')
        label = label.replace(',', '')
        label = label.replace(' ', '')
        new_labels.append(label)
    labels = new_labels

    parameter['bbox_to_anchor'] = kwargs.get('bbox_to_anchor', (1, 0.5))
    parameter['loc'] = kwargs.get('loc', 'center left')
    parameter['ncol'] = kwargs.get('ncol', 1)
    plotshare = kwargs.get('plotshare', 0.9)

    if reverse:
        handels = handels.reverse()
        labels = labels.reverse()

    box = axes.get_position()
    axes.set_position([box.x0, box.y0, box.width * plotshare, box.height])

    parameter['handles'] = handels
    parameter['labels'] = labels
    axes.legend(**parameter)
    return axes


# Parameter
solver = 'cbc'
smooth_plot = True

# logger.define_logging(text="Starting chp example", screen_level=logging.DEBUG)
logger.define_logging()
logging.info('Initialize the energy system')

# create time index for 192 hours in May.
date_time_index = pd.date_range('5/5/2012', periods=192, freq='H')
energysystem = solph.EnergySystem(timeindex=date_time_index)

# Read data file with heat and electrical demand (192 hours)
full_filename = os.path.join(os.path.dirname(__file__), 'variable_chp.csv')
data = pd.read_csv(full_filename, sep=",")

##########################################################################
# Create oemof.solph objects
##########################################################################

logging.info('Create oemof.solph objects')

# create natural gas bus
bgas = solph.Bus(label="natural_gas")

# create commodity object for gas resource
solph.Source(label='rgas', outputs={bgas: solph.Flow(variable_costs=50)})

# create two electricity buses and two heat buses
bel = solph.Bus(label="electricity")
bel2 = solph.Bus(label="electricity_2")
bth = solph.Bus(label="heat")
bth2 = solph.Bus(label="heat_2")

# create excess components for the elec/heat bus to allow overproduction
solph.Sink(label='excess_bth_2', inputs={bth2: solph.Flow()})
solph.Sink(label='excess_therm', inputs={bth: solph.Flow()})
solph.Sink(label='excess_bel_2', inputs={bel2: solph.Flow()})
solph.Sink(label='excess_elec', inputs={bel: solph.Flow()})

# create simple sink object for electrical demand for each electrical bus
solph.Sink(label='demand_elec', inputs={bel: solph.Flow(
    actual_value=data['demand_el'], fixed=True, nominal_value=1)})
solph.Sink(label='demand_el_2', inputs={bel2: solph.Flow(
    actual_value=data['demand_el'], fixed=True, nominal_value=1)})

# create simple sink object for heat demand for each thermal bus
solph.Sink(label='demand_therm', inputs={bth: solph.Flow(
    actual_value=data['demand_th'], fixed=True, nominal_value=741000)})
solph.Sink(label='demand_th_2', inputs={bth2: solph.Flow(
    actual_value=data['demand_th'], fixed=True, nominal_value=741000)})

# This is just a dummy transformer with a nominal input of zero
solph.Transformer(
    label='fixed_chp_gas',
    inputs={bgas: solph.Flow(nominal_value=0)},
    outputs={bel: solph.Flow(), bth: solph.Flow()},
    conversion_factors={bel: 0.3, bth: 0.5})

# create a fixed transformer to distribute to the heat_2 and elec_2 buses
solph.Transformer(
    label='fixed_chp_gas_2',
    inputs={bgas: solph.Flow(nominal_value=10e10)},
    outputs={bel2: solph.Flow(), bth2: solph.Flow()},
    conversion_factors={bel2: 0.3, bth2: 0.5})

# create a fixed transformer to distribute to the heat and elec buses
solph.components.ExtractionTurbineCHP(
    label='variable_chp_gas',
    inputs={bgas: solph.Flow(nominal_value=10e10)},
    outputs={bel: solph.Flow(), bth: solph.Flow()},
    conversion_factors={bel: 0.3, bth: 0.5},
    conversion_factor_full_condensation={bel: 0.5}
    )

##########################################################################
# Optimise the energy system and plot the results
##########################################################################

logging.info('Optimise the energy system')

om = solph.Model(energysystem)

logging.info('Solve the optimization problem')
om.solve(solver=solver, solve_kwargs={'tee': False})

results = outputlib.processing.results(om)

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
fig = plt.figure(figsize=(18, 9))
plt.rc('legend', **{'fontsize': 13})
plt.rcParams.update({'font.size': 13})
fig.subplots_adjust(left=0.07, bottom=0.12, right=0.86, top=0.93,
                    wspace=0.03, hspace=0.2)

# subplot of electricity bus (fixed chp) [1]
electricity_2 = outputlib.views.node(results, 'electricity_2')
myplot = oemof_plot.io_plot(
    bus_label='electricity_2', df=electricity_2['sequences'],
    cdict=cdict, smooth=smooth_plot,
    line_kwa={'linewidth': 4}, ax=fig.add_subplot(3, 2, 1),
    inorder=[(('fixed_chp_gas_2', 'electricity_2'), 'flow')],
    outorder=[(('electricity_2', 'demand_el_2'), 'flow'),
              (('electricity_2', 'excess_bel_2'), 'flow')])
myplot['ax'].set_ylabel('Power in MW')
myplot['ax'].set_xlabel('')
myplot['ax'].get_xaxis().set_visible(False)
myplot['ax'].set_title("Electricity output (fixed chp)")
myplot['ax'].legend_.remove()

# subplot of electricity bus (variable chp) [2]
electricity = outputlib.views.node(results, 'electricity')
myplot = oemof_plot.io_plot(
    bus_label='electricity', df=electricity['sequences'],
    cdict=cdict, smooth=smooth_plot,
    line_kwa={'linewidth': 4}, ax=fig.add_subplot(3, 2, 2),
    inorder=[(('fixed_chp_gas', 'electricity'), 'flow'),
             (('variable_chp_gas', 'electricity'), 'flow')],
    outorder=[(('electricity', 'demand_elec'), 'flow'),
              (('electricity', 'excess_elec'), 'flow')])
myplot['ax'].get_yaxis().set_visible(False)
myplot['ax'].set_xlabel('')
myplot['ax'].get_xaxis().set_visible(False)
myplot['ax'].set_title("Electricity output (variable chp)")
shape_legend('electricity', plotshare=1, **myplot)

# subplot of heat bus (fixed chp) [3]
heat_2 = outputlib.views.node(results, 'heat_2')
myplot = oemof_plot.io_plot(
    bus_label='heat_2', df=heat_2['sequences'],
    cdict=cdict, smooth=smooth_plot,
    line_kwa={'linewidth': 4}, ax=fig.add_subplot(3, 2, 3),
    inorder=[(('fixed_chp_gas_2', 'heat_2'), 'flow')],
    outorder=[(('heat_2', 'demand_th_2'), 'flow'),
              (('heat_2', 'excess_bth_2'), 'flow')])
myplot['ax'].set_ylabel('Power in MW')
myplot['ax'].set_ylim([0, 600000])
myplot['ax'].get_xaxis().set_visible(False)
myplot['ax'].set_title("Heat output (fixed chp)")
myplot['ax'].legend_.remove()

# subplot of heat bus (variable chp) [4]
heat = outputlib.views.node(results, 'heat')
myplot = oemof_plot.io_plot(
    bus_label='heat', df=heat['sequences'],
    cdict=cdict, smooth=smooth_plot,
    line_kwa={'linewidth': 4}, ax=fig.add_subplot(3, 2, 4),
    inorder=[(('fixed_chp_gas', 'heat'), 'flow'),
             (('variable_chp_gas', 'heat'), 'flow')],
    outorder=[(('heat', 'demand_therm'), 'flow'),
              (('heat', 'excess_therm'), 'flow')])
myplot['ax'].set_ylim([0, 600000])
myplot['ax'].get_yaxis().set_visible(False)
myplot['ax'].get_xaxis().set_visible(False)
myplot['ax'].set_title("Heat output (variable chp)")
shape_legend('heat', plotshare=1, **myplot)

if smooth_plot:
    style = None
else:
    style = 'steps-mid'

# subplot of efficiency (fixed chp) [5]
fix_chp_gas2 = outputlib.views.node(results, 'fixed_chp_gas_2')
ngas = fix_chp_gas2['sequences'][(('natural_gas', 'fixed_chp_gas_2'), 'flow')]
elec = fix_chp_gas2['sequences'][(('fixed_chp_gas_2', 'electricity_2'), 'flow')]
heat = fix_chp_gas2['sequences'][(('fixed_chp_gas_2', 'heat_2'), 'flow')]
e_ef = elec.div(ngas)
h_ef = heat.div(ngas)
df = pd.DataFrame(pd.concat([h_ef, e_ef], axis=1))
my_ax = df.plot(drawstyle=style, ax=fig.add_subplot(3, 2, 5), linewidth=2)
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
my_ax = df.plot(drawstyle=style, ax=fig.add_subplot(3, 2, 6), linewidth=2)
my_ax.set_ylim([0, 0.55])
my_ax.get_yaxis().set_visible(False)
my_ax.set_xlabel('Date')
my_ax.set_title('Efficiency (variable chp)')
my_box = my_ax.get_position()
my_ax.set_position([my_box.x0, my_box.y0, my_box.width * 1, my_box.height])
my_ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)

plt.show()
