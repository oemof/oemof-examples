from tespy.components import source, sink, heat_exchanger_simple, pipe
from tespy.connections import connection, bus, ref
from tespy.networks import network

from sub_consumer import (lin_consum_closed as lc,
                          lin_consum_open as lo,
                          fork as fo)

# %% network

nw = network(fluids=['water'], T_unit='C', p_unit='bar', h_unit='kJ / kg')

# %% components

# sources and sinks

so = source('source')
si = sink('sink')

so1 = source('source1')
si1 = sink('sink1')

so2 = source('source2')
si2 = sink('sink2')

# %% construction part

# pipe_feed

pif1 = pipe('pipe1_feed', ks=7e-5, L=50, D=0.15, offdesign=['kA'])
pif2 = pipe('pipe2_feed', ks=7e-5, L=200, D=0.15, offdesign=['kA'])

pif4 = pipe('pipe4_feed', ks=7e-5, L=50, D=0.15, offdesign=['kA'])
pif7 = pipe('pipe7_feed', ks=7e-5, L=175, D=0.15, offdesign=['kA'])

pif8 = pipe('pipe8_feed', ks=7e-5, L=75, D=0.15, offdesign=['kA'])
pif10 = pipe('pipe10_feed', ks=7e-5, L=450, D=0.1, offdesign=['kA'])

pif11 = pipe('pipe11_feed', ks=7e-5, L=60, D=0.04, offdesign=['kA'])
pif16 = pipe('pipe16_feed', ks=7e-5, L=30, D=0.065, offdesign=['kA'])

pif17 = pipe('pipe17_feed', ks=7e-5, L=250, D=0.065, offdesign=['kA'])
pif21 = pipe('pipe21_feed', ks=7e-5, L=30, D=0.04, offdesign=['kA'])

# pipe_back

pib1 = pipe('pipe1_back', ks=7e-5, L=50, D=0.15, offdesign=['kA'])
pib2 = pipe('pipe2_back', ks=7e-5, L=200, D=0.15, offdesign=['kA'])

pib4 = pipe('pipe4_back', ks=7e-5, L=50, D=0.15, offdesign=['kA'])
pib7 = pipe('pipe7_back', ks=7e-5, L=175, D=0.15, offdesign=['kA'])

pib8 = pipe('pipe8_back', ks=7e-5, L=75, D=0.15, offdesign=['kA'])
pib10 = pipe('pipe10_back', ks=7e-5, L=450, D=0.1, offdesign=['kA'])

pib11 = pipe('pipe11_back', ks=7e-5, L=60, D=0.04, offdesign=['kA'])
pib16 = pipe('pipe16_back', ks=7e-5, L=30, D=0.065, offdesign=['kA'])

pib17 = pipe('pipe17_back', ks=7e-5, L=250, D=0.065, offdesign=['kA'])
pib21 = pipe('pipe21_back', ks=7e-5, L=30, D=0.04, offdesign=['kA'])

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

h1.comps['consumer_0'].set_attr(Q=-5e4, pr=0.99)
h1.comps['consumer_1'].set_attr(Q=-5e4, pr=0.99)

ia.comps['consumer_0'].set_attr(Q=-6.15e5, pr=0.99)
ia.comps['consumer_1'].set_attr(Q=-2.23e5, pr=0.99)
ia.comps['consumer_2'].set_attr(Q=-4e5, pr=0.99)

sc.comps['consumer_0'].set_attr(Q=-5.8e5, pr=0.99)
sc.comps['consumer_1'].set_attr(Q=-1e6, pr=0.99)

h2.comps['consumer_0'].set_attr(Q=-18e3, pr=0.99)
h2.comps['consumer_1'].set_attr(Q=-4e3, pr=0.99)
h2.comps['consumer_2'].set_attr(Q=-4e3, pr=0.99)
h2.comps['consumer_3'].set_attr(Q=-4e3, pr=0.99)
h2.comps['consumer_4'].set_attr(Q=-4e3, pr=0.99)

h3.comps['consumer_0'].set_attr(Q=-1.4e5, pr=0.99)
h3.comps['consumer_1'].set_attr(Q=-5.2e4, pr=0.99)
h3.comps['consumer_2'].set_attr(Q=-5e4, pr=0.99)

h4.comps['consumer_0'].set_attr(Q=-5e4, pr=0.99)
h4.comps['consumer_1'].set_attr(Q=-5e4, pr=0.99)
h4.comps['consumer_2'].set_attr(Q=-5e4, pr=0.99)
h4.comps['consumer_3'].set_attr(Q=-5e4, pr=0.99)


# return temperatures of consumers

for sub in [h1, ia, sc, h2, h3, h4]:
    for i in range(sub.num_consumer):
        sub.conns['cova_' + str(i)].set_attr(T=52)

    # temperature differences over subsystem pipes

    if isinstance(sub, lc):

        for i in range(sub.num_consumer - 1):

            # feed
            dT_feed = ref(sub.conns['spfe_' + str(i)], 1,
                          -sub.comps['feed_' + str(i)].L.val / 100)
            # return
            dT_return = ref(sub.conns['mere_' + str(i + 1)], 1,
                            -sub.comps['return_' + str(i)].L.val / 200)

            sub.conns['fesp_' + str(i + 1)].set_attr(T=dT_feed, design=['T'])
            sub.conns['reme_' + str(i)].set_attr(T=dT_return, design=['T'])

    elif isinstance(sub, lo):

        for i in range(sub.num_consumer - 1):

            # feed
            dT_feed = ref(sub.conns['spfe_' + str(i)], 1,
                          -sub.comps['feed_' + str(i)].L.val / 100)
            # return
            dT_return = ref(sub.conns['mere_' + str(i + 1)], 1,
                            -sub.comps['return_' + str(i)].L.val / 200)

            sub.conns['fesp_' + str(i + 1)].set_attr(T=dT_feed, design=['T'])
            sub.conns['reme_' + str(i)].set_attr(T=dT_return, design=['T'])

# %% pipes of subsystems
# pipe_feed

h1.comps['feed_0'].set_attr(ks=7e-5, L=150, D=0.15, offdesign=['kA'])

ia.comps['feed_0'].set_attr(ks=7e-5, L=100, D=0.15, offdesign=['kA'])
ia.comps['feed_1'].set_attr(ks=7e-5, L=100, D=0.15, offdesign=['kA'])

sc.comps['feed_0'].set_attr(ks=7e-5, L=100, D=0.15, offdesign=['kA'])

h2.comps['feed_0'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA'])
h2.comps['feed_1'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA'])
h2.comps['feed_2'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA'])
h2.comps['feed_3'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA'])

h3.comps['feed_0'].set_attr(ks=7e-5, L=335, D=0.05, offdesign=['kA'])
h3.comps['feed_1'].set_attr(ks=7e-5, L=100, D=0.04, offdesign=['kA'])

h4.comps['feed_0'].set_attr(ks=7e-5, L=30, D=0.04, offdesign=['kA'])
h4.comps['feed_1'].set_attr(ks=7e-5, L=10, D=0.04, offdesign=['kA'])
h4.comps['feed_2'].set_attr(ks=7e-5, L=10, D=0.04, offdesign=['kA'])

# pipe_back

h1.comps['return_0'].set_attr(ks=7e-5, L=150, D=0.15, offdesign=['kA'])

ia.comps['return_0'].set_attr(ks=7e-5, L=100, D=0.15, offdesign=['kA'])
ia.comps['return_0'].set_attr(ks=7e-5, L=100, D=0.15, offdesign=['kA'])

sc.comps['return_0'].set_attr(ks=7e-5, L=100, D=0.15, offdesign=['kA'])

h2.comps['return_0'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA'])
h2.comps['return_1'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA'])
h2.comps['return_2'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA'])
h2.comps['return_3'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA'])

h3.comps['return_0'].set_attr(ks=7e-5, L=335, D=0.05, offdesign=['kA'])
h3.comps['return_1'].set_attr(ks=7e-5, L=100, D=0.04, offdesign=['kA'])

h4.comps['return_0'].set_attr(ks=7e-5, L=30, D=0.04, offdesign=['kA'])
h4.comps['return_1'].set_attr(ks=7e-5, L=10, D=0.04, offdesign=['kA'])
h4.comps['return_2'].set_attr(ks=7e-5, L=10, D=0.04, offdesign=['kA'])


# %% connections

# %% starting area & housing area 1

# feed
so_pif1 = connection(so, 'out1', pif1, 'in1', T=90, p=15, fluid={'water': 1})
pif1_k1f = connection(pif1, 'out1', k1.comps['splitter'], 'in1', T=ref(so_pif1, 1, -1*pif1.L.val/100), design=['T'])
k1f_pif2 = connection(k1.comps['splitter'], 'out1', pif2, 'in1')
pif2_h1 = connection(pif2, 'out1', h1.comps['splitter_0'], 'in1', T=ref(pif1_k1f, 1, -1*pif2.L.val/100), design=['T'])

# back
h1_pib2 = connection(h1.comps['merge_0'], 'out1', pib2, 'in1')
pib2_k1 = connection(pib2, 'out1', k1.comps['valve_0'], 'in1', T=ref(h1_pib2, 1, -1*pib2.L.val/200), design=['T'])
k1_pib1 = connection(k1.comps['merge'], 'out1', pib1, 'in1', p=11)
pib1_si = connection(pib1, 'out1', si, 'in1', T=ref(k1_pib1, 1, -1*pib1.L.val/200), design=['T'])

nw.add_conns(so_pif1, pif1_k1f, k1f_pif2, pif2_h1)
nw.add_conns(h1_pib2, pib2_k1, k1_pib1, pib1_si)
nw.add_subsys(h1)


# %%industrial area

# feed
k1_pif4 = connection(k1.comps['splitter'], 'out2', pif4, 'in1')
pif4_v = connection(pif4, 'out1', ia.comps['splitter_0'], 'in1', T=ref(k1_pif4, 1, -1*pif4.L.val/100), design=['T'])
v_pif7 = connection(ia.comps['splitter_2'], 'out2', pif7, 'in1')
pif7_k2 = connection(pif7, 'out1', k2.comps['splitter'], 'in1', T=ref(v_pif7, 1, -1*pif7.L.val/100), design=['T'])

# back
k2_pib7 = connection(k2.comps['merge'], 'out1', pib7, 'in1', p=12)
pib7_v = connection(pib7, 'out1', ia.comps['merge_2'], 'in1', T=ref(k2_pib7, 1, -1*pib7.L.val/200), design=['T'])
v_pib4 = connection(ia.comps['merge_0'], 'out1', pib4, 'in1')
pib4_k1 = connection(pib4, 'out1', k1.comps['valve_1'], 'in1', T=ref(v_pib4, 1, -1*pib4.L.val/200), design=['T'])

nw.add_conns(k1_pif4, pif4_v, v_pif7, pif7_k2)
nw.add_conns(k2_pib7, pib7_v, v_pib4, pib4_k1)
nw.add_subsys(ia)

# %% sport center

# feed
k2_pif8 = connection(k2.comps['splitter'], 'out1', pif8, 'in1')
pif8_sc = connection(pif8, 'out1', sc.comps['splitter_0'], 'in1', T=ref(k2_pif8, 1, -1*pif8.L.val/100), design=['T'])

# back
sc_pib8 = connection(sc.comps['merge_0'], 'out1', pib8, 'in1')
pib8_k2 = connection(pib8, 'out1', k2.comps['valve_0'], 'in1', T=ref(sc_pib8, 1, -1*pib8.L.val/200), design=['T'])

nw.add_conns(k2_pif8, pif8_sc)
nw.add_conns(sc_pib8, pib8_k2)
nw.add_subsys(sc)

# %% pipe10 & housing area 2

# feed
k2_pif10 = connection(k2.comps['splitter'], 'out2', pif10, 'in1')
pif10_k3 = connection(pif10, 'out1', k3.comps['splitter'], 'in1', T=ref(k2_pif10, 1, -1*pif10.L.val/100), design=['T'])
k3_pif11 = connection(k3.comps['splitter'], 'out1', pif11, 'in1')
pif11_h2 = connection(pif11, 'out1', h2.comps['splitter_0'], 'in1', T=ref(k3_pif11, 1, -1*pif11.L.val/100), design=['T'])

# back
h2_pib11 = connection(h2.comps['merge_0'], 'out1', pib11, 'in1')
pib11_k3 = connection(pib11, 'out1', k3.comps['valve_0'], 'in1', T=ref(h2_pib11, 1, -1*pib11.L.val/200), design=['T'])
k3_pib10 = connection(k3.comps['merge'], 'out1', pib10, 'in1', p=12.5)
pib10_k2 = connection(pib10, 'out1', k2.comps['valve_1'], 'in1', T=ref(k3_pib10, 1, -1*pib10.L.val/200), design=['T'])
#
nw.add_conns(k2_pif10, pif10_k3, k3_pif11, pif11_h2)
nw.add_conns(h2_pib11, pib11_k3, k3_pib10, pib10_k2)
nw.add_subsys(h2)

# %% pipe16 & housing area 3

# feed
k3_pif16 = connection(k3.comps['splitter'], 'out2', pif16, 'in1')
pif16_k4 = connection(pif16, 'out1', k4.comps['splitter'], 'in1', T=ref(k3_pif16, 1, -1*pif16.L.val/100), design=['T'])
k4_pif17 = connection(k4.comps['splitter'], 'out1', pif17, 'in1')
pif17_h3 = connection(pif17, 'out1', h3.comps['splitter_0'], 'in1', T=ref(k4_pif17, 1, -1*pif17.L.val/100), design=['T'])

# back
h3_pib17 = connection(h3.comps['merge_0'], 'out1', pib17, 'in1')
pib17_k4 = connection(pib17, 'out1', k4.comps['valve_0'], 'in1',T=ref(h3_pib17, 1, -1*pib17.L.val/200), design=['T'])
k4_pib16 = connection(k4.comps['merge'], 'out1', pib16, 'in1', p=13)
pib16_k3 = connection(pib16, 'out1', k3.comps['valve_1'], 'in1', T=ref(k4_pib16, 1, -1*pib16.L.val/200), design=['T'])

nw.add_conns(k3_pif16, pif16_k4, k4_pif17, pif17_h3)
nw.add_conns(h3_pib17, pib17_k4, k4_pib16, pib16_k3)
nw.add_subsys(h3)

# %% housing area 4

# feed
k4_pif21 = connection(k4.comps['splitter'], 'out2', pif21, 'in1')
pif21_h4 = connection(pif21, 'out1', h4.comps['splitter_0'], 'in1', T=ref(k4_pif21, 1, -1*pif21.L.val/100), design=['T'])

# back
h4_pib21 = connection(h4.comps['merge_0'], 'out1', pib21, 'in1')
pib21_k4 = connection(pib21, 'out1', k4.comps['valve_1'], 'in1', T=ref(h4_pib21, 1, -1*pib21.L.val/200), design=['T'])

nw.add_conns(k4_pif21, pif21_h4)
nw.add_conns(h4_pib21, pib21_k4)
nw.add_subsys(h4)

# %% busses
#
heat_losses = bus('network losses')
heat_consumer = bus('network consumer')
nw.check_network()

for comp in nw.comps.index:
    if isinstance(comp, pipe):
        comp.set_attr(Tamb=0)

        heat_losses.add_comps({'c': comp})

    if (isinstance(comp, heat_exchanger_simple) and
            not isinstance(comp, pipe)):
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
    if isinstance(comp, pipe):
        comp.set_attr(Tamb=10)

nw.solve('offdesign', design_path='grid')
print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at 10 °C outside temperature:', heat_losses.P.val)

for comp in nw.comps.index:
    if isinstance(comp, pipe):
        comp.set_attr(Tamb=20)

nw.solve('offdesign', design_path='grid')
print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at 20 °C outside temperature:', heat_losses.P.val)

# offdesign case: -10 °C ambient temperature

for comp in nw.comps.index:
    if isinstance(comp, pipe):
        comp.set_attr(Tamb=-10)

nw.solve('offdesign', design_path='grid')
print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at -10 °C outside temperature:', heat_losses.P.val)

# offdesign case: -20 °C ambient temperature

for comp in nw.comps.index:
    if isinstance(comp, pipe):
        comp.set_attr(Tamb=-20)

nw.solve('offdesign', design_path='grid')
print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at -20 °C outside temperature:', heat_losses.P.val)
