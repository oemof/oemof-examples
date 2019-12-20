# -*- coding: utf-8 -*-
"""
@author: witte
"""
from tespy import con, nwk, cmp, hlp, cmp_char
from matplotlib import pyplot as plt
import numpy as np
from tespy.tools import logger
import logging
mypath = logger.define_logging(
log_path=True, log_version=True, timed_rotating={'backupCount': 4},
screen_level=logging.WARNING, screen_datefmt = "no_date")

# %% calculation of thermal efficiency (for this specific process)


def thermal_efficiency(sg, cond, turb, pump):

    # carnot efficiency

    T_m_in = sg.Q.val / sg.SQ1.val
    T_m_out = cond.Q.val / cond.SQ1.val
    eta_c = 1 - (T_m_out / T_m_in)

    # irreversibility elements

    f = T_m_out / sg.Q.val
    d_eta_t = turb.Sirr.val * f
    d_eta_p = pump.Sirr.val * f

    # thermal efficiency

    eta_th = abs(turbine.P.val + pump.P.val) / sg.Q.val
    print('Thermal efficiency by definition:', round(eta_th, 4))
    print('Thermal efficiency by entropy analysis:',
          round(eta_c - (d_eta_t + d_eta_p), 4))

    # plot
    fig, ax = plt.subplots()

    x = [0, 1, 2, 3]
    eta = [eta_c, d_eta_t, d_eta_p, eta_th]
    plt.bar(x, eta, Color='#00395b', zorder=3)

    ax.set_ylabel('efficiency')
    ax.set_xticks(x)
    ax.set_xticklabels(['$\eta_c$', '$\Delta \eta_t$', '$\Delta \eta_p$',
                        '$\eta_{th}$'])
    plt.title('thermal efficiency')
    ax.grid(axis='y', zorder=0)

    rects, labels = ax.patches, [round(val, 4) for val in eta]

    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom')

    plt.show()

    fig.savefig('efficiency.svg')


# %% network


fluids = ['water']

nw = nwk.network(fluids=fluids)
nw.set_attr(p_unit='bar', T_unit='C', h_unit='kJ / kg',
            p_range=[0.01, 150], T_range=[5, 800], h_range=[10, 5000])

# %% components

# main components
turbine = cmp.turbine('turbine')
condenser = cmp.condenser('condenser')
pump = cmp.pump('pump')
steam_generator = cmp.heat_exchanger_simple('steam generator')
source = cmp.source('cycle opener')
sink = cmp.sink('cycle closer')

# cooling water
source_cw = cmp.source('cooling water inlet')
sink_cw = cmp.sink('cooling water outlet')

# %% connections

# main cycle
fs_in = con.connection(source, 'out1', turbine, 'in1')
ws = con.connection(turbine, 'out1', condenser, 'in1')
cond = con.connection(condenser, 'out1', pump, 'in1')
fw = con.connection(pump, 'out1', steam_generator, 'in1')
fs_out = con.connection(steam_generator, 'out1', sink, 'in1')
nw.add_conns(fs_in, ws, cond, fw, fs_out)

# cooling water
cw_in = con.connection(source_cw, 'out1', condenser, 'in2')
cw_out = con.connection(condenser, 'out2', sink_cw, 'in1')
nw.add_conns(cw_in, cw_out)

# %% busses

# characteristic function for generator efficiency
x = np.array([0, 0.2, 0.4, 0.6, 0.8, 1, 1.2])
y = np.array([0, 0.86, 0.9, 0.93, 0.95, 0.96, 0.95])

gen = cmp_char.characteristics(x=x, y=y)

# motor of pump has a constant efficiency
power = con.bus('total output power')
power.add_comps({'c': turbine, 'p': 'P', 'char': gen},
                {'c': pump, 'char': 1 / 0.95})
nw.add_busses(power)

# %% parametrization of components

turbine.set_attr(eta_s=0.9, design=['eta_s'], offdesign=['eta_s_char', 'cone'])
condenser.set_attr(pr1=0.5, pr2=0.98, ttd_u=5, design=['pr2', 'ttd_u'], offdesign=['zeta2', 'kA'])
pump.set_attr(eta_s=0.8, design=['eta_s'], offdesign=['eta_s_char'])
steam_generator.set_attr(pr=0.95)

# %% parametrization of connections

# offdesign calculation: use parameter design for auto deactivation
# turbine inlet pressure is deriven by stodolas law, outlet pressure by
# characteristic of condenser
fs_in.set_attr(p=100, T=500, fluid={'water': 1}, design=['p'])

# closing the cycle: fluid properties at sink must be identical to fluid
# properties at the source
fs_out.set_attr(p=con.ref(fs_in, 1, 0), h=con.ref(fs_in, 1, 0))

cw_in.set_attr(T=20, p=5, fluid={'water': 1})
cw_out.set_attr(T=30)

# total output power as input parameter
power.set_attr(P=-10e6)

# %% solving

mode = 'design'

file = 'cr'

# solve the network, print the results to prompt and save
nw.solve(mode=mode)
nw.print_results()
nw.save(file)

thermal_efficiency(steam_generator, condenser, turbine, pump)
# change to offdesign mode
mode = 'offdesign'

# reset power input
power.set_attr(P=-9e6)

# the design file holds the information on the design case
# initialisation from previously design process
nw.solve(mode=mode, design_file=file + '/results.csv',
         init_file=file + '/results.csv')
nw.print_results()
nw.save('cr_OD')

thermal_efficiency(steam_generator, condenser, turbine, pump)
