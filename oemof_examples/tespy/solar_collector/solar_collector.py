# -*- coding: utf-8 -*-
from tespy.networks import Network
from tespy.components import Sink, Source, SolarCollector
from tespy.connections import Connection
from tespy.tools import document_model

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

# %% network

fluid_list = ['H2O']
nw = Network(fluids=fluid_list, p_unit='bar', T_unit='C')

# %% components

# sinks & sources
back = Source('to collector')
feed = Sink('from collector')

# collector
coll = SolarCollector(label='solar thermal collector')

# %% connections

b_c = Connection(back, 'out1', coll, 'in1')
c_f = Connection(coll, 'out1', feed, 'in1')

nw.add_conns(b_c, c_f)

# %% component parameters

# set pressure ratio and heat flow, as well as dimensional parameters of
# the collector. E is missing, thus energy balance for radiation is not
# performed at this point
coll.set_attr(pr=0.99, Q=8e3)

# %% connection parameters

b_c.set_attr(p=5, T=35, fluid={'H2O': 1})
c_f.set_attr(p0=2, T=120)

# %% solving

# going through several parametrisation possibilities
print('###############')
print('simulation 1')
mode = 'design'
nw.solve(mode=mode)
nw.print_results()

# set absorption instead of outlet temperature
coll.set_attr(E=9e2, eta_opt=0.9, lkf_lin=1, lkf_quad=0.005, A=10, Tamb=10)
c_f.set_attr(T=np.nan)
print('###############')
print('simulation 2')

nw.solve(mode=mode)
document_model(nw)
nw.print_results()


# set outlet temperature and mass flow instead of heat flow and radiation
coll.set_attr(Q=np.nan, E=np.nan)
c_f.set_attr(T=100, m=1e-1)

print('###############')
print('design simulation')
nw.solve(mode=mode)
nw.print_results()
nw.save('design')

# looping over different ambient temperatures and levels of absorption
# (of the inclined surface) assuming constant mass flow

# set print_level to none
mode = 'offdesign'
nw.set_attr(iterinfo=False)
c_f.set_attr(T=np.nan)

gridnum = 10
T_amb = np.linspace(-10, 30, gridnum, dtype=float)
E_glob = np.linspace(100, 1000, gridnum, dtype=float)

df = pd.DataFrame(columns=T_amb)

for E in E_glob:
    eta = []
    coll.set_attr(E=E)
    for T in T_amb:
        coll.set_attr(Tamb=T)
        nw.solve(mode=mode, design_path='design')
        eta += [coll.Q.val / (coll.E.val * coll.A.val)]
        # cut out efficiencies smaller than zero
        if eta[-1] < 0:
            eta[-1] = np.nan

    df.loc[E] = eta

print('###############')
print('offdesign performance map')
E, T = np.meshgrid(T_amb, E_glob)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(E, T, df.values)
# temperature difference -> mean collector temperature to ambient temperature
ax.set_xlabel('ambient temperature t_a in °C')
# absorption on the inclined surface
ax.set_ylabel('absorption E in $\mathrm{\\frac{W}{m^2}}$')
# thermal efficiency (no optical losses)
ax.set_zlabel('efficiency $\eta$')
plt.show()
