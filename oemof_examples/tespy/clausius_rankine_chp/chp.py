# -*- coding: utf-8 -*-
from tespy.networks import Network
from tespy.components import (
    Sink, Source, Valve, Turbine, Splitter, Merge, Condenser, Pump,
    HeatExchangerSimple, CycleCloser
)
from tespy.connections import Connection, Bus, Ref
from tespy.tools import CharLine
from tespy.tools import document_model

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# %% network

fluids = ['water']

nw = Network(fluids=fluids, p_unit='bar', T_unit='C', h_unit='kJ / kg', iterinfo=False)

# %% components

# turbine part
valve_turb = Valve('turbine inlet valve')
turbine_hp = Turbine('high pressure turbine')
split = Splitter('extraction splitter')
turbine_lp = Turbine('low pressure turbine')

# condenser and preheater
cond = Condenser('condenser')
preheater = Condenser('preheater')
merge_ws = Merge('waste steam merge')
valve_pre = Valve('preheater valve')

# feed water
pump = Pump('pump')
steam_generator = HeatExchangerSimple('steam generator')

closer = CycleCloser('cycle closer')

# source and sink for cooling water
source_cw = Source('source_cw')
sink_cw = Sink('sink_cw')

# %% connections

# turbine part
fs_in = Connection(closer, 'out1', valve_turb, 'in1')
fs = Connection(valve_turb, 'out1', turbine_hp, 'in1')
ext = Connection(turbine_hp, 'out1', split, 'in1')
ext_v = Connection(split, 'out1', preheater, 'in1')
ext_turb = Connection(split, 'out2', turbine_lp, 'in1')
nw.add_conns(fs_in, fs, ext, ext_v, ext_turb)

# preheater and condenser
ext_cond = Connection(preheater, 'out1', valve_pre, 'in1')
cond_ws = Connection(valve_pre, 'out1', merge_ws, 'in2')
turb_ws = Connection(turbine_lp, 'out1', merge_ws, 'in1')
ws = Connection(merge_ws, 'out1', cond, 'in1')
nw.add_conns(ext_cond, cond_ws, turb_ws, ws)

# feed water
con = Connection(cond, 'out1', pump, 'in1')
fw_c = Connection(pump, 'out1', preheater, 'in2')
fw_w = Connection(preheater, 'out2', steam_generator, 'in1')
fs_out = Connection(steam_generator, 'out1', closer, 'in1')
nw.add_conns(con, fw_c, fw_w, fs_out)

# cooling water
cw_in = Connection(source_cw, 'out1', cond, 'in2')
cw_out = Connection(cond, 'out2', sink_cw, 'in1')
nw.add_conns(cw_in, cw_out)

# %% busses

x = np.array([0, 0.2, 0.4, 0.6, 0.8, 1, 1.2])
y = np.array([0.5, 0.87, 0.91, 0.94, 0.96, 0.97, 0.96])

char = CharLine(x, y)
# power bus
power_bus = Bus('power')
power_bus.add_comps(
    {'comp': turbine_hp, 'char': char, 'base': 'component'},
    {'comp': turbine_lp, 'char': char, 'base': 'component'},
    {'comp': pump, 'char': char, 'base': 'bus'})

# heating bus
heat_bus = Bus('heat')
heat_bus.add_comps({'comp': cond, 'char': -1})

nw.add_busses(power_bus, heat_bus)

# %% parametrization of components

turbine_hp.set_attr(eta_s=0.9, design=['eta_s'],
                    offdesign=['eta_s_char', 'cone'])
turbine_lp.set_attr(eta_s=0.9, design=['eta_s'],
                    offdesign=['eta_s_char', 'cone'])

cond.set_attr(pr1=1, pr2=0.99, ttd_u=12, design=['pr2', 'ttd_u'],
              offdesign=['zeta2', 'kA_char'])
preheater.set_attr(pr1=1, pr2=0.99, ttd_u=5,
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
power_bus.set_attr(P=-5e6)
#
cw_out.set_attr(T=110)


# %% solving

path = 'chp'
nw.solve('design')
nw.save(path)
nw.print_results()
document_model(nw, filename='report_design.tex')

power_bus.set_attr(P=None)
m_design = fs_in.m.val
fs_in.set_attr(m=m_design)

nw.solve('offdesign', design_path='chp')
# offdesign test and documentation
document_model(nw, filename='report_offdesign.tex')

# representation of part loads
m_range = np.linspace(0.6, 1.05, 10)[::-1]
# temperatures for the heating system
T_range = [120, 110, 100, 90, 80, 70]

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
        P += [-power_bus.P.val]

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
    plt.plot(df_Q.loc[T], df_P.loc[T], 'x', color=colors[i],
             label='$T_{VL}$ = ' + str(T) + ' °C', markersize=7,
             linewidth=2)
    i += 1

ax.set_ylabel('$P$ in MW')
ax.set_xlabel(r'$\dot{Q}$ in MW')
plt.title('P-Q diagram for CHP with backpressure steam turbine')
plt.legend(loc='lower left')
ax.set_ylim([0, 7e6])
ax.set_xlim([0, 14e6])
plt.yticks(np.arange(0, 7e6, step=1e6), np.arange(0, 7, step=1))
plt.xticks(np.arange(0, 14e6, step=2e6), np.arange(0, 14, step=2))

fig.savefig('PQ_diagram.svg')
