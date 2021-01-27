# -*- coding: utf-8 -*-

from tespy.networks import Network
from tespy.components import (Sink, Source, Turbine, Condenser,
                              Pump, HeatExchangerSimple, CycleCloser)
from tespy.connections import Connection, Bus, Ref
from tespy.tools.characteristics import CharLine
from tespy.tools import document_model
import numpy as np

# %% network

fluids = ['water']

nw = Network(fluids=fluids)
nw.set_attr(
    p_unit='bar', T_unit='C', h_unit='kJ / kg',
    p_range=[0.01, 150], h_range=[10, 5000])

# %% components

# main components
turb = Turbine('turbine')
con = Condenser('condenser')
pu = Pump('pump')
steam_generator = HeatExchangerSimple('steam generator')
closer = CycleCloser('cycle closer')

# cooling water
so_cw = Source('cooling water inlet')
si_cw = Sink('cooling water outlet')

# %% connections

# main cycle
fs_in = Connection(closer, 'out1', turb, 'in1')
ws = Connection(turb, 'out1', con, 'in1')
cond = Connection(con, 'out1', pu, 'in1')
fw = Connection(pu, 'out1', steam_generator, 'in1')
fs_out = Connection(steam_generator, 'out1', closer, 'in1')
nw.add_conns(fs_in, ws, cond, fw, fs_out)

# cooling water
cw_in = Connection(so_cw, 'out1', con, 'in2')
cw_out = Connection(con, 'out2', si_cw, 'in1')
nw.add_conns(cw_in, cw_out)

# %% busses

# characteristic function for generator efficiency
x = np.array([0, 0.2, 0.4, 0.6, 0.8, 1, 1.2])
y = np.array([0, 0.86, 0.9, 0.93, 0.95, 0.96, 0.95])

char = CharLine(x=x, y=y)

# motor of pump has a constant efficiency
power = Bus('total output power')
power.add_comps(
    {'comp': turb, 'char': char},
    {'comp': pu, 'char': char, 'base': 'bus'})
nw.add_busses(power)

# %% parametrization of components

turb.set_attr(eta_s=0.9, design=['eta_s'], offdesign=['eta_s_char', 'cone'])
con.set_attr(pr1=1, pr2=0.98, ttd_u=5, design=['pr2', 'ttd_u'],
             offdesign=['zeta2', 'kA_char'])
pu.set_attr(eta_s=0.8, design=['eta_s'], offdesign=['eta_s_char'])
steam_generator.set_attr(pr=0.95)

# %% parametrization of connections

# offdesign calculation: use parameter design for auto deactivation
# turbine inlet pressure is deriven by stodolas law, outlet pressure by
# characteristic of condenser
fs_in.set_attr(p=100, T=500, fluid={'water': 1}, design=['p'])

cw_in.set_attr(T=20, p=5, fluid={'water': 1})
cw_out.set_attr(T=30)

# total output power as input parameter
power.set_attr(P=-10e6)

# %% solving

# solve the network, print the results to prompt and save
nw.solve('design')
nw.print_results()
nw.save('design')
document_model(nw, filename='report_design.tex')

# reset power input
power.set_attr(P=-9e6)

# the design file holds the information on the design case
# initialisation from previously design process
nw.solve('offdesign', design_path='design')
nw.print_results()

document_model(nw, filename='report_offdesign.tex')
