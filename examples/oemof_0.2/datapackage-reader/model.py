# -*- coding: utf-8 -*-
"""
General description
-------------------
This example shows how to create an oemof energysystem from a datapackage by
using the oemof datapackge reader.

Data
----
Data is provided in the datapackage directory:

data/elements/
   demands.csv',
   volatile-generators.csv
   combined-heat-and-power-plants.csv
   header.csv
   dispatchable-generators.csv
   storages.csv
   transshipment.csv

data/geometries/
   components.csv
   hubs.csv

data/sequences/
   demand-profiles.csv
   solar-profiles.csv
   wind-profiles.csv


Installation requirements
-------------------------
This example requires the latest version of oemof. Install
by:

    pip install 'oemof<0.3,>=0.2'

14.02.2018 - simon.hilpert@rl-institut.de
"""

from oemof.energy_system import EnergySystem


es = EnergySystem.from_datapackage('datapackage/datapackage.json')
