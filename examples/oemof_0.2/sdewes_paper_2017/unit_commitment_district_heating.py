# -*- coding: utf-8 -*-
"""
General description:
---------------------
Example from the SDEWES conference paper:

Simon Hilpert, Cord Kaldemeyer, Uwe Krien, Stephan Günther (2017).
'Solph - An Open Multi Purpose Optimisation Library for Flexible
         Energy System Analysis'. Paper presented at SDEWES Conference,
         Dubrovnik.

Installation requirements:
---------------------------
This example requires the latest version of oemof. Install by:

    pip install oemof

"""
import os
import pandas as pd

from oemof.network import Node
from oemof.outputlib.graph_tools import graph
from oemof.outputlib import processing, views
from oemof.solph import (EnergySystem, Bus, Source, Sink, Flow, NonConvex,
                         Model, Transformer, components)

timeindex = pd.date_range('1/1/2017', periods=168, freq='H')

energysystem = EnergySystem(timeindex=timeindex)
Node.registry = energysystem
##########################################################################
# data
##########################################################################
# Read data file
full_filename = os.path.join(os.path.dirname(__file__),
                             "timeseries.csv")
timeseries = pd.read_csv(full_filename, sep=",")

##########################################################################
# Create oemof objects
##########################################################################

bel = Bus(label="bel")

bgas = Bus(label="bgas")

bth = Bus(label="bth")

Source(label="gas",
       outputs={bgas: Flow(variable_costs=35)})

Transformer(label='boiler',
            inputs={
                bgas: Flow()},
            outputs={
                bth: Flow(nominal_value=500,
                          variable_cost=50,
                          binary=NonConvex())},
            conversion_factors={bth: 0.9})

Transformer(label='chp',
            inputs={
                bgas: Flow()},
            outputs={
                bel: Flow(nominal_value=300, min=0.5,
                          nonconvex=NonConvex()),
                bth: Flow()},
            conversion_factors={bth: 0.3, bel: 0.45})


Sink(label='demand_th',
     inputs={
         bth: Flow(actual_value=timeseries['demand_th'],
                   fixed=True, nominal_value=500)})

Sink(label='spot_el',
     inputs={
         bel: Flow(variable_costs=timeseries['price_el'])})


components.GenericStorage(
    label='storage_th',
    inputs={
        bth: Flow()},
    outputs={
        bth: Flow()},
    nominal_capacity=1500,
    capacity_loss=0.00,
    initial_capacity=0.5,
    nominal_input_capacity_ratio=1/6,
    nominal_output_capacity_ratio=1/6)

##########################################################################
# Create model and solve
##########################################################################

m = Model(energysystem)
# om.write(filename, io_options={'symbolic_solver_labels': True})

m.solve(solver='cbc', solve_kwargs={'tee': True})

results = processing.results(m)

views.node(results, 'bth')['sequences'][1:168].plot(drawstyle='steps')

graph = graph(energysystem, m, plot=True)
