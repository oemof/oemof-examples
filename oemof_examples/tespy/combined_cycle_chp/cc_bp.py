# -*- coding: utf-8 -*-
from tespy.networks import Network
from tespy.components import (
    Sink, Source, Compressor, Turbine, Condenser, CombustionChamber, Pump,
    HeatExchanger, Drum, CycleCloser)
from tespy.connections import Connection, Bus, Ref
from tespy.tools import document_model

# %% network
fluid_list = ['Ar', 'N2', 'O2', 'CO2', 'CH4', 'H2O']

nw = Network(fluids=fluid_list, p_unit='bar', T_unit='C', h_unit='kJ / kg')

# %% components
# gas turbine part
comp = Compressor('compressor')
c_c = CombustionChamber('combustion')
g_turb = Turbine('gas turbine')

CH4 = Source('fuel source')
air = Source('ambient air')

# waste heat recovery
suph = HeatExchanger('superheater')
evap = HeatExchanger('evaporator')
dr = Drum('drum')
eco = HeatExchanger('economizer')
dh_whr = HeatExchanger('waste heat recovery')
ch = Sink('chimney')

# steam turbine part
turb = Turbine('steam turbine')
cond = Condenser('condenser')
pu = Pump('feed water pump')
cc = CycleCloser('ls cycle closer')

# district heating
dh_in = Source('district heating backflow')
dh_out = Sink('district heating feedflow')

# %% connections
# gas turbine part
c_in = Connection(air, 'out1', comp, 'in1')
c_out = Connection(comp, 'out1', c_c, 'in1')
fuel = Connection(CH4, 'out1', c_c, 'in2')
gt_in = Connection(c_c, 'out1', g_turb, 'in1')
gt_out = Connection(g_turb, 'out1', suph, 'in1')

nw.add_conns(c_in, c_out, fuel, gt_in, gt_out)

# waste heat recovery (flue gas side)
suph_evap = Connection(suph, 'out1', evap, 'in1')
evap_eco = Connection(evap, 'out1', eco, 'in1')
eco_dh = Connection(eco, 'out1', dh_whr, 'in1')
dh_ch = Connection(dh_whr, 'out1', ch, 'in1')

nw.add_conns(suph_evap, evap_eco, eco_dh, dh_ch)

# waste heat recovery (water side)
eco_drum = Connection(eco, 'out2', dr, 'in1')
drum_evap = Connection(dr, 'out1', evap, 'in2')
evap_drum = Connection(evap, 'out2', dr, 'in2')
drum_suph = Connection(dr, 'out2', suph, 'in2')

nw.add_conns(eco_drum, drum_evap, evap_drum, drum_suph)

# steam turbine
suph_ls = Connection(suph, 'out2', cc, 'in1')
ls = Connection(cc, 'out1', turb, 'in1')
ws = Connection(turb, 'out1', cond, 'in1')
c_p = Connection(cond, 'out1', pu, 'in1')
fw = Connection(pu, 'out1', eco, 'in2')

nw.add_conns(suph_ls, ls, ws, c_p, fw)

# district heating
dh_c = Connection(dh_in, 'out1', cond, 'in2')
dh_i = Connection(cond, 'out2', dh_whr, 'in2')
dh_w = Connection(dh_whr, 'out2', dh_out, 'in1')

nw.add_conns(dh_c, dh_i, dh_w)


# %% busses
power = Bus('power output')
power.add_comps({'comp': g_turb}, {'comp': comp}, {'comp': turb}, {'comp': pu})

heat_out = Bus('heat output')
heat_out.add_comps({'comp': cond}, {'comp': dh_whr})

heat_in = Bus('heat input')
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
    T=Ref(c_in, 1, 0), h0=800, fluid={
        'CO2': 0.04, 'Ar': 0, 'N2': 0, 'O2': 0, 'H2O': 0, 'CH4': 0.96
    }
)

# waste heat recovery
eco_dh.set_attr(T=290, design=['T'], p0=1)
dh_ch.set_attr(T=100, design=['T'], p=1)

# steam turbine
evap_drum.set_attr(m=Ref(drum_suph, 4, 0))
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
document_model(nw, filename='report_design.tex')

power.set_attr(P=0.9 * power.P.val)

nw.solve(mode='offdesign', init_path='design_point',
         design_path='design_point')
nw.print_results()
document_model(nw, filename='report_offdesign.tex')

power.set_attr(P=1/0.9 * 0.8 * power.P.val)

nw.solve(mode='offdesign', design_path='design_point')
nw.print_results()
