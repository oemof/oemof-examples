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

v0.3.x
++++++

* **oemof-core**: Example for the usage of the oemof core

v0.2.x
++++++

* **basic_example**: Introduction to the basic usage of oemof.solph

  - basic optimisation with different solvers
  - initiate the logger
  - use the lp-file for debugging
  - show/hide output of the solver
  - store and process results

* **excel-reader (replacement for csv-reader)** Shows how to define the input data in a customisable excel-file (libreoffice etc.)

* **flexible_modelling**: Shows how to add an individual constraint to the oemof solph Model.
* **generic_chp**: Illustrates how the custom component `GenericCHP` can be used...

  * bpt: \.\.\. to model a back pressure turbine.

  * ccet: \.\.\. to model a combined cycle extraction turbine.

  * mchp: \.\.\. to model a motoric chp.

* **sdewes_paper_2017**: Examples from the SDEWES conference paper.

  * economic_dispatch

  * micro_grid_design_optimisation

  * unit_commitment_district_heating

* **sector_coupling**: Jupyter notebook giving a simple example of how to couple the sectors power, heat and mobility.
* **simple_dispatch**: Shows how to set up a dispatch model.
* **storage_investment**: Variation of parameters for a storage capacity optimization.
* **variable_chp**: Presents how a variable combined heat and power plant (chp) works in contrast to a fixed chp.


v0.1.x
++++++

* **csv_reader**:

  * dispatch: Dispatch optimisation using oemof's csv-reader.

  * investment: Investment optimisation using oemof's csv-reader.

* **flexible_modelling**: Shows how to add an individual constraint to the oemof solph Model.
* **sector_coupling**: Jupyter notebook giving a simple example of how to couple the sectors power, heat and mobility.
* **simple_dispatch**: Shows how to set up a dispatch model.
* **storage_invest**: Jupyter notebook of storage capacity optimization.
* **storage_investment**: Example of storage capacity optimization.
* **variable_chp**: Presents how a variable combined heat and power plant (chp) works in contrast to a fixed chp.


oemof.tabular
-------------

Coming soon


tespy
-----

Coming soon


windpowerlib
------------

v0.1.x
++++++

* **ModelChain example**: A simple way to calculate the power output of wind turbines.


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
