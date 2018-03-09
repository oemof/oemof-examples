# -*- coding: utf-8 -*-
"""
General description
-------------------
As the csv-reader was removed with version 0.2 this example shows how to create
an excel-reader. The example is equivalent to the old csv-reader example.
Following the example one can customise the excel reader to ones own needs.

The pandas package supports the '.xls' and the '.xlsx' format but one can create
read and adept the files with open source software such as libreoffice,
openoffice, gnumeric,...

Data
----
scenario.xlsx

Installation requirements
-------------------------
This example requires the latest version of oemof, matplotlib and xlrd. Install
by:

    pip install 'oemof<0.3,>=0.2'
    pip install xlrd
    pip install matplotlib

5.1.2018 - uwe.krien@rl-institut.de
"""

import os
import logging
import pandas as pd

from oemof.tools import logger
from oemof import solph
from oemof import outputlib
from matplotlib import pyplot as plt


def nodes_from_excel(filename):
    xls = pd.ExcelFile(filename)
    buses = xls.parse('buses')
    commodity_sources = xls.parse('commodity_sources')
    transformers = xls.parse('transformers')
    renewables = xls.parse('renewables')
    demand = xls.parse('demand')
    storages = xls.parse('storages')
    powerlines = xls.parse('powerlines')
    timeseries = xls.parse('time_series')

    # Create Bus objects from buses table
    noded = {}
    for i, b in buses.iterrows():
        noded[b['label']] = solph.Bus(label=b['label'])
        if b['excess']:
            label = b['label'] + '_excess'
            noded[label] = solph.Sink(label=label, inputs={
                noded[b['label']]: solph.Flow()})
        if b['shortage']:
            label = b['label'] + '_shortage'
            noded[label] = solph.Source(label=label, outputs={
                noded[b['label']]: solph.Flow(
                    variable_costs=b['shortage costs'])})

    # Create Source objects from table 'commodity sources'
    for i, cs in commodity_sources.iterrows():
        noded[i] = solph.Source(label=i, outputs={noded[cs['to']]: solph.Flow(
            variable_costs=cs['variable costs'])})

    # Create Source objects with fixed time series from 'renewables' table
    for i, re in renewables.iterrows():
        noded[i] = solph.Source(label=i, outputs={noded[re['to']]: solph.Flow(
            actual_value=timeseries[i], nominal_value=re['capacity'],
            fixed=True)})

    # Create Sink objects with fixed time series from 'demand' table
    for i, re in demand.iterrows():
        noded[i] = solph.Sink(label=i, inputs={noded[re['from']]: solph.Flow(
            actual_value=timeseries[i], nominal_value=re['maximum'],
            fixed=True)})

    # Create Transformer objects from 'transformers' table
    for i, t in transformers.iterrows():
        noded[i] = solph.Transformer(
            label=i,
            inputs={noded[t['from']]: solph.Flow()},
            outputs={noded[t['to']]: solph.Flow(
                nominal_value=t['capacity'],
                variable_costs=t['variable costs'],
                max=t['simultaneity'])},
            conversion_factors={noded[t['to']]: t['efficiency']})

    for i, s in storages.iterrows():
        noded[i] = solph.components.GenericStorage(
            label=i,
            inputs={noded[s['bus']]: solph.Flow(
                nominal_value=s['capacity pump'], max=s['max'])},
            outputs={noded[s['bus']]: solph.Flow(
                nominal_value=s['capacity turbine'], max=s['max'])},
            nominal_capacity=s['capacity storage'],
            capacity_loss=s['capacity loss'],
            initial_capacity=s['initial capacity'],
            capacity_max=s['cmax'], capacity_min=s['cmin'],
            inflow_conversion_factor=s['efficiency pump'],
            outflow_conversion_factor=s['efficiency turbine'])

    for i, p in powerlines.iterrows():
        label = 'powerline_' + p['bus_1'] + '_' + p['bus_2']
        noded[label] = solph.Transformer(
            label=label,
            inputs={noded[p['bus_1']]: solph.Flow()},
            outputs={noded[p['bus_2']]: solph.Flow(
                nominal_value=p['capacity'])},
            conversion_factors={noded[p['bus_2']]: p['efficiency']})
        label = 'powerline_' + p['bus_2'] + '_' + p['bus_1']
        noded[label] = solph.Transformer(
            label=label,
            inputs={noded[p['bus_2']]: solph.Flow()},
            outputs={noded[p['bus_1']]: solph.Flow(
                nominal_value=p['capacity'])},
            conversion_factors={noded[p['bus_1']]: p['efficiency']})
    return noded


logger.define_logging()
datetime_index = pd.date_range(
    '2030-01-01 00:00:00', '2030-01-14 23:00:00', freq='60min')

# model creation and solving
logging.info('Starting optimization')

# initialisation of the energy system
es = solph.EnergySystem(timeindex=datetime_index)

# adding all nodes and flows to the energy system
# (data taken from excel-file)
nodes = nodes_from_excel(
    os.path.join(os.path.dirname(__file__), 'scenarios.xlsx',))

es.add(*nodes.values())

print("********************************************************")
print("The following objects has been created from excel sheet:")
for n in es.nodes:
    oobj = str(type(n)).replace("<class 'oemof.solph.", "").replace("'>", "")
    print(oobj + ':', n.label)
print("********************************************************")

# creation of a least cost model from the energy system
om = solph.Model(es)
om.receive_duals()

# solving the linear problem using the given solver
om.solve(solver='cbc')

results = outputlib.processing.results(om)

region2 = outputlib.views.node(results, 'R2_bus_el')
region1 = outputlib.views.node(results, 'R1_bus_el')

print(region2['sequences'].sum())
print(region1['sequences'].sum())

ax = plt.figure().add_subplot(1,1,1)
region1['sequences'].plot(ax=ax).legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
logging.info("Done!")
