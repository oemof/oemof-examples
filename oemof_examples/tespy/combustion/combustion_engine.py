# -*- coding: utf-8 -*-
from tespy.networks import Network
from tespy.components import Sink, Source, Splitter, Merge, CombustionEngine
from tespy.connections import Connection
from tespy.tools import document_model

import numpy as np

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
cw_in1 = Source('cooling water inlet1')
cw_in2 = Source('cooling water inlet2')
cw_out1 = Sink('cooling water outlet1')
cw_out2 = Sink('cooling water outlet2')
split = Splitter('splitter')
merge = Merge('merge')

# combustion chamber
chp = CombustionEngine(label='combustion engine')

# %% connections

amb_comb = Connection(amb, 'out1', chp, 'in3')
sf_comb = Connection(sf, 'out1', chp, 'in4')
comb_fg = Connection(chp, 'out3', fg, 'in1')

nw.add_conns(sf_comb, amb_comb, comb_fg)

cw1_chp1 = Connection(cw_in1, 'out1', chp, 'in1')
cw2_chp2 = Connection(cw_in2, 'out1', chp, 'in2')

nw.add_conns(cw1_chp1, cw2_chp2)

chp1_cw = Connection(chp, 'out1', cw_out1, 'in1')
chp2_cw = Connection(chp, 'out2', cw_out2, 'in1')

nw.add_conns(chp1_cw, chp2_cw)

# %% component parameters

# set combustion chamber fuel, air to stoichometric air ratio and thermal input
chp.set_attr(pr1=0.99, pr2=0.99, P=-10e6, lamb=1.2)


# %% connection parameters

# air from abient (ambient pressure and temperature), air composition must be
# stated component wise.
amb_comb.set_attr(
    p=5, T=30,
    fluid={
        'Ar': 0.0129, 'N2': 0.7553, 'H2O': 0, 'CH4': 0, 'CO2': 0.0004,
        'O2': 0.2314
    }
)

# fuel, pressure must not be stated, as pressure is the same at all inlets and
# outlets of the combustion chamber
sf_comb.set_attr(
    T=30, fluid={'CO2': 0, 'Ar': 0, 'N2': 0, 'O2': 0, 'H2O': 0, 'CH4': 1}
)

comb_fg.set_attr()

cw1_chp1.set_attr(
    p=3, T=60, m=50,
    fluid={'CO2': 0, 'Ar': 0, 'N2': 0, 'O2': 0, 'H2O': 1, 'CH4': 0}
)

cw2_chp2.set_attr(
    p=3, T=80, m=50,
    fluid={'CO2': 0, 'Ar': 0, 'N2': 0, 'O2': 0, 'H2O': 1, 'CH4': 0}
)

# %% solving

mode = 'design'
nw.set_attr(iterinfo=False)
nw.solve(mode=mode)
nw.save('chp')

chp.P.design = chp.P.val
load = chp.P.val / chp.P.design
power = chp.P.val
heat = chp.Q1.val + chp.Q2.val
ti = chp.ti.val
print('Load: ' + '{:.3f}'.format(load))
print('Power generation: ' + '{:.3f}'.format(abs(chp.P.val / chp.ti.val)))
print(
    'Heat generation: ' +
    '{:.3f}'.format(abs((chp.Q1.val + chp.Q2.val) / chp.ti.val)))
print(
    'Fuel utilization: ' +
    '{:.3f}'.format(abs((chp.P.val + chp.Q1.val + chp.Q2.val) / chp.ti.val)))


mode = 'offdesign'
for P in np.linspace(1, 0.4, 5) * chp.P.design:
    chp.set_attr(P=P)
    nw.solve(mode=mode, design_path='chp')

    load = chp.P.val/chp.P.design
    print('Load: ' + '{:.3f}'.format(load))
    print('Power generation: ' + '{:.3f}'.format(abs(chp.P.val / chp.ti.val)))
    print(
        'Heat generation: ' +
        '{:.3f}'.format(abs((chp.Q1.val + chp.Q2.val) / chp.ti.val)))
    print(
        'Fuel utilization: ' +
        '{:.3f}'.format(abs((chp.P.val + chp.Q1.val + chp.Q2.val) / chp.ti.val)))

document_model(nw)
