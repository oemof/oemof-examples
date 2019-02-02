# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 07:45:32 2018

@author: Ms Rohm
"""

from tespy import cmp, con, nwk, hlp

# %% network
fluid_list = ['Ar', 'N2', 'O2', 'CO2', 'CH4', 'H2O']

nw = nwk.network(fluids=fluid_list, p_unit='bar', T_unit='C', h_unit='kJ / kg',
                 p_range=[1, 10], T_range=[110, 1500], h_range=[500, 4000])

# %% components
# gas turbine part
comp = cmp.compressor('compressor')
c_c = cmp.combustion_chamber('combustion')
g_turb = cmp.turbine('gas turbine')

CH4 = cmp.source('fuel source')
air = cmp.source('ambient air')

# waste heat recovery
suph = cmp.heat_exchanger('superheater')
evap = cmp.heat_exchanger('evaporator')
drum = cmp.drum('drum')
eco = cmp.heat_exchanger('economizer')
dh_whr = cmp.heat_exchanger('waste heat recovery')
ch = cmp.sink('chimney')

# steam turbine part
turb = cmp.turbine('steam turbine')
cond = cmp.condenser('condenser')
pump = cmp.pump('feed water pump')
ls_out = cmp.sink('ls sink')
ls_in = cmp.source('ls source')

# district heating
dh_in = cmp.source('district heating backflow')
dh_out = cmp.sink('district heating feedflow')

# %% connections
# gas turbine part
c_in = con.connection(air, 'out1', comp, 'in1')
c_out = con.connection(comp, 'out1', c_c, 'in1')
fuel = con.connection(CH4, 'out1', c_c, 'in2')
gt_in = con.connection(c_c, 'out1', g_turb, 'in1')
gt_out = con.connection(g_turb, 'out1', suph, 'in1')

nw.add_conns(c_in, c_out, fuel, gt_in, gt_out)

# waste heat recovery (flue gas side)
suph_evap = con.connection(suph, 'out1', evap, 'in1')
evap_eco = con.connection(evap, 'out1', eco, 'in1')
eco_dh = con.connection(eco, 'out1', dh_whr, 'in1')
dh_ch = con.connection(dh_whr, 'out1', ch, 'in1')

nw.add_conns(suph_evap, evap_eco, eco_dh, dh_ch)

# waste heat recovery (water side)
eco_drum = con.connection(eco, 'out2', drum, 'in1')
drum_evap = con.connection(drum, 'out1', evap, 'in2')
evap_drum = con.connection(evap, 'out2', drum, 'in2')
drum_suph = con.connection(drum, 'out2', suph, 'in2')

nw.add_conns(eco_drum, drum_evap, evap_drum, drum_suph)

# steam turbine
suph_ls = con.connection(suph, 'out2', ls_out, 'in1')
ls = con.connection(ls_in, 'out1', turb, 'in1')
ws = con.connection(turb, 'out1', cond, 'in1')
c_p = con.connection(cond, 'out1', pump, 'in1')
fw = con.connection(pump, 'out1', eco, 'in2')

nw.add_conns(suph_ls, ls, ws, c_p, fw)

# district heating
dh_c = con.connection(dh_in, 'out1', cond, 'in2')
dh_i = con.connection(cond, 'out2', dh_whr, 'in2')
dh_w = con.connection(dh_whr, 'out2', dh_out, 'in1')

nw.add_conns(dh_c, dh_i, dh_w)


# %% busses
power = con.bus('power output')
power.add_comps({'c': g_turb}, {'c': comp}, {'c': turb}, {'c': pump})

heat_out = con.bus('heat output')
heat_out.add_comps({'c': cond}, {'c': dh_whr})

heat_in = con.bus('heat input')
heat_in.add_comps({'c': c_c})

nw.add_busses(power, heat_out, heat_in)

# %% component parameters
# gas turbine
comp.set_attr(pr=14, eta_s=0.91, design=['pr', 'eta_s'], offdesign=['eta_s_char'])
g_turb.set_attr(eta_s=0.88, design=['eta_s'], offdesign=['eta_s_char', 'cone'])
c_c.set_attr(fuel='CH4')

# steam turbine
suph.set_attr(pr1=0.99, pr2=0.834, design=['pr1', 'pr2'], offdesign=['zeta1', 'zeta2', 'kA'])
eco.set_attr(pr1=0.99, pr2=1, design=['pr1', 'pr2'], offdesign=['zeta1', 'zeta2', 'kA'])
evap.set_attr(pr1=0.99, ttd_l=25, design=['pr1', 'ttd_l'], offdesign=['zeta1', 'kA'])
dh_whr.set_attr(pr1=0.99, pr2=0.98, design=['pr1', 'pr2'], offdesign=['zeta1', 'zeta2', 'kA'])
turb.set_attr(eta_s=0.85, design=['eta_s'], offdesign=['eta_s_char', 'cone'])
cond.set_attr(pr1=0.99, pr2=0.98, design=['pr2'], offdesign=['zeta2', 'kA'])
pump.set_attr(eta_s=0.75, design=['eta_s'], offdesign=['eta_s_char'])

# %% connection parameters

# gas turbine
c_in.set_attr(T=20, p=1, m=250, fluid={'Ar': 0.0129, 'N2': 0.7553, 'H2O': 0,
                                       'CH4': 0, 'CO2': 0.0004, 'O2': 0.2314},
              design=['m'])
gt_in.set_attr(T=1200)
gt_out.set_attr(p0=1)
fuel.set_attr(T=con.ref(c_in, 1, 0), h0=800,
              fluid={'CO2': 0.04, 'Ar': 0, 'N2': 0,
                     'O2': 0, 'H2O': 0, 'CH4': 0.96})

# waste heat recovery
eco_dh.set_attr(T=290, design=['T'], p0=1)
dh_ch.set_attr(T=100, design=['T'], p=1)

# steam turbine
evap_drum.set_attr(m=con.ref(drum_suph, 4, 0))
suph_ls.set_attr(p=100, T=550, fluid={'CO2': 0, 'Ar': 0, 'N2': 0,
                                      'O2': 0, 'H2O': 1, 'CH4': 0},
                 design=['p', 'T'])
ls.set_attr(p=con.ref(suph_ls, 1, 0), h=con.ref(suph_ls, 1, 0))
ws.set_attr(p=0.8, design=['p'])

# district heating
dh_c.set_attr(T=60, p=5, fluid={'CO2': 0, 'Ar': 0, 'N2': 0,
                                'O2': 0, 'H2O': 1, 'CH4': 0})
dh_w.set_attr(T=90)

# %%

nw.solve(mode='design')
nw.print_results()
nw.save('design_point')

power.set_attr(P=0.9 * power.P.val)

nw.solve(mode='offdesign', init_path='design_point',
         design_path='design_point')
nw.print_results()
nw.save('OD')

power.set_attr(P=1/0.9 * 0.8 * power.P.val)

nw.solve(mode='offdesign', init_path='OD',
         design_path='design_point')
nw.print_results()
