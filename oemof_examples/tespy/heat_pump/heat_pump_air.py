#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 08:44:36 2018

@author: witte
"""

from tespy import cmp, con, nwk

import numpy as np
import pandas as pd

# %% network

nw = nwk.network(fluids=['water', 'NH3', 'air'],
                 T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

# %% components

# sources & sinks
c_in = cmp.source('coolant in')
cb = cmp.source('consumer back flow')
cf = cmp.sink('consumer feed flow')
amb = cmp.source('ambient air')
amb_out1 = cmp.sink('sink ambient 1')
amb_out2 = cmp.sink('sink ambient 2')
c_out = cmp.sink('coolant out')

# ambient air system
sp = cmp.splitter('splitter')
fan = cmp.compressor('fan')

# consumer system

cd = cmp.condenser('condenser')
dhp = cmp.pump('district heating pump')
cons = cmp.heat_exchanger_simple('consumer')

# evaporator system

ves = cmp.valve('valve')
dr = cmp.drum('drum')
ev = cmp.heat_exchanger('evaporator')
su = cmp.heat_exchanger('superheater')
erp = cmp.pump('evaporator reciculation pump')

# compressor-system

cp1 = cmp.compressor('compressor 1')
cp2 = cmp.compressor('compressor 2')
ic = cmp.heat_exchanger('intercooler')

# %% connections

# consumer system

c_in_cd = con.connection(c_in, 'out1', cd, 'in1')

cb_dhp = con.connection(cb, 'out1', dhp, 'in1')
dhp_cd = con.connection(dhp, 'out1', cd, 'in2')
cd_cons = con.connection(cd, 'out2', cons, 'in1')
cons_cf = con.connection(cons, 'out1', cf, 'in1')

nw.add_conns(c_in_cd, cb_dhp, dhp_cd, cd_cons, cons_cf)

# connection condenser - evaporator system

cd_ves = con.connection(cd, 'out1', ves, 'in1')

nw.add_conns(cd_ves)

# evaporator system

ves_dr = con.connection(ves, 'out1', dr, 'in1')
dr_erp = con.connection(dr, 'out1', erp, 'in1')
erp_ev = con.connection(erp, 'out1', ev, 'in2')
ev_dr = con.connection(ev, 'out2', dr, 'in2')
dr_su = con.connection(dr, 'out2', su, 'in2')

nw.add_conns(ves_dr, dr_erp, erp_ev, ev_dr, dr_su)

amb_fan = con.connection(amb, 'out1', fan, 'in1')
fan_sp = con.connection(fan, 'out1', sp, 'in1')
sp_su = con.connection(sp, 'out1', su, 'in1')
su_ev = con.connection(su, 'out1', ev, 'in1')
ev_amb_out = con.connection(ev, 'out1', amb_out1, 'in1')

nw.add_conns(amb_fan, fan_sp, sp_su, su_ev, ev_amb_out)

# connection evaporator system - compressor system

su_cp1 = con.connection(su, 'out2', cp1, 'in1')

nw.add_conns(su_cp1)

# compressor-system

cp1_he = con.connection(cp1, 'out1', ic, 'in1')
he_cp2 = con.connection(ic, 'out1', cp2, 'in1')
cp2_c_out = con.connection(cp2, 'out1', c_out, 'in1')

sp_ic = con.connection(sp, 'out2', ic, 'in2')
ic_out = con.connection(ic, 'out2', amb_out2, 'in1')

nw.add_conns(cp1_he, he_cp2, sp_ic, ic_out, cp2_c_out)

# %% component parametrization

# condenser system

cd.set_attr(pr1=0.99, pr2=0.99, ttd_u=5, design=['pr2', 'ttd_u'], offdesign=['zeta2', 'kA'])
dhp.set_attr(eta_s=0.8, design=['eta_s'], offdesign=['eta_s_char'])
cons.set_attr(pr=0.99, design=['pr'], offdesign=['zeta'])

# ambient air

fan.set_attr(eta_s=0.5, pr=1.005, design=['eta_s'], offdesign=['eta_s_char'])

# evaporator system

ev.set_attr(pr1=0.999, pr2=0.99, ttd_l=5,
            kA_char1='EVA_HOT', kA_char2='EVA_COLD',
            design=['pr1', 'ttd_l'], offdesign=['zeta1', 'kA'])
su.set_attr(pr1=0.999, pr2=0.99, ttd_u=2, design=['pr1', 'pr2', 'ttd_u'], offdesign=['zeta1', 'zeta2', 'kA'])
erp.set_attr(eta_s=0.8, design=['eta_s'], offdesign=['eta_s_char'])

# compressor system

cp1.set_attr(eta_s=0.8, design=['eta_s'], offdesign=['eta_s_char'])
cp2.set_attr(eta_s=0.8, pr=5, design=['eta_s'], offdesign=['eta_s_char'])
ic.set_attr(pr1=0.98, pr2=0.999, design=['pr1', 'pr2'], offdesign=['zeta1', 'zeta2', 'kA'])

# %% connection parametrization

# condenser system

c_in_cd.set_attr(fluid={'air': 0, 'NH3': 1, 'water': 0})
cb_dhp.set_attr(T=60, p=10, fluid={'air': 0, 'NH3': 0, 'water': 1})
cd_cons.set_attr(T=90)
cons_cf.set_attr(h=con.ref(cb_dhp, 1, 0), p=con.ref(cb_dhp, 1, 0))

# evaporator system cold side

erp_ev.set_attr(m=con.ref(ves_dr, 4, 0), p0=5)
su_cp1.set_attr(p0=5, h0=1700)

# evaporator system hot side

amb_fan.set_attr(T=12, p=4, fluid={'air': 1, 'NH3': 0, 'water': 0},
                 offdesign=['v'])
sp_su.set_attr(offdesign=['v'])
ev_amb_out.set_attr(T=9, design=['T'])

# compressor-system

he_cp2.set_attr(T=40, p0=10, design=['T'])
ic_out.set_attr(T=30, design=['T'])
cp2_c_out.set_attr(p=con.ref(c_in_cd, 1, 0), h=con.ref(c_in_cd, 1, 0))

# %% key paramter

cons.set_attr(Q=-200e3)

# %% Calculation

nw.solve('design')
nw.print_results()
nw.save('heat_pump_air')

T_range = [6, 9, 12, 15, 18, 21, 24]
Q_range = np.array([120e3, 140e3, 160e3, 180e3, 200e3, 220e3])
df = pd.DataFrame(columns=Q_range / -cons.Q.val)

for T in T_range:
    amb_fan.set_attr(T=T)
    eps = []

    for Q in Q_range:
        cons.set_attr(Q=-Q)
        try:
            nw.solve('offdesign',
                     init_path='OD_air_' + str(Q/1e3),
                     design_path='heat_pump_air')
        except:
            nw.solve('offdesign', init_path='heat_pump_air',
                     design_path='heat_pump_air')

        if nw.lin_dep:
            eps += [np.nan]

        else:
            nw.save('OD_air_' + str(Q/1e3))
            eps += [abs(cd.Q.val) / (cp1.P.val + cp2.P.val + erp.P.val +
                    fan.P.val)]

    df.loc[T] = eps

df.to_csv('COP_air.csv')
