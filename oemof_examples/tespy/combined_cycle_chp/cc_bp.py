# -*- coding: utf-8 -*-
from tespy.networks import network
from tespy.components import (
<<<<<<< Updated upstream
    sink, source, compressor, turbine, condenser, combustion_chamber, pump,
    heat_exchanger, drum, cycle_closer)
from tespy.connections import connection, bus, ref
=======
    Sink, Source, Compressor, Turbine, Condenser, CombustionChamber, Pump,
    HeatExchanger, Drum, CycleCloser)
from tespy.connections import Connection, Bus, Ref
from tespy.tools import document_model
from tespy.tools import CharLine
import numpy as np
>>>>>>> Stashed changes

# %% network
fluid_list = ['Ar', 'N2', 'O2', 'CO2', 'CH4', 'H2O']

nw = network(fluids=fluid_list, p_unit='bar', T_unit='C', h_unit='kJ / kg')

# %% components
# gas turbine part
comp = compressor('compressor')
c_c = combustion_chamber('combustion')
g_turb = turbine('gas turbine')

CH4 = source('fuel source')
air = source('ambient air')

# waste heat recovery
suph = heat_exchanger('superheater')
evap = heat_exchanger('evaporator')
dr = drum('drum')
eco = heat_exchanger('economizer')
dh_whr = heat_exchanger('waste heat recovery')
ch = sink('chimney')

# steam turbine part
turb = turbine('steam turbine')
cond = condenser('condenser')
pu = pump('feed water pump')
cc = cycle_closer('ls cycle closer')

# district heating
dh_in = source('district heating backflow')
dh_out = sink('district heating feedflow')

# %% connections
# gas turbine part
c_in = connection(air, 'out1', comp, 'in1')
c_out = connection(comp, 'out1', c_c, 'in1')
fuel = connection(CH4, 'out1', c_c, 'in2')
gt_in = connection(c_c, 'out1', g_turb, 'in1')
gt_out = connection(g_turb, 'out1', suph, 'in1')

nw.add_conns(c_in, c_out, fuel, gt_in, gt_out)

# waste heat recovery (flue gas side)
suph_evap = connection(suph, 'out1', evap, 'in1')
evap_eco = connection(evap, 'out1', eco, 'in1')
eco_dh = connection(eco, 'out1', dh_whr, 'in1')
dh_ch = connection(dh_whr, 'out1', ch, 'in1')

nw.add_conns(suph_evap, evap_eco, eco_dh, dh_ch)

# waste heat recovery (water side)
eco_drum = connection(eco, 'out2', dr, 'in1')
drum_evap = connection(dr, 'out1', evap, 'in2')
evap_drum = connection(evap, 'out2', dr, 'in2')
drum_suph = connection(dr, 'out2', suph, 'in2')

nw.add_conns(eco_drum, drum_evap, evap_drum, drum_suph)

# steam turbine
suph_ls = connection(suph, 'out2', cc, 'in1')
ls = connection(cc, 'out1', turb, 'in1')
ws = connection(turb, 'out1', cond, 'in1')
c_p = connection(cond, 'out1', pu, 'in1')
fw = connection(pu, 'out1', eco, 'in2')

nw.add_conns(suph_ls, ls, ws, c_p, fw)

# district heating
dh_c = connection(dh_in, 'out1', cond, 'in2')
dh_i = connection(cond, 'out2', dh_whr, 'in2')
dh_w = connection(dh_whr, 'out2', dh_out, 'in1')

nw.add_conns(dh_c, dh_i, dh_w)


# characteristic function for generator efficiency
x = np.array([0, 0.2, 0.4, 0.6, 0.8, 1, 1.2])
y = np.array([0, 0.86, 0.9, 0.93, 0.95, 0.96, 0.95])

char = CharLine(x=x, y=y)

# %% busses
<<<<<<< Updated upstream
power = bus('power output')
power.add_comps({'comp': g_turb}, {'comp': comp}, {'comp': turb}, {'comp': pu})
=======
power = Bus('power output')
power.add_comps({'comp': g_turb, 'char': char}, {'comp': comp, 'char': char, 'base': 'bus'}, {'comp': turb, 'char': char}, {'comp': pu, 'char': char, 'base': 'bus'})
>>>>>>> Stashed changes

heat_out = bus('heat output')
heat_out.add_comps({'comp': cond}, {'comp': dh_whr})

heat_in = bus('heat input')
heat_in.add_comps({'comp': c_c})

nw.add_busses(power, heat_out, heat_in)

# %% component parameters
# gas turbine
comp.set_attr(pr=14, eta_s=0.91, design=['pr', 'eta_s'], offdesign=['eta_s_char'])
g_turb.set_attr(eta_s=0.88, design=['eta_s'], offdesign=['eta_s_char', 'cone'])

# steam turbine
suph.set_attr(pr1=0.99, pr2=0.834, design=['pr1', 'pr2'], offdesign=['zeta1', 'zeta2', 'kA_char'])
eco.set_attr(pr1=0.99, pr2=1, design=['pr1', 'pr2'], offdesign=['zeta1', 'zeta2', 'kA_char'])
evap.set_attr(pr1=0.99, ttd_l=25, design=['pr1', 'ttd_l'], offdesign=['zeta1', 'kA_char'])
dh_whr.set_attr(pr1=0.99, pr2=0.98, design=['pr1', 'pr2'], offdesign=['zeta1', 'zeta2', 'kA_char'])
turb.set_attr(eta_s=0.85, design=['eta_s'], offdesign=['eta_s_char', 'cone'])
cond.set_attr(pr1=0.99, pr2=0.98, design=['pr2'], offdesign=['zeta2', 'kA_char'])
pu.set_attr(eta_s=0.75, design=['eta_s'], offdesign=['eta_s_char'])

# %% connection parameters

# gas turbine
c_in.set_attr(
    T=20, p=1, m=250, fluid={
        'Ar': 0.0129, 'N2': 0.7553, 'H2O': 0, 'CH4': 0, 'CO2': 0.0004,
        'O2': 0.2314
    }, design=['m']
)
gt_in.set_attr(T=1200)
gt_out.set_attr(p0=1)
fuel.set_attr(
    T=ref(c_in, 1, 0), h0=800, fluid={
        'CO2': 0.04, 'Ar': 0, 'N2': 0, 'O2': 0, 'H2O': 0, 'CH4': 0.96
    }
)

# waste heat recovery
eco_dh.set_attr(T=290, design=['T'], p0=1)
dh_ch.set_attr(T=100, design=['T'], p=1)

# steam turbine
evap_drum.set_attr(m=ref(drum_suph, 4, 0))
suph_ls.set_attr(
    p=100, T=550, fluid={
        'CO2': 0, 'Ar': 0, 'N2': 0, 'O2': 0, 'H2O': 1, 'CH4': 0
    }, design=['p', 'T']
)
ws.set_attr(p=0.8, design=['p'])

# district heating
dh_c.set_attr(
    T=60, p=5, fluid={
        'CO2': 0, 'Ar': 0, 'N2': 0, 'O2': 0, 'H2O': 1, 'CH4': 0
    }
)
dh_w.set_attr(T=90)

# %%

nw.solve(mode='design')
nw.print_results()
nw.save('design_point')

power.set_attr(P=-100e6)

nw.solve(mode='offdesign', init_path='design_point',
         design_path='design_point')
nw.print_results()

power.set_attr(P=1/0.9 * 0.8 * power.P.val)

nw.solve(mode='offdesign', design_path='design_point')
nw.print_results()
