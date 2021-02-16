# -*- coding: utf-8 -*-
from tespy.connections import Connection
from tespy.components import Source, Sink, CombustionChamberStoich
from tespy.networks import Network
from tespy.tools import document_model

# %% network

# define full fluid list for the network's variable space
fluid_list = ['myAir', 'myFuel', 'myFuel_fg']

# define unit systems and fluid property ranges
nw = Network(fluids=fluid_list, p_unit='bar', T_unit='C', p_range=[1, 10])

# %% components

# sinks & sources
amb = Source('ambient')
sf = Source('fuel')
fg = Sink('flue gas outlet')

# combustion chamber
comb = CombustionChamberStoich('stoichiometric combustion chamber')

# %% connections

amb_comb = Connection(amb, 'out1', comb, 'in1')
sf_comb = Connection(sf, 'out1', comb, 'in2')
comb_fg = Connection(comb, 'out1', fg, 'in1')

nw.add_conns(sf_comb, amb_comb, comb_fg)

# %% component parameters

# for the first calculation run
comb.set_attr(
    fuel={'CH4': 0.96, 'CO2': 0.04},
    air={'Ar': 0.0129, 'N2': 0.7553, 'CO2': 0.0004, 'O2': 0.2314},
    fuel_alias='myFuel', air_alias='myAir', lamb=3, ti=20000
)

# %% connection parameters

# air from abient (ambient pressure and temperature), air composition must be
# stated component wise.
amb_comb.set_attr(
    T=20, p=1, fluid={'myAir': 1, 'myFuel': 0, 'myFuel_fg': 0}
)

# fuel, pressure must not be stated, as pressure is the same at all inlets and
# outlets of the combustion chamber
sf_comb.set_attr(
    T=25, fluid={'myAir': 0, 'myFuel': 1, 'myFuel_fg': 0}
)

# %% solving

mode = 'design'
nw.solve(mode=mode)
nw.print_results()

comb.set_attr(path='./LUT')

mode = 'design'
nw.solve(mode=mode)
nw.print_results()
document_model(nw)
