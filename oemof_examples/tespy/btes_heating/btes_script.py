from tespy import cmp, con, nwk
from sub_btes_para import btes_para as bp

# %% network

btes = nwk.network(fluids=['water'], T_unit='C', p_unit='bar', h_unit='kJ / kg')

# %% components

# cycle closer (from consumer)
fc_in = cmp.source('from consumer inflow')
fc_out = cmp.sink('from consumer outflow')

sp = cmp.splitter('splitter')
mg = cmp.merge('merge')

# two btes subsystems (pipes in parallel flow):
# 10 pipes for outer ring, 5 pipes inner ring
bo = bp('btes outer', 4)
bi = bp('btes inner', 2)

# circulation pump and consumer
pump = cmp.pump('circulation pump')
cons = cmp.heat_exchanger_simple('consumer')

# %% connections

# inlet
fc_sp = con.connection(fc_in, 'out1', sp, 'in1')
sp_bo = con.connection(sp, 'out1', bo.inlet, 'in1')
sp_bi = con.connection(sp, 'out2', bi.inlet, 'in1')

# outlet
bo_mg = con.connection(bo.outlet, 'out1', mg, 'in1')
bi_mg = con.connection(bi.outlet, 'out1', mg, 'in2')

# consumer and pump
mg_pu = con.connection(mg, 'out1', pump, 'in1')
pu_cons = con.connection(pump, 'out1', cons, 'in1')
cons_fc = con.connection(cons, 'out1', fc_out, 'in1')

btes.add_conns(fc_sp, sp_bo, sp_bi, bo_mg, bi_mg, mg_pu, pu_cons, cons_fc)
btes.add_subsys(bo, bi)

# %% busses

heat = con.bus('consumer heat demand')
heat.add_comps({'c': cons})
btes.add_busses(heat)

# %% component parameters

# pump efficiency
pump.set_attr(eta_s=0.8, design=['eta_s'], offdesign=['eta_s_char'])

# pressure loss consumer
cons.set_attr(pr=0.95, design=['pr'], offdesign=['zeta'])

# %% outer BTES pipes' parameters

# ambient and subsurface temperatures for design case
bo.set_attr(Tamb=5, Tsub=80)

# set pressure losses for design case offdesign pressure ratio by zeta value,
# energyloss by kA (see subsystem definition)
# set desired outlet temperatures of btes pipes (design parameters, offdesign
# parameter is kA, thus temperature will be a result)

bo.set_attr(dT_pb0=0.1, dT_pb1=0.1, pr_pb0=0.99, pr_pb1=0.99)
bo.set_attr(dT_pf0=0.1, dT_pf1=0.1, pr_pf0=0.99, pr_pf1=0.99)
bo.set_attr(T_out0=70, T_out1=70, pr0=0.99, pr1=0.99)

bo.set_attr(dT_pb2=0.1, dT_pb3=0.1, pr_pb2=0.99, pr_pb3=0.99)
bo.set_attr(dT_pf2=0.1, dT_pf3=0.1, pr_pf2=0.99, pr_pf3=0.99)
bo.set_attr(T_out2=70, T_out3=70, pr2=0.99, pr3=0.99)

# inner BTES pipes' parameters

# ambient and subsurface temperatures for design case
bi.set_attr(Tamb=5, Tsub=85)

# set pressure losses for design case offdesign pressure ratio by zeta value,
# energyloss by kA (see subsystem definition)
# set desired outlet temperatures of btes pipes (design parameters, offdesign
# parameter is kA, thus temperature will be a result)

bi.set_attr(dT_pb0=0.1, dT_pb1=0.1, pr_pb0=0.99, pr_pb1=0.99)
bi.set_attr(dT_pf0=0.1, dT_pf1=0.1, pr_pf0=0.99, pr_pf1=0.99)
bi.set_attr(T_out0=75, T_out1=75, pr0=0.99, pr1=0.99)

# %% connection parameters

# pressure after the valves
mg_pu.set_attr(p=9)
# specify the mass flow distribution between the two btes systems
# a) specify temperature of mixture at merge
#mg_pu.set_attr(T=72)
# b) specify zeta value for one of the valves (I took this value from
# previously calculated results)
#bo.valve[0].set_attr(zeta=67870207254.06077)
# c) specify mass flow distribution directly (without good starting values the
# other methods will most probably fail), 2/5 of total mass flow will flow
# through outer btes pipes
sp_bo.set_attr(m=con.ref(fc_sp, 3/5, 0))

# system inlet
fc_sp.set_attr(p=10, T=50, fluid={'water': 1})

# closing the circle
cons_fc.set_attr(p=con.ref(fc_sp, 1, 0), h=con.ref(fc_sp, 1, 0))

# %% consumer heat demand

heat.set_attr(P=-20e3)

# %% solving

btes.solve('design')
btes.save('BTES')
btes.print_results()

heat.set_attr(P=-18e3)

btes.solve('offdesign', init_path='BTES',
           design_path='BTES')
btes.save('BTES_OD')
btes.print_results()
