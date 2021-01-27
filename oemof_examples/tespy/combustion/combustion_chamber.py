# -*- coding: utf-8 -*-
from tespy.connections import Connection
from tespy.components import Source, Sink, CombustionChamber
from tespy.networks import Network
from tespy.tools import document_model

# %% network

# define full fluid list for the network's variable space
fluid_list = ['Ar', 'N2', 'O2', 'CO2', 'CH4', 'H2O']

# define unit systems and fluid property ranges
nw = Network(fluids=fluid_list, p_unit='bar', T_unit='C', p_range=[0.5, 10])

# %% components

# sinks & sources
amb = Source('ambient')
sf = Source('fuel')
fg = Sink('flue gas outlet')

# combustion chamber
comb = CombustionChamber(label='combustion chamber')

# %% connections

amb_comb = Connection(amb, 'out1', comb, 'in1')
sf_comb = Connection(sf, 'out1', comb, 'in2')
comb_fg = Connection(comb, 'out1', fg, 'in1')

nw.add_conns(sf_comb, amb_comb, comb_fg)

# %% component parameters

# set combustion chamber air to stoichometric air ratio and thermal input
comb.set_attr(lamb=3, ti=2e6)

# %% connection parameters

# air from abient (ambient pressure and temperature), air composition must be
# stated component wise.
amb_comb.set_attr(
    p=1, T=20,
    fluid={
        'Ar': 0.0129, 'N2': 0.7553, 'H2O': 0, 'CH4': 0, 'CO2': 0.0004,
        'O2': 0.2314
    }
)

# fuel, pressure must not be stated, as pressure is the same at all inlets and
# outlets of the combustion chamber
sf_comb.set_attr(
    T=25,
    fluid={'CO2': 0.04, 'Ar': 0, 'N2': 0, 'O2': 0, 'H2O': 0, 'CH4': 0.96}
)

# %% solving

nw.solve('design')
nw.print_results()
document_model(nw)
