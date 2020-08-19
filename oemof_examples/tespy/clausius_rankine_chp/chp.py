# -*- coding: utf-8 -*-
from tespy.networks import network
from tespy.components import (
    sink, source, valve, turbine, splitter, merge, condenser, pump,
    heat_exchanger_simple, cycle_closer
)
from tespy.connections import connection, bus, ref

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# %% network

fluids = ['water']

nw = network(fluids=fluids, p_unit='bar', T_unit='C', h_unit='kJ / kg')

# %% components

# turbine part
valve_turb = valve('turbine inlet valve')
turbine_hp = turbine('high pressure turbine')
split = splitter('extraction splitter')
turbine_lp = turbine('low pressure turbine')

# condenser and preheater
cond = condenser('condenser')
preheater = condenser('preheater')
merge_ws = merge('waste steam merge')
valve_pre = valve('preheater valve')

# feed water
pump = pump('pump')
steam_generator = heat_exchanger_simple('steam generator')

closer = cycle_closer('cycle closer')

# source and sink for cooling water
source_cw = source('source_cw')
sink_cw = sink('sink_cw')

# %% connections

# turbine part
fs_in = connection(closer, 'out1', valve_turb, 'in1')
fs = connection(valve_turb, 'out1', turbine_hp, 'in1')
ext = connection(turbine_hp, 'out1', split, 'in1')
ext_v = connection(split, 'out1', preheater, 'in1')
ext_turb = connection(split, 'out2', turbine_lp, 'in1')
nw.add_conns(fs_in, fs, ext, ext_v, ext_turb)

# preheater and condenser
ext_cond = connection(preheater, 'out1', valve_pre, 'in1')
cond_ws = connection(valve_pre, 'out1', merge_ws, 'in2')
turb_ws = connection(turbine_lp, 'out1', merge_ws, 'in1')
ws = connection(merge_ws, 'out1', cond, 'in1')
nw.add_conns(ext_cond, cond_ws, turb_ws, ws)

# feed water
con = connection(cond, 'out1', pump, 'in1')
fw_c = connection(pump, 'out1', preheater, 'in2')
fw_w = connection(preheater, 'out2', steam_generator, 'in1')
fs_out = connection(steam_generator, 'out1', closer, 'in1')
nw.add_conns(con, fw_c, fw_w, fs_out)

# cooling water
cw_in = connection(source_cw, 'out1', cond, 'in2')
cw_out = connection(cond, 'out2', sink_cw, 'in1')
nw.add_conns(cw_in, cw_out)

# %% busses

# power bus
power_bus = bus('power')
power_bus.add_comps({'comp': turbine_hp, 'char': -1},
                    {'comp': turbine_lp, 'char': -1},
                    {'comp': pump, 'char': -1})

# heating bus
heat_bus = bus('heat')
heat_bus.add_comps({'comp': cond, 'char': -1})

nw.add_busses(power_bus, heat_bus)

# %% parametrization of components

turbine_hp.set_attr(eta_s=0.9, design=['eta_s'],
                    offdesign=['eta_s_char', 'cone'])
turbine_lp.set_attr(eta_s=0.9, design=['eta_s'],
                    offdesign=['eta_s_char', 'cone'])

cond.set_attr(pr1=0.99, pr2=0.99, ttd_u=12, design=['pr2', 'ttd_u'],
              offdesign=['zeta2', 'kA_char'])
preheater.set_attr(pr1=0.99, pr2=0.99, ttd_u=5,
                   design=['pr2', 'ttd_u', 'ttd_l'],
                   offdesign=['zeta2', 'kA_char'])

pump.set_attr(eta_s=0.8, design=['eta_s'], offdesign=['eta_s_char'])
steam_generator.set_attr(pr=0.95)

# %% parametrization of connections

# fresh steam properties
fs_in.set_attr(p=110, T=550, fluid={'water': 1})

# pressure after turbine inlet valve
fs.set_attr(p=100, design=['p'])

# pressure extraction steam
ext.set_attr(p=10, design=['p'])

# staring value for warm feed water
fw_w.set_attr(h0=310)

# cooling water inlet
cw_in.set_attr(T=60, p=10, fluid={'water': 1})

# setting key parameters:
# Power of the plant
power_bus.set_attr(P=5e6)
#
cw_out.set_attr(T=110)


# %% solving

path = 'chp'
nw.solve('design')
nw.save(path)
nw.print_results()

power_bus.set_attr(P=np.nan)
m_design = fs_in.m.val_SI

# representation of part loads
m_range = [1.05, 1, 0.9, 0.8, 0.7, 0.6]

# temperatures for the heating system
T_range = [120, 110, 100, 95, 90, 85, 80, 75, 70]

df_P = pd.DataFrame(columns=m_range)
df_Q = pd.DataFrame(columns=m_range)

# iterate over temperatures
for T in T_range:
    cw_out.set_attr(T=T)
    Q = []
    P = []
    # iterate over mass flow
    for m in m_range:
        print('case: T='+str(T)+', load='+str(m))
        fs_in.set_attr(m=m*m_design)

        # use an initialisation file with parameters similar to next
        # calculation
        if m == m_range[0]:
            nw.solve('offdesign', init_path=path, design_path=path)
        else:
            nw.solve('offdesign', design_path=path)

        Q += [heat_bus.P.val]
        P += [power_bus.P.val]

    df_Q.loc[T] = Q
    df_P.loc[T] = P

df_P.to_csv('power.csv')
df_Q.to_csv('heat.csv')
# plotting
df_P = pd.read_csv('power.csv', index_col=0)
df_Q = pd.read_csv('heat.csv', index_col=0)

colors = ['#00395b', '#74adc1', '#b54036', '#ec6707',
          '#bfbfbf', '#999999', '#010101']

fig, ax = plt.subplots()

i = 0
for T in T_range:
    if T % 10 == 0:
        plt.plot(df_Q.loc[T], df_P.loc[T], '-x', Color=colors[i],
                 label='$T_{VL}$ = ' + str(T) + ' °C', markersize=7,
                 linewidth=2)
        i += 1

ax.set_ylabel('$P$ in MW')
ax.set_xlabel('$\dot{Q}$ in MW')
plt.title('P-Q diagram for CHP with backpressure steam turbine')
plt.legend(loc='lower left')
ax.set_ylim([0, 7e6])
ax.set_xlim([0, 14e6])
plt.yticks(np.arange(0, 7e6, step=1e6), np.arange(0, 7, step=1))
plt.xticks(np.arange(0, 14e6, step=2e6), np.arange(0, 14, step=2))

fig.savefig('PQ_diagram.svg')
