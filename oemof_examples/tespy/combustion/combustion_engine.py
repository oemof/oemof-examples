# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 10:37:36 2017

@author: witte
"""

from tespy import con, cmp, nwk
import numpy as np

# %% network

# define full fluid list for the network's variable space
fluid_list = ['Ar', 'N2', 'O2', 'CO2', 'CH4', 'H2O']
# define unit systems and fluid property ranges
nw = nwk.network(fluids=fluid_list, p_unit='bar', T_unit='C',
                 p_range=[0.5, 10], T_range=[10, 1200])

# %% components

# sinks & sources
amb = cmp.source('ambient')
sf = cmp.source('fuel')
fg = cmp.sink('flue gas outlet')
cw_in1 = cmp.source('cooling water inlet1')
cw_in2 = cmp.source('cooling water inlet2')
cw_out1 = cmp.sink('cooling water outlet1')
cw_out2 = cmp.sink('cooling water outlet2')
split = cmp.splitter('splitter')
merge = cmp.merge('merge')

# combustion chamber
chp = cmp.cogeneration_unit(label='cogeneration unit')

# %% connections

amb_comb = con.connection(amb, 'out1', chp, 'in3')
sf_comb = con.connection(sf, 'out1', chp, 'in4')
comb_fg = con.connection(chp, 'out3', fg, 'in1')

nw.add_conns(sf_comb, amb_comb, comb_fg)

cw1_chp1 = con.connection(cw_in1, 'out1', chp, 'in1')
cw2_chp2 = con.connection(cw_in2, 'out1', chp, 'in2')

nw.add_conns(cw1_chp1, cw2_chp2)

chp1_cw = con.connection(chp, 'out1', cw_out1, 'in1')
chp2_cw = con.connection(chp, 'out2', cw_out2, 'in1')

nw.add_conns(chp1_cw, chp2_cw)

# %% component parameters

# set combustion chamber fuel, air to stoichometric air ratio and thermal input
chp.set_attr(fuel='CH4', pr1=0.99, pr2=0.99, P=10e6, lamb=1.2)

# %% connection parameters

# air from abient (ambient pressure and temperature), air composition must be
# stated component wise.
amb_comb.set_attr(p=5, T=30,
                  fluid={'Ar': 0.0129, 'N2': 0.7553, 'H2O': 0,
                         'CH4': 0, 'CO2': 0.0004, 'O2': 0.2314})

# fuel, pressure must not be stated, as pressure is the same at all inlets and
# outlets of the combustion chamber
sf_comb.set_attr(T=30,
                 fluid={'CO2': 0, 'Ar': 0, 'N2': 0,
                        'O2': 0, 'H2O': 0, 'CH4': 1})

comb_fg.set_attr()

cw1_chp1.set_attr(p=3, T=60, m=50, fluid={'CO2': 0, 'Ar': 0, 'N2': 0,
                                    'O2': 0, 'H2O': 1, 'CH4': 0})

cw2_chp2.set_attr(p=3, T=80, m=50, fluid={'CO2': 0, 'Ar': 0, 'N2': 0,
                                    'O2': 0, 'H2O': 1, 'CH4': 0})

# %% solving

mode = 'design'
nw.set_printoptions(print_level='none')
nw.solve(mode=mode)
nw.save('cog')

chp.P.design = chp.P.val
load = chp.P.val / chp.P.design
power = chp.P.val
heat = chp.Q1.val + chp.Q2.val
ti = chp.ti.val
print('Load: ' + str(round(load, 3)))
print('Power generation: ' + str(round(chp.P.val / chp.ti.val, 3)))
print('Heat generation: ' + str(round((chp.Q1.val + chp.Q2.val) / chp.ti.val, 3)))
print('Fuel utilization: ' + str(round((chp.P.val + chp.Q1.val + chp.Q2.val) / chp.ti.val, 3)))


mode = 'offdesign'
for P in np.linspace(0.6, 1.0, 5) * 1e7:
    chp.set_attr(P=P)
    nw.solve(mode=mode, design_path='cog')

    load = chp.P.val/chp.P.design
    print('Load: ' + str(round(load, 3)))
    print('Power generation: ' + str(round(chp.P.val / chp.ti.val, 3)))
    print('Heat generation: ' + str(round((chp.Q1.val + chp.Q2.val) / chp.ti.val, 3)))
    print('Fuel utilization: ' + str(round((chp.P.val + chp.Q1.val + chp.Q2.val) / chp.ti.val, 3)))


