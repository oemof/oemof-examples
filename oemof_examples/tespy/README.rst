Within this repository you will find the source code of various examples for
`TESPy-applications <http://tespy.readthedocs.org>`_.

.. contents::
    :depth: 1
    :local:
    :backlinks: top

Usage
=====

Download the example you want to check out or the whole repository and you are
ready to start. In your python3 environment with `TESPy installed 
<http://tespy.readthedocs.io/en/master/installation.html>`_ run the python
code, no additional package installation should be required.


Contributing
============

You are very welcome to add your own examples, improve the documentation or fix
bugs, typos etc.. Just create a pull request or send us an e-mail
(see `here <https://oemof.org/contact/>`_ for contact information).
If you want to add your own example please provide a short description and
required packages to run the example.

Examples
========
    
* clausius_rankine: Basic example of the clausius rankine process.
* clausius_rankine_chp: A simple backpressure turbine.

    * backpressure-line at different loads and
    * varying feed flow temperature levels.
    
* combined_cycle_chp: Combined cycle power plant with backpressure steam turbine.    
* combustion: Examples on how to work with combustion in TESPy.

    * combustion_champer: using all fluid components individually
    * combustion_chamber_stoich: using fluid aliases (flue gas is mixture of
      fresh air and stoichiometric flue gas)
      
    * combustion_engine: Motoric CHP.
    
* custom_variables: Example on how to calculate the diameter of a pipe at a given pressure ratio.

* district_heating: A small district heating systems with about 150 components.
    
    * modeling of pressure drop and
    * energy loss at different ambient temperature levels.

* heat_pump: An air to water and a water to water heat pump for power-to-heat applications.

    * COP for varying loads,
    * varying ambient temperature levels and
    * air vs. water as heat source.

* solar_collector: An example to show, how the solar collector component can be
  implemented.
