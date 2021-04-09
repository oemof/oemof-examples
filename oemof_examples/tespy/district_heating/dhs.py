# -*- coding: utf-8 -*-
from tespy.components import Source, Sink, HeatExchangerSimple, Pipe
from tespy.connections import Connection, Bus, Ref
from tespy.networks import Network
from tespy.tools import document_model

from sub_consumer import (LinConsumClosed as lc,
                          LinConsumOpen as lo,
                          Fork as fo)

# %% network

nw = Network(fluids=['water'], T_unit='C', p_unit='bar', h_unit='kJ / kg')

# %% components

# sources and sinks

so = Source('source')
si = Sink('sink')

so1 = Source('source1')
si1 = Sink('sink1')

so2 = Source('source2')
si2 = Sink('sink2')

# %% construction part

# pipe_feed

pif1 = Pipe('pipe1_feed', ks=7e-5, L=50, D=0.15, offdesign=['kA_char'])
pif2 = Pipe('pipe2_feed', ks=7e-5, L=200, D=0.15, offdesign=['kA_char'])

pif4 = Pipe('pipe4_feed', ks=7e-5, L=50, D=0.15, offdesign=['kA_char'])
pif7 = Pipe('pipe7_feed', ks=7e-5, L=175, D=0.15, offdesign=['kA_char'])

pif8 = Pipe('pipe8_feed', ks=7e-5, L=75, D=0.15, offdesign=['kA_char'])
pif10 = Pipe('pipe10_feed', ks=7e-5, L=450, D=0.1, offdesign=['kA_char'])

pif11 = Pipe('pipe11_feed', ks=7e-5, L=60, D=0.04, offdesign=['kA_char'])
pif16 = Pipe('pipe16_feed', ks=7e-5, L=30, D=0.065, offdesign=['kA_char'])

pif17 = Pipe('pipe17_feed', ks=7e-5, L=250, D=0.065, offdesign=['kA_char'])
pif21 = Pipe('pipe21_feed', ks=7e-5, L=30, D=0.04, offdesign=['kA_char'])

# pipe_back

pib1 = Pipe('pipe1_back', ks=7e-5, L=50, D=0.15, offdesign=['kA_char'])
pib2 = Pipe('pipe2_back', ks=7e-5, L=200, D=0.15, offdesign=['kA_char'])

pib4 = Pipe('pipe4_back', ks=7e-5, L=50, D=0.15, offdesign=['kA_char'])
pib7 = Pipe('pipe7_back', ks=7e-5, L=175, D=0.15, offdesign=['kA_char'])

pib8 = Pipe('pipe8_back', ks=7e-5, L=75, D=0.15, offdesign=['kA_char'])
pib10 = Pipe('pipe10_back', ks=7e-5, L=450, D=0.1, offdesign=['kA_char'])

pib11 = Pipe('pipe11_back', ks=7e-5, L=60, D=0.04, offdesign=['kA_char'])
pib16 = Pipe('pipe16_back', ks=7e-5, L=30, D=0.065, offdesign=['kA_char'])

pib17 = Pipe('pipe17_back', ks=7e-5, L=250, D=0.065, offdesign=['kA_char'])
pib21 = Pipe('pipe21_back', ks=7e-5, L=30, D=0.04, offdesign=['kA_char'])

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

# consumers of subsystems

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

# pipes of subsystems
# feed flow

h1.comps['feed_0'].set_attr(ks=7e-5, L=150, D=0.15, offdesign=['kA_char'])

ia.comps['feed_0'].set_attr(ks=7e-5, L=100, D=0.15, offdesign=['kA_char'])
ia.comps['feed_1'].set_attr(ks=7e-5, L=100, D=0.15, offdesign=['kA_char'])

sc.comps['feed_0'].set_attr(ks=7e-5, L=100, D=0.15, offdesign=['kA_char'])

h2.comps['feed_0'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA_char'])
h2.comps['feed_1'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA_char'])
h2.comps['feed_2'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA_char'])
h2.comps['feed_3'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA_char'])

h3.comps['feed_0'].set_attr(ks=7e-5, L=335, D=0.05, offdesign=['kA_char'])
h3.comps['feed_1'].set_attr(ks=7e-5, L=100, D=0.04, offdesign=['kA_char'])

h4.comps['feed_0'].set_attr(ks=7e-5, L=30, D=0.04, offdesign=['kA_char'])
h4.comps['feed_1'].set_attr(ks=7e-5, L=10, D=0.04, offdesign=['kA_char'])
h4.comps['feed_2'].set_attr(ks=7e-5, L=10, D=0.04, offdesign=['kA_char'])

# return flow

h1.comps['return_0'].set_attr(ks=7e-5, L=150, D=0.15, offdesign=['kA_char'])

ia.comps['return_0'].set_attr(ks=7e-5, L=100, D=0.15, offdesign=['kA_char'])
ia.comps['return_1'].set_attr(ks=7e-5, L=100, D=0.15, offdesign=['kA_char'])

sc.comps['return_0'].set_attr(ks=7e-5, L=100, D=0.15, offdesign=['kA_char'])

h2.comps['return_0'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA_char'])
h2.comps['return_1'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA_char'])
h2.comps['return_2'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA_char'])
h2.comps['return_3'].set_attr(ks=7e-5, L=60, D=0.04, offdesign=['kA_char'])

h3.comps['return_0'].set_attr(ks=7e-5, L=335, D=0.05, offdesign=['kA_char'])
h3.comps['return_1'].set_attr(ks=7e-5, L=100, D=0.04, offdesign=['kA_char'])

h4.comps['return_0'].set_attr(ks=7e-5, L=30, D=0.04, offdesign=['kA_char'])
h4.comps['return_1'].set_attr(ks=7e-5, L=10, D=0.04, offdesign=['kA_char'])
h4.comps['return_2'].set_attr(ks=7e-5, L=10, D=0.04, offdesign=['kA_char'])


# temperature difference factor for pipes:

dT_feed = 100
dT_return = 200
# return temperatures of consumers

for sub in [h1, ia, sc, h2, h3, h4]:
    for i in range(sub.num_consumer):
        sub.conns['cova_' + str(i)].set_attr(T=52)

    # temperature differences over subsystem pipes

    if isinstance(sub, lc):

        for i in range(sub.num_consumer - 1):

            # feed
            dT_feed_ref = Ref(
                sub.conns['spfe_' + str(i)], 1,
                -sub.comps['feed_' + str(i)].L.val / dT_feed)
            # return
            if i == sub.num_consumer - 1:
                dT_return_ref = Ref(
                    sub.conns['mere_' + str(i + 1)], 1,
                    -sub.comps['return_' + str(i)].L.val / dT_return)
            else:
                dT_return_ref = Ref(
                    sub.conns['cova_' + str(i + 1)], 1,
                    -sub.comps['return_' + str(i)].L.val / dT_return)

            if i == sub.num_consumer - 2:
                sub.conns['spco_' + str(i + 1)].set_attr(
                    T=dT_feed_ref, design=['T'])
            else:
                sub.conns['fesp_' + str(i + 1)].set_attr(
                    T=dT_feed_ref, design=['T'])
            sub.conns['reme_' + str(i)].set_attr(T=dT_return_ref, design=['T'])

    elif isinstance(sub, lo):

        for i in range(sub.num_consumer - 1):

            # feed
            dT_feed_ref = Ref(
                sub.conns['spfe_' + str(i)], 1,
                -sub.comps['feed_' + str(i)].L.val / dT_feed)
            # return
            dT_return_ref = Ref(
                sub.conns['mere_' + str(i + 1)], 1,
                -sub.comps['return_' + str(i)].L.val / dT_return)

            sub.conns['fesp_' + str(i + 1)].set_attr(
                T=dT_feed_ref, design=['T'])
            sub.conns['reme_' + str(i)].set_attr(
                T=dT_return_ref, design=['T'])


# %% connections

# %% starting area & housing area 1

# feed
so_pif1 = Connection(so, 'out1', pif1, 'in1', T=90, p=15, fluid={'water': 1})
pif1_k1f = Connection(pif1, 'out1', k1.comps['splitter'], 'in1', T=Ref(so_pif1, 1, -pif1.L.val / dT_feed), design=['T'])
k1f_pif2 = Connection(k1.comps['splitter'], 'out1', pif2, 'in1')
pif2_h1 = Connection(pif2, 'out1', h1.comps['splitter_0'], 'in1', T=Ref(pif1_k1f, 1, -pif2.L.val / dT_feed), design=['T'])

# back
h1_pib2 = Connection(h1.comps['merge_0'], 'out1', pib2, 'in1')
pib2_k1 = Connection(pib2, 'out1', k1.comps['valve_0'], 'in1', T=Ref(h1_pib2, 1, -pib2.L.val / dT_return), design=['T'])
k1_pib1 = Connection(k1.comps['merge'], 'out1', pib1, 'in1', p=11)
pib1_si = Connection(pib1, 'out1', si, 'in1', T=Ref(k1_pib1, 1, -pib1.L.val / dT_return), design=['T'])

nw.add_conns(so_pif1, pif1_k1f, k1f_pif2, pif2_h1)
nw.add_conns(h1_pib2, pib2_k1, k1_pib1, pib1_si)
nw.add_subsys(h1)


# %%industrial area

# feed
k1_pif4 = Connection(k1.comps['splitter'], 'out2', pif4, 'in1')
pif4_v = Connection(pif4, 'out1', ia.comps['splitter_0'], 'in1', T=Ref(k1_pif4, 1, -pif4.L.val / dT_feed), design=['T'])
v_pif7 = Connection(ia.comps['splitter_2'], 'out2', pif7, 'in1')
pif7_k2 = Connection(pif7, 'out1', k2.comps['splitter'], 'in1', T=Ref(v_pif7, 1, -pif7.L.val / dT_feed), design=['T'])

# back
k2_pib7 = Connection(k2.comps['merge'], 'out1', pib7, 'in1', p=12)
pib7_v = Connection(pib7, 'out1', ia.comps['merge_2'], 'in1', T=Ref(k2_pib7, 1, -pib7.L.val / dT_return), design=['T'])
v_pib4 = Connection(ia.comps['merge_0'], 'out1', pib4, 'in1')
pib4_k1 = Connection(pib4, 'out1', k1.comps['valve_1'], 'in1', T=Ref(v_pib4, 1, -pib4.L.val / dT_return), design=['T'])

nw.add_conns(k1_pif4, pif4_v, v_pif7, pif7_k2)
nw.add_conns(k2_pib7, pib7_v, v_pib4, pib4_k1)
nw.add_subsys(ia)

# %% sport center

# feed
k2_pif8 = Connection(k2.comps['splitter'], 'out1', pif8, 'in1')
pif8_sc = Connection(pif8, 'out1', sc.comps['splitter_0'], 'in1', T=Ref(k2_pif8, 1, -pif8.L.val / dT_feed), design=['T'])

# back
sc_pib8 = Connection(sc.comps['merge_0'], 'out1', pib8, 'in1')
pib8_k2 = Connection(pib8, 'out1', k2.comps['valve_0'], 'in1', T=Ref(sc_pib8, 1, -pib8.L.val / dT_return), design=['T'])

nw.add_conns(k2_pif8, pif8_sc)
nw.add_conns(sc_pib8, pib8_k2)
nw.add_subsys(sc)

# %% pipe10 & housing area 2

# feed
k2_pif10 = Connection(k2.comps['splitter'], 'out2', pif10, 'in1')
pif10_k3 = Connection(pif10, 'out1', k3.comps['splitter'], 'in1', T=Ref(k2_pif10, 1, -pif10.L.val / dT_feed), design=['T'])
k3_pif11 = Connection(k3.comps['splitter'], 'out1', pif11, 'in1')
pif11_h2 = Connection(pif11, 'out1', h2.comps['splitter_0'], 'in1', T=Ref(k3_pif11, 1, -pif11.L.val / dT_feed), design=['T'])

# back
h2_pib11 = Connection(h2.comps['merge_0'], 'out1', pib11, 'in1')
pib11_k3 = Connection(pib11, 'out1', k3.comps['valve_0'], 'in1', T=Ref(h2_pib11, 1, -pib11.L.val / dT_return), design=['T'])
k3_pib10 = Connection(k3.comps['merge'], 'out1', pib10, 'in1', p=12.5)
pib10_k2 = Connection(pib10, 'out1', k2.comps['valve_1'], 'in1', T=Ref(k3_pib10, 1, -pib10.L.val / dT_return), design=['T'])
#
nw.add_conns(k2_pif10, pif10_k3, k3_pif11, pif11_h2)
nw.add_conns(h2_pib11, pib11_k3, k3_pib10, pib10_k2)
nw.add_subsys(h2)

# %% pipe16 & housing area 3

# feed
k3_pif16 = Connection(k3.comps['splitter'], 'out2', pif16, 'in1')
pif16_k4 = Connection(pif16, 'out1', k4.comps['splitter'], 'in1', T=Ref(k3_pif16, 1, -pif16.L.val / dT_feed), design=['T'])
k4_pif17 = Connection(k4.comps['splitter'], 'out1', pif17, 'in1')
pif17_h3 = Connection(pif17, 'out1', h3.comps['splitter_0'], 'in1', T=Ref(k4_pif17, 1, -pif17.L.val / dT_feed), design=['T'])

# back
h3_pib17 = Connection(h3.comps['merge_0'], 'out1', pib17, 'in1')
pib17_k4 = Connection(pib17, 'out1', k4.comps['valve_0'], 'in1',T=Ref(h3_pib17, 1, -pib17.L.val / dT_return), design=['T'])
k4_pib16 = Connection(k4.comps['merge'], 'out1', pib16, 'in1', p=12.75)
pib16_k3 = Connection(pib16, 'out1', k3.comps['valve_1'], 'in1', T=Ref(k4_pib16, 1, -pib16.L.val / dT_return), design=['T'])

nw.add_conns(k3_pif16, pif16_k4, k4_pif17, pif17_h3)
nw.add_conns(h3_pib17, pib17_k4, k4_pib16, pib16_k3)
nw.add_subsys(h3)

# %% housing area 4

# feed
k4_pif21 = Connection(k4.comps['splitter'], 'out2', pif21, 'in1')
pif21_h4 = Connection(pif21, 'out1', h4.comps['splitter_0'], 'in1', T=Ref(k4_pif21, 1, -pif21.L.val / dT_feed), design=['T'])

# back
h4_pib21 = Connection(h4.comps['merge_0'], 'out1', pib21, 'in1')
pib21_k4 = Connection(pib21, 'out1', k4.comps['valve_1'], 'in1', T=Ref(h4_pib21, 1, -pib21.L.val / dT_return), design=['T'])

nw.add_conns(k4_pif21, pif21_h4)
nw.add_conns(h4_pib21, pib21_k4)
nw.add_subsys(h4)

# %% busses
#
heat_losses = Bus('network losses')
heat_consumer = Bus('network consumer')
nw.check_network()

for comp in nw.comps['object']:
    if isinstance(comp, Pipe):
        comp.set_attr(Tamb=0)

        heat_losses.add_comps({'comp': comp})

    if (isinstance(comp, HeatExchangerSimple) and
            not isinstance(comp, Pipe)):
        heat_consumer.add_comps({'comp': comp})

nw.add_busses(heat_losses, heat_consumer)

# %% solve

# design case: 0 °C ambient temperature
nw.solve('design')
nw.save('grid')
document_model(nw)
# no documentation of offedesign state added, as report creation takes
# quite long with all characteristics applied, try it out yourself :)

print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at 0 °C outside temperature (design):', heat_losses.P.val)

# offdesign case: 10 °C ambient temperature

for comp in nw.comps['object']:
    if isinstance(comp, Pipe):
        comp.set_attr(Tamb=10)

nw.solve('offdesign', design_path='grid')
print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at 10 °C outside temperature:', heat_losses.P.val)

for comp in nw.comps['object']:
    if isinstance(comp, Pipe):
        comp.set_attr(Tamb=20)

nw.solve('offdesign', design_path='grid')
print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at 20 °C outside temperature:', heat_losses.P.val)

# offdesign case: -10 °C ambient temperature

for comp in nw.comps['object']:
    if isinstance(comp, Pipe):
        comp.set_attr(Tamb=-10)

nw.solve('offdesign', design_path='grid')

print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at -10 °C outside temperature:', heat_losses.P.val)

# offdesign case: -20 °C ambient temperature

for comp in nw.comps['object']:
    if isinstance(comp, Pipe):
        comp.set_attr(Tamb=-20)

nw.solve('offdesign', design_path='grid')
print('Heat demand consumer:', heat_consumer.P.val)
print('network losses at -20 °C outside temperature:', heat_losses.P.val)
