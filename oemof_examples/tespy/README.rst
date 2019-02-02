Within this repository you will find the source code of various examples for `TESPy-applications <http://tespy.readthedocs.org>`_.

.. contents::
    :depth: 1
    :local:
    :backlinks: top

Usage
=====

Download the example you want to check out or the whole repository and you are ready to start. In your python3 environment with `TESPy installed <http://tespy.readthedocs.io/en/master/installation.html>`_ run the python code, no additional package installation should be required.


Contributing
============

You are very welcome to add your own examples, improve the documentation or fix bugs, typos etc.. Just create a pull request or send us an e-mail (see `here <https://oemof.org/contact/>`_ for contact information).
If you want to add your own example please provide a short description and required packages to run the example.

Examples
========
	
* basic: Clausius rankine process as very basic example.
* btes_system: heat extraction from underground heat storage using btes.		
* ccbp: Combined cycle power plant with backpressure steam turbine.
* chp: A simple backpressure turbine chp.

	* backpressure-line at different loads and
	* varying feed flow temperature levels.
	
* cogeneration_unit: Motoric CHP.
	
* combustion_chamber: Examples on how to work with combustion chambers in TESPy

	* combustion_champer.py: using all fluid components individually
	* combustion_chamber_stoich.py: using fluid aliases (flue gas is mixture of fresh air and stoichiometric flue gas)
	
* custom_variables: Example on how to use the custom variables feature for TESPy

	* works with the features/custom_vars branch only at the moment

* district_heating: A small district heating systems with about 150 components.
	
	* modeling of pressure drop and
	* energy loss at different ambient temperature levels.

* heat_pump: A air/water to water heat pump for power-to-heat applications.

	* COP for varying loads,
	* varying ambient temperature levels and
	* air vs. water as heat source.

* solar_collector: An example to show, how the solar collector component can be implemented.
