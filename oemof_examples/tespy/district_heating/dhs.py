from tespy import nwk, con, cmp, nwkr, hlp
from sub_consumer import (lin_consum_closed as lc,
                          lin_consum_open as lo,
                          fork as fo)
# %% network

nw = nwk.network(fluids=['water'], T_unit='C', p_unit='bar', h_unit='kJ / kg')

# %% components

# sources and sinks

so = cmp.source('source')
si = cmp.sink('sink')

so1 = cmp.source('source1')
si1 = cmp.sink('sink1')

so2 = cmp.source('source2')
si2 = cmp.sink('sink2')

# %% construction part

# pipe_feed

pif1 = cmp.pipe('pipe1_feed', ks=7e-5, L=50, D=0.15, offdesign=['kA'])
pif2 = cmp.pipe('pipe2_feed', ks=7e-5, L=200, D=0.15, offdesign=['kA'])

pif4 = cmp.pipe('pipe4_feed', ks=7e-5, L=50, D=0.15, offdesign=['kA'])
pif7 = cmp.pipe('pipe7_feed', ks=7e-5, L=175, D=0.15, offdesign=['kA'])

pif8 = cmp.pipe('pipe8_feed', ks=7e-5, L=75, D=0.15, offdesign=['kA'])
pif10 = cmp.pipe('pipe10_feed', ks=7e-5, L=450, D=0.1, offdesign=['kA'])

pif11 = cmp.pipe('pipe11_feed', ks=7e-5, L=60, D=0.04, offdesign=['kA'])
pif16 = cmp.pipe('pipe16_feed', ks=7e-5, L=30, D=0.065, offdesign=['kA'])

pif17 = cmp.pipe('pipe17_feed', ks=7e-5, L=250, D=0.065, offdesign=['kA'])
pif21 = cmp.pipe('pipe21_feed', ks=7e-5, L=30, D=0.04, offdesign=['kA'])

# pipe_back

pib1 = cmp.pipe('pipe1_back', ks=7e-5, L=50, D=0.15, offdesign=['kA'])
pib2 = cmp.pipe('pipe2_back', ks=7e-5, L=200, D=0.15, offdesign=['kA'])

pib4 = cmp.pipe('pipe4_back', ks=7e-5, L=50, D=0.15, offdesign=['kA'])
pib7 = cmp.pipe('pipe7_back', ks=7e-5, L=175, D=0.15, offdesign=['kA'])

pib8 = cmp.pipe('pipe8_back', ks=7e-5, L=75, D=0.15, offdesign=['kA'])
pib10 = cmp.pipe('pipe10_back', ks=7e-5, L=450, D=0.1, offdesign=['kA'])

pib11 = cmp.pipe('pipe11_back', ks=7e-5, L=60, D=0.04, offdesign=['kA'])
pib16 = cmp.pipe('pipe16_back', ks=7e-5, L=30, D=0.065, offdesign=['kA'])

pib17 = cmp.pipe('pipe17_back', ks=7e-5, L=250, D=0.065, offdesign=['kA'])
pib21 = cmp.pipe('pipe21_back', ks=7e-5, L=30, D=0.04, offdesign=['kA'])

# %% subsystems for forks

k1 = fo('K1', 2)
k2 = fo('K2', 2)
k3 = fo('K3', 2)
k4 = fo('K4', 2)

nw.add_subsys(k1, k2, k3, k4)

# %% subsystems for consumers

h1 = lc('housing area 1', 2)
ia = lo('industrial area', 3)
sc = lc('sport center', 2)
h2 = lc('housing area 2', 5)
h3 = lc('housing area 3', 3)
h4 = lc('housing area 4', 4)

# consumer

h1.set_attr(Q0=-5e4, pr0=0.99, T_out0=52)
h1.set_attr(Q1=-5e4, pr1=0.99, T_out1=52)

ia.set_attr(Q0=-6.15e5, pr0=0.99, T_out0=52)
ia.set_attr(Q1=-2.23e5, pr1=0.99, T_out1=52)
ia.set_attr(Q2=-4e5, pr2=0.99, T_out2=52)

sc.set_attr(Q0=-5.8e5, pr0=0.99, T_out0=52)
sc.set_attr(Q1=-1e6, pr1=0.99, T_out1=52)

h2.set_attr(Q0=-18e3, pr0=0.99, T_out0=52)
h2.set_attr(Q1=-4e3, pr1=0.99, T_out1=52)
h2.set_attr(Q2=-4e3, pr2=0.99, T_out2=52)
h2.set_attr(Q3=-4e3, pr3=0.99, T_out3=52)
h2.set_attr(Q4=-4e3, pr4=0.99, T_out4=52)

h3.set_attr(Q0=-1.4e5, pr0=0.99, T_out0=52)
h3.set_attr(Q1=-5.2e4, pr1=0.99, T_out1=52)
h3.set_attr(Q2=-5e4, pr2=0.99, T_out2=52)

h4.set_attr(Q0=-5e4, pr0=0.99, T_out0=52)
h4.set_attr(Q1=-5e4, pr1=0.99, T_out1=52)
h4.set_attr(Q2=-5e4, pr2=0.99, T_out2=52)
h4.set_attr(Q3=-5e4, pr3=0.99, T_out3=52)

# pipes of subsystems

# pipe_feed

h1.set_attr(ks_pf0=7e-5, L_pf0=150, D_pf0=0.15, dT_pf0=1.5)

ia.set_attr(ks_pf0=7e-5, L_pf0=100, D_pf0=0.15, dT_pf0=1)
ia.set_attr(ks_pf1=7e-5, L_pf1=100, D_pf1=0.15, dT_pf1=1)

sc.set_attr(ks_pf0=7e-5, L_pf0=100, D_pf0=0.15, dT_pf0=1)

h2.set_attr(ks_pf0=7e-5, L_pf0=60, D_pf0=0.04, dT_pf0=0.6)
h2.set_attr(ks_pf1=7e-5, L_pf1=60, D_pf1=0.04, dT_pf1=0.6)
h2.set_attr(ks_pf2=7e-5, L_pf2=60, D_pf2=0.04, dT_pf2=0.6)
h2.set_attr(ks_pf3=7e-5, L_pf3=60, D_pf3=0.04, dT_pf3=0.6)

h3.set_attr(ks_pf0=7e-5, L_pf0=335, D_pf0=0.05, dT_pf0=3.35)
h3.set_attr(ks_pf1=7e-5, L_pf1=100, D_pf1=0.04, dT_pf1=1)

h4.set_attr(ks_pf0=7e-5, L_pf0=30, D_pf0=0.04, dT_pf0=0.3)
h4.set_attr(ks_pf1=7e-5, L_pf1=10, D_pf1=0.04, dT_pf1=0.1)
h4.set_attr(ks_pf2=7e-5, L_pf2=10, D_pf2=0.04, dT_pf2=0.1)

# pipe_back

h1.set_attr(ks_pb0=7e-5, L_pb0=150, D_pb0=0.15, dT_pb0=0.75)

ia.set_attr(ks_pb0=7e-5, L_pb0=100, D_pb0=0.15, dT_pb0=0.5)
ia.set_attr(ks_pb1=7e-5, L_pb1=100, D_pb1=0.15, dT_pb1=0.5)

sc.set_attr(ks_pb0=7e-5, L_pb0=100, D_pb0=0.15, dT_pb0=0.5)

h2.set_attr(ks_pb0=7e-5, L_pb0=60, D_pb0=0.04, dT_pb0=0.3)
h2.set_attr(ks_pb1=7e-5, L_pb1=60, D_pb1=0.04, dT_pb1=0.3)
h2.set_attr(ks_pb2=7e-5, L_pb2=60, D_pb2=0.04, dT_pb2=0.3)
h2.set_attr(ks_pb3=7e-5, L_pb3=60, D_pb3=0.04, dT_pb3=0.3)

h3.set_attr(ks_pb0=7e-5, L_pb0=335, D_pb0=0.05, dT_pb0=1.675)
h3.set_attr(ks_pb1=7e-5, L_pb1=100, D_pb1=0.04, dT_pb1=0.5)

h4.set_attr(ks_pb0=7e-5, L_pb0=30, D_pb0=0.04, dT_pb0=0.15)
h4.set_attr(ks_pb1=7e-5, L_pb1=10, D_pb1=0.04, dT_pb1=0.05)
h4.set_attr(ks_pb2=7e-5, L_pb2=10, D_pb2=0.04, dT_pb2=0.05)


# %% connections

# %% starting area & housing area 1

# feed
so_pif1 = con.connection(so, 'out1', pif1, 'in1',
                         T=90, p=15, fluid={'water': 1})
pif1_k1f = con.connection(pif1, 'out1', k1.inlet, 'in1',
                          T=con.ref(so_pif1, 1, -1*pif1.L.val/100),
                          design=['T'])
k1f_pif2 = con.connection(k1.outlet, 'out2', pif2, 'in1')
pif2_h1 = con.connection(pif2, 'out1', h1.inlet, 'in1',
                         T=con.ref(pif1_k1f, 1, -1*pif2.L.val/100),
                         design=['T'])

# back
h1_pib2 = con.connection(h1.outlet, 'out1', pib2, 'in1')
pib2_k1 = con.connection(pib2, 'out1', k1.inlet, 'in2',
                         T=con.ref(h1_pib2, 1, -1*pib2.L.val/200),
                         design=['T'])
k1_pib1 = con.connection(k1.outlet, 'out1', pib1, 'in1', p=11)
pib1_si = con.connection(pib1, 'out1', si, 'in1',
                         T=con.ref(k1_pib1, 1, -1*pib1.L.val/200),
                         design=['T'])

nw.add_conns(so_pif1, pif1_k1f, k1f_pif2, pif2_h1)
nw.add_conns(h1_pib2, pib2_k1, k1_pib1, pib1_si)
nw.add_subsys(h1)


# %%industrial area

# feed
k1_pif4 = con.connection(k1.outlet, 'out3', pif4, 'in1')
pif4_v = con.connection(pif4, 'out1', ia.inlet, 'in1',
                        T=con.ref(k1_pif4, 1, -1*pif4.L.val/100), design=['T'])
v_pif7 = con.connection(ia.outlet, 'out2', pif7, 'in1')
pif7_k2 = con.connection(pif7, 'out1', k2.inlet, 'in1',
                         T=con.ref(v_pif7, 1, -1*pif7.L.val/100),
                         design=['T'])

# back
k2_pib7 = con.connection(k2.outlet, 'out1', pib7, 'in1', p=12)
pib7_v = con.connection(pib7, 'out1', ia.inlet, 'in2',
                        T=con.ref(k2_pib7, 1, -1*pib7.L.val/200),
                        design=['T'])
v_pib4 = con.connection(ia.outlet, 'out1', pib4, 'in1')
pib4_k1 = con.connection(pib4, 'out1', k1.inlet, 'in3',
                         T=con.ref(v_pib4, 1, -1*pib4.L.val/200), design=['T'])

nw.add_conns(k1_pif4, pif4_v, v_pif7, pif7_k2)
nw.add_conns(k2_pib7, pib7_v, v_pib4, pib4_k1)
nw.add_subsys(ia)

# %% sport center

# feed
k2_pif8 = con.connection(k2.outlet, 'out2', pif8, 'in1')
pif8_sc = con.connection(pif8, 'out1', sc.inlet, 'in1',
                         T=con.ref(k2_pif8, 1, -1*pif8.L.val/100),
                         design=['T'])

# back
sc_pib8 = con.connection(sc.outlet, 'out1', pib8, 'in1')
pib8_k2 = con.connection(pib8, 'out1', k2.inlet, 'in2',
                         T=con.ref(sc_pib8, 1, -1*pib8.L.val/200),
                         design=['T'])

nw.add_conns(k2_pif8, pif8_sc)
nw.add_conns(sc_pib8, pib8_k2)
nw.add_subsys(sc)

# %% pipe10 & housing area 2

# feed
k2_pif10 = con.connection(k2.outlet, 'out3', pif10, 'in1')
pif10_k3 = con.connection(pif10, 'out1', k3.inlet, 'in1',
                          T=con.ref(k2_pif10, 1, -1*pif10.L.val/100),
                          design=['T'])
k3_pif11 = con.connection(k3.outlet, 'out2', pif11, 'in1')
pif11_h2 = con.connection(pif11, 'out1', h2.inlet, 'in1',
                          T=con.ref(k3_pif11, 1, -1*pif11.L.val/100),
                          design=['T'])

# back
h2_pib11 = con.connection(h2.outlet, 'out1', pib11, 'in1')
pib11_k3 = con.connection(pib11, 'out1', k3.inlet, 'in2',
                          T=con.ref(h2_pib11, 1, -1*pib11.L.val/200),
                          design=['T'])
k3_pib10 = con.connection(k3.outlet, 'out1', pib10, 'in1', p=12.5)
pib10_k2 = con.connection(pib10, 'out1', k2.inlet, 'in3',
                          T=con.ref(k3_pib10, 1, -1*pib10.L.val/200),
                          design=['T'])
#
nw.add_conns(k2_pif10, pif10_k3, k3_pif11, pif11_h2)
nw.add_conns(h2_pib11, pib11_k3, k3_pib10, pib10_k2)
nw.add_subsys(h2)

# %% pipe16 & housing area 3

# feed
k3_pif16 = con.connection(k3.outlet, 'out3', pif16, 'in1')
pif16_k4 = con.connection(pif16, 'out1', k4.inlet, 'in1',
                          T=con.ref(k3_pif16, 1, -1*pif16.L.val/100),
                          design=['T'])
k4_pif17 = con.connection(k4.outlet, 'out2', pif17, 'in1')
pif17_h3 = con.connection(pif17, 'out1', h3.inlet, 'in1',
                          T=con.ref(k4_pif17, 1, -1*pif17.L.val/100),
                          design=['T'])

# back
h3_pib17 = con.connection(h3.outlet, 'out1', pib17, 'in1')
pib17_k4 = con.connection(pib17, 'out1', k4.inlet, 'in2',
                          T=con.ref(h3_pib17, 1, -1*pib17.L.val/200),
                          design=['T'])
k4_pib16 = con.connection(k4.outlet, 'out1', pib16, 'in1', p=13)
pib16_k3 = con.connection(pib16, 'out1', k3.inlet, 'in3',
                          T=con.ref(k4_pib16, 1, -1*pib16.L.val/200),
                          design=['T'])

nw.add_conns(k3_pif16, pif16_k4, k4_pif17, pif17_h3)
nw.add_conns(h3_pib17, pib17_k4, k4_pib16, pib16_k3)
nw.add_subsys(h3)

# %% housing area 4

# feed
k4_pif21 = con.connection(k4.outlet, 'out3', pif21, 'in1')
pif21_h4 = con.connection(pif21, 'out1', h4.inlet, 'in1',
                          T=con.ref(k4_pif21, 1, -1*pif21.L.val/100),
                          design=['T'])

# back
h4_pib21 = con.connection(h4.outlet, 'out1', pib21, 'in1')
pib21_k4 = con.connection(pib21, 'out1', k4.inlet, 'in3',
                          T=con.ref(h4_pib21, 1, -1*pib21.L.val/200),
                          design=['T'])

nw.add_conns(k4_pif21, pif21_h4)
nw.add_conns(h4_pib21, pib21_k4)
nw.add_subsys(h4)

# %% busses
#
heat_losses = con.bus('network losses')
heat_consumer = con.bus('network consumer')
nw.check_network()

for comp in nw.comps.index:
    if isinstance(comp, cmp.pipe):
        comp.set_attr(Tamb=0)

        heat_losses.add_comps({'c': comp})

    if (isinstance(comp, cmp.heat_exchanger_simple) and
            not isinstance(comp, cmp.pipe)):
        heat_consumer.add_comps({'c': comp})

nw.add_busses(heat_losses, heat_consumer)

# %% solve

# design case: 0 °C ambient temperature
nw.solve('design')
nw.save('grid')

print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at 0 °C outside temperature (design):', heat_losses.P.val)

# offdesign case: 10 °C ambient temperature

for comp in nw.comps.index:
    if isinstance(comp, cmp.pipe):
        comp.set_attr(Tamb=10)

nw.solve('offdesign', design_path='grid')
print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at 10 °C outside temperature:', heat_losses.P.val)

for comp in nw.comps.index:
    if isinstance(comp, cmp.pipe):
        comp.set_attr(Tamb=20)

nw.solve('offdesign', design_path='grid')
print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at 20 °C outside temperature:', heat_losses.P.val)

# offdesign case: -10 °C ambient temperature

for comp in nw.comps.index:
    if isinstance(comp, cmp.pipe):
        comp.set_attr(Tamb=-10)

nw.solve('offdesign', design_path='grid')
print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at -10 °C outside temperature:', heat_losses.P.val)

# offdesign case: -20 °C ambient temperature

for comp in nw.comps.index:
    if isinstance(comp, cmp.pipe):
        comp.set_attr(Tamb=-20)

nw.solve('offdesign', design_path='grid')
print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at -20 °C outside temperature:', heat_losses.P.val)
