# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:38:43 2019

@author: Malte Fritz
"""

from tespy.networks import network
from tespy.components import sink, source, combustion_chamber
from tespy.connections import connection

# %% network

# define full fluid list for the network's variable space
fluid_list = ['Ar', 'N2', 'O2', 'CO2', 'CH4', 'H2O']

# define unit systems and fluid property ranges
nw = network(fluids=fluid_list, p_unit='bar', T_unit='C',
             p_range=[0.5, 10], T_range=[10, 1200])

# %% components

# sinks & sources
amb = source('ambient')
sf = source('fuel')
fg = sink('flue gas outlet')

# combustion chamber
comb=combustion_chamber(label='combustion chamber')

# %% connections

amb_comb = connection(amb, 'out1', comb, 'in1')
sf_comb = connection(sf, 'out1', comb, 'in2')
comb_fg = connection(comb, 'out1', fg, 'in1')

nw.add_conns(sf_comb, amb_comb, comb_fg)

# %% component parameters

# set combustion chamber air to stoichometric air ratio and thermal input
comb.set_attr(lamb=3, ti=2e6)

# %% connection parameters

# air from abient (ambient pressure and temperature), air composition must be
# stated component wise.
amb_comb.set_attr(p=1, T=20, fluid={'Ar': 0.0129, 'N2': 0.7553, 'H2O': 0,
                                    'CH4': 0, 'CO2': 0.0004, 'O2': 0.2314})

# fuel, pressure must not be stated, as pressure is the same at all inlets and
# outlets of the combustion chamber
sf_comb.set_attr(T=25, fluid={'CO2': 0.04, 'Ar': 0, 'N2': 0, 'O2': 0, 'H2O': 0,
                              'CH4': 0.96})

# %% solving

nw.solve('design')
nw.print_results()