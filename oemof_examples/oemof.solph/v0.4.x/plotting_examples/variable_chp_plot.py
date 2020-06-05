# -*- coding: utf-8 -*-

"""
General description
-------------------
This example shows a complex 6 tiles plot using the i/o-plot function of the
oemof-visio package. This examples focuses on the plotting function and not on
the general oemof functions.


Data
----
variable_chp.csv


Installation requirements
-------------------------
This example requires the version v0.3.x of oemof. Install by:

    pip install 'oemof.solph>=0.4,<0.5'

The oemof-visio provides the base for the created i/o plot.

    pip install git+https://github.com/oemof/oemof_visio.git

5.1.2017 - uwe.krien@rl-institut.de
"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

import logging
import os
import pandas as pd
import matplotlib.pyplot as plt

from oemof.network.network import Node
from oemof.tools import logger
from oemof import solph

import oemof_visio as oev


def shape_legend(node, reverse=True, **kwargs):
    handels = kwargs["handles"]
    labels = kwargs["labels"]
    axes = kwargs["ax"]
    parameter = {}

    new_labels = []
    for label in labels:
        label = label.replace("(", "")
        label = label.replace("), flow)", "")
        label = label.replace(node, "")
        label = label.replace(",", "")
        label = label.replace(" ", "")
        new_labels.append(label)
    labels = new_labels

    parameter["bbox_to_anchor"] = kwargs.get("bbox_to_anchor", (1, 0.5))
    parameter["loc"] = kwargs.get("loc", "center left")
    parameter["ncol"] = kwargs.get("ncol", 1)
    plotshare = kwargs.get("plotshare", 0.9)

    if reverse:
        handels.reverse()
        labels.reverse()

    box = axes.get_position()
    axes.set_position([box.x0, box.y0, box.width * plotshare, box.height])

    parameter["handles"] = handels
    parameter["labels"] = labels
    axes.legend(**parameter)
    return axes


logger.define_logging()
logging.info("Initialize the energy system")
date_time_index = pd.date_range("5/5/2012", periods=192, freq="H")
energysystem = solph.EnergySystem(timeindex=date_time_index)
Node.registry = energysystem

full_filename = os.path.join(os.getcwd(), "variable_chp.csv")
data = pd.read_csv(full_filename, sep=",")

logging.info("Create oemof.solph objects")

bgas = solph.Bus(label="natural_gas")
solph.Source(label="rgas", outputs={bgas: solph.Flow(variable_costs=50)})

bel = solph.Bus(label="electricity")
bel2 = solph.Bus(label="electricity_2")
bth = solph.Bus(label="heat")
bth2 = solph.Bus(label="heat_2")

solph.Sink(label="excess_bth_2", inputs={bth2: solph.Flow()})
solph.Sink(label="excess_therm", inputs={bth: solph.Flow()})
solph.Sink(label="excess_bel_2", inputs={bel2: solph.Flow()})
solph.Sink(label="excess_elec", inputs={bel: solph.Flow()})

solph.Sink(
    label="demand_elec",
    inputs={bel: solph.Flow(fix=data["demand_el"], nominal_value=1)},
)
solph.Sink(
    label="demand_el_2",
    inputs={bel2: solph.Flow(fix=data["demand_el"], nominal_value=1)},
)

solph.Sink(
    label="demand_therm",
    inputs={bth: solph.Flow(fix=data["demand_th"], nominal_value=741000)},
)
solph.Sink(
    label="demand_th_2",
    inputs={bth2: solph.Flow(fix=data["demand_th"], nominal_value=741000)},
)

# This is just a dummy transformer with a nominal input of zero (for the plot)
solph.Transformer(
    label="fixed_chp_gas",
    inputs={bgas: solph.Flow(nominal_value=0)},
    outputs={bel: solph.Flow(), bth: solph.Flow()},
    conversion_factors={bel: 0.3, bth: 0.5},
)

solph.Transformer(
    label="fixed_chp_gas_2",
    inputs={bgas: solph.Flow(nominal_value=10e10)},
    outputs={bel2: solph.Flow(), bth2: solph.Flow()},
    conversion_factors={bel2: 0.3, bth2: 0.5},
)

solph.components.ExtractionTurbineCHP(
    label="variable_chp_gas",
    inputs={bgas: solph.Flow(nominal_value=10e10)},
    outputs={bel: solph.Flow(), bth: solph.Flow()},
    conversion_factors={bel: 0.3, bth: 0.5},
    conversion_factor_full_condensation={bel: 0.5},
)

logging.info("Optimise the energy system")
om = solph.Model(energysystem)
logging.info("Solve the optimization problem")
om.solve(solver="cbc", solve_kwargs={"tee": False})

results = solph.processing.results(om)

##########################################################################
# Plotting
##########################################################################

logging.info("Plot the results")
smooth_plot = True

cdict = {
    (("variable_chp_gas", "electricity"), "flow"): "#42c77a",
    (("fixed_chp_gas_2", "electricity_2"), "flow"): "#20b4b6",
    (("fixed_chp_gas", "electricity"), "flow"): "#20b4b6",
    (("fixed_chp_gas", "heat"), "flow"): "#20b4b6",
    (("variable_chp_gas", "heat"), "flow"): "#42c77a",
    (("heat", "demand_therm"), "flow"): "#5b5bae",
    (("heat_2", "demand_th_2"), "flow"): "#5b5bae",
    (("electricity", "demand_elec"), "flow"): "#5b5bae",
    (("electricity_2", "demand_el_2"), "flow"): "#5b5bae",
    (("heat", "excess_therm"), "flow"): "#f22222",
    (("heat_2", "excess_bth_2"), "flow"): "#f22222",
    (("electricity", "excess_elec"), "flow"): "#f22222",
    (("electricity_2", "excess_bel_2"), "flow"): "#f22222",
    (("fixed_chp_gas_2", "heat_2"), "flow"): "#20b4b6",
}

fig = plt.figure(figsize=(18, 9))
plt.rc("legend", **{"fontsize": 13})
plt.rcParams.update({"font.size": 13})
fig.subplots_adjust(
    left=0.07, bottom=0.12, right=0.86, top=0.93, wspace=0.03, hspace=0.2
)

# subplot of electricity bus (fixed chp) [1]
electricity_2 = solph.views.node(results, "electricity_2")
x_length = len(electricity_2["sequences"].index)
myplot = oev.plot.io_plot(
    bus_label="electricity_2",
    df=electricity_2["sequences"],
    cdict=cdict,
    smooth=smooth_plot,
    line_kwa={"linewidth": 4},
    ax=fig.add_subplot(3, 2, 1),
    inorder=[(("fixed_chp_gas_2", "electricity_2"), "flow")],
    outorder=[
        (("electricity_2", "demand_el_2"), "flow"),
        (("electricity_2", "excess_bel_2"), "flow"),
    ],
)
myplot["ax"].set_ylabel("Power in MW")
myplot["ax"].set_xlabel("")
myplot["ax"].get_xaxis().set_visible(False)
myplot["ax"].set_xlim(0, x_length)
myplot["ax"].set_title("Electricity output (fixed chp)")
myplot["ax"].legend_.remove()

# subplot of electricity bus (variable chp) [2]
electricity = solph.views.node(results, "electricity")
myplot = oev.plot.io_plot(
    bus_label="electricity",
    df=electricity["sequences"],
    cdict=cdict,
    smooth=smooth_plot,
    line_kwa={"linewidth": 4},
    ax=fig.add_subplot(3, 2, 2),
    inorder=[
        (("fixed_chp_gas", "electricity"), "flow"),
        (("variable_chp_gas", "electricity"), "flow"),
    ],
    outorder=[
        (("electricity", "demand_elec"), "flow"),
        (("electricity", "excess_elec"), "flow"),
    ],
)
myplot["ax"].get_yaxis().set_visible(False)
myplot["ax"].set_xlabel("")
myplot["ax"].get_xaxis().set_visible(False)
myplot["ax"].set_title("Electricity output (variable chp)")
myplot["ax"].set_xlim(0, x_length)
shape_legend("electricity", plotshare=1, **myplot)

# subplot of heat bus (fixed chp) [3]
heat_2 = solph.views.node(results, "heat_2")
myplot = oev.plot.io_plot(
    bus_label="heat_2",
    df=heat_2["sequences"],
    cdict=cdict,
    smooth=smooth_plot,
    line_kwa={"linewidth": 4},
    ax=fig.add_subplot(3, 2, 3),
    inorder=[(("fixed_chp_gas_2", "heat_2"), "flow")],
    outorder=[
        (("heat_2", "demand_th_2"), "flow"),
        (("heat_2", "excess_bth_2"), "flow"),
    ],
)
myplot["ax"].set_ylabel("Power in MW")
myplot["ax"].set_ylim([0, 600000])
myplot["ax"].get_xaxis().set_visible(False)
myplot["ax"].set_title("Heat output (fixed chp)")
myplot["ax"].set_xlim(0, x_length)
myplot["ax"].legend_.remove()

# subplot of heat bus (variable chp) [4]
heat = solph.views.node(results, "heat")
myplot = oev.plot.io_plot(
    bus_label="heat",
    df=heat["sequences"],
    cdict=cdict,
    smooth=smooth_plot,
    line_kwa={"linewidth": 4},
    ax=fig.add_subplot(3, 2, 4),
    inorder=[
        (("fixed_chp_gas", "heat"), "flow"),
        (("variable_chp_gas", "heat"), "flow"),
    ],
    outorder=[
        (("heat", "demand_therm"), "flow"),
        (("heat", "excess_therm"), "flow"),
    ],
)
myplot["ax"].set_ylim([0, 600000])
myplot["ax"].get_yaxis().set_visible(False)
myplot["ax"].get_xaxis().set_visible(False)
myplot["ax"].set_title("Heat output (variable chp)")
myplot["ax"].set_xlim(0, x_length)
shape_legend("heat", plotshare=1, **myplot)

if smooth_plot:
    style = None
else:
    style = "steps-mid"

# subplot of efficiency (fixed chp) [5]
fix_chp_gas2 = solph.views.node(results, "fixed_chp_gas_2")
ngas = fix_chp_gas2["sequences"][(("natural_gas", "fixed_chp_gas_2"), "flow")]
elec = fix_chp_gas2["sequences"][
    (("fixed_chp_gas_2", "electricity_2"), "flow")
]
heat = fix_chp_gas2["sequences"][(("fixed_chp_gas_2", "heat_2"), "flow")]
e_ef = elec.div(ngas)
h_ef = heat.div(ngas)
df = pd.DataFrame(pd.concat([h_ef, e_ef], axis=1))
my_ax = df.reset_index(drop=True).plot(
    drawstyle=style, ax=fig.add_subplot(3, 2, 5), linewidth=2
)
my_ax.set_ylabel("efficiency")
my_ax.set_ylim([0, 0.55])
my_ax.set_xlabel("May 2012")
my_ax = oev.plot.set_datetime_ticks(
    my_ax, df.index, tick_distance=24, date_format="%d", offset=12, tight=True
)
my_ax.set_title("Efficiency (fixed chp)")
my_ax.legend_.remove()

# subplot of efficiency (variable chp) [6]
var_chp_gas = solph.views.node(results, "variable_chp_gas")
ngas = var_chp_gas["sequences"][(("natural_gas", "variable_chp_gas"), "flow")]
elec = var_chp_gas["sequences"][(("variable_chp_gas", "electricity"), "flow")]
heat = var_chp_gas["sequences"][(("variable_chp_gas", "heat"), "flow")]
e_ef = elec.div(ngas)
h_ef = heat.div(ngas)
e_ef.name = "electricity           "
h_ef.name = "heat"
df = pd.DataFrame(pd.concat([h_ef, e_ef], axis=1))
my_ax = df.reset_index(drop=True).plot(
    drawstyle=style, ax=fig.add_subplot(3, 2, 6), linewidth=2
)
my_ax.set_ylim([0, 0.55])
my_ax = oev.plot.set_datetime_ticks(
    my_ax, df.index, tick_distance=24, date_format="%d", offset=12, tight=True
)
my_ax.get_yaxis().set_visible(False)
my_ax.set_xlabel("May 2012")

my_ax.set_title("Efficiency (variable chp)")
my_box = my_ax.get_position()
my_ax.set_position([my_box.x0, my_box.y0, my_box.width * 1, my_box.height])
my_ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), ncol=1)

plt.show()
