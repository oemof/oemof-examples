This repository holds a collections of various examples on how to build an energy system with `oemof <http://oemof.readthedocs.org>`_.

Examples are provided for each major oemof release specified by the directory they are in. 

.. contents::
    :depth: 3
    :local:
    :backlinks: top

Installation
================

Download the repository using the green download button. 

You need a working python3 environment to be able to run the examples. For more details see `'Installation and setup' <http://oemof.readthedocs.io/en/latest/installation_and_setup.html>`_ section of the oemof documentation.
Required packages to run each example are listed in the respective example header.


Contributing
================

Everybody is welcome to contribute by adding their own example, fix documentation, bugs and typos in existing examples, etc via a `pull request <https://github.com/oemof/examples/pulls>`_ or by sending us an e-mail (see `here <https://oemof.org/contact/>`_ for contact information).
If you want to add your own example please provide a short description and required packages to run the example.

Examples
=========

oemof.solph (oemof)
-------------------

Examples of the latest release, some examples may not exist for older versions.

* **activity_costs**:

* **basic_example**:
     Introduction to the basic usage of oemof.solph

  - basic optimisation with different solvers
  - initiate the logger
  - use the lp-file for debugging
  - show/hide output of the solver
  - store and process results

* **electrical**: Linear Optimised Power Flow

  - lopf
  - transshipment

* **emission_constraint**: Shows how to add an additional constraint to limit
  the overall emissions.

* **excel-reader** Shows how to define the input data in a customisable excel-file (libreoffice etc.)

* **flexible_modelling**: Shows how to add an individual constraint to the oemof solph Model.

* **generic_chp**: Illustrates how the custom component `GenericCHP` can be used...

  * bpt: \.\.\. to model a back pressure turbine.

  * ccet: \.\.\. to model a combined cycle extraction turbine.

  * mchp: \.\.\. to model a motoric chp.

* **installation test**: Test your oemof installation and the connected solvers

* **invest_non_convex**: This example illustrates a possible combination of
  solph.Investment and solph.NonConvex. Note that both options are added to
  different components of the energy system.

* Basic Notebooks

  - 1_Simple_dispatch_store_results.ipynb
  - 2_Processing_results_and_plotting.ipynb

* **min_max_runtimes**: Example that illustrates how to model min and
  max runtimes.

* **plotting_examples**: The examples shows how to use oemof_visio with solph
  results.

* **flow_schedule (notebook)**:

* **simple_dispatch**: Shows how to set up a dispatch model.

* **start_and_shutdown_costs**: Example that illustrates how to model startup
  and shutdown costs attributed to a binary flow.

* **Balanced and unbalanced storage**

* **storage_investment**: Variation of parameters for a storage capacity optimization.

  - v1_invest_optimize_all_technologies
  - v2_invest_optimize_only_gas_and_storage
  - v3_invest_optimize_only_storage_with_fossil_share
  - v4_invest_optimize_all_technologies_with_fossil_share

* **variable_chp**: Presents how a variable combined heat and power plant (chp) works in contrast to a fixed chp.


oemof.tabular
-------------

Coming soon


tespy
-----
    
* **clausius_rankine**: Basic example of the clausius rankine process.
* **clausius_rankine_chp**: Backpressure turbine in district heating.    
* **combined_cycle_chp**: Combined cycle power plant with backpressure steam turbine.    
* **combustion**: Examples on how to work with combustion in TESPy.
* **custom_variables**: Example on how to calculate the diameter of a pipe at a given pressure ratio.
* **district_heating**: A small district heating systems with about 150 components.
* **heat_pump**: An air to water and a water to water heat pump for power-to-heat applications.
* **solar_collector**: An example to show, how the solar collector component can be implemented.

windpowerlib
------------

v0.1.x
++++++

* **ModelChain example**: A simple way to calculate the power output of wind turbines.

v0.2.x
++++++

* `ModelChain example <https://github.com/oemof/oemof-examples/blob/master/oemof_examples/windpowerlib/v0.2.x/modelchain_example.py>`_: A simple way to calculate the power output of wind turbines.
* `Turbine cluster ModelChain example <https://github.com/oemof/oemof-examples/blob/master/oemof_examples/windpowerlib/v0.2.x/turbine_cluster_modelchain_example.py>`_: A simple and fast way to calculate
  windturbine cluster and farms.


License
=======

Copyright (C) 2017 oemof developing group

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.
