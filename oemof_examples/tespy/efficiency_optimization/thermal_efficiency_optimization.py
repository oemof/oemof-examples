from tespy.networks import Network
from tespy.components import (
    Turbine, Splitter, Merge, Condenser, Pump, Sink, Source,
    HeatExchangerSimple, Desuperheater, CycleCloser
)
from tespy.connections import Connection, Bus
from tespy.tools import document_model
from tespy.tools import logger
import logging

import pygmo as pg
import matplotlib.pyplot as plt
import numpy as np

logger.define_logging(screen_level=logging.ERROR)


class PowerPlant():
    def __init__(self):
        self.nw = Network(
            fluids=['BICUBIC::water'],
            p_unit='bar', T_unit='C', h_unit='kJ / kg',
            iterinfo=False)
        # components
        # main cycle
        eco = HeatExchangerSimple('economizer')
        eva = HeatExchangerSimple('evaporator')
        sup = HeatExchangerSimple('superheater')
        cc = CycleCloser('cycle closer')
        hpt = Turbine('high pressure turbine')
        sp1 = Splitter('splitter 1', num_out=2)
        mpt = Turbine('mid pressure turbine')
        sp2 = Splitter('splitter 2', num_out=2)
        lpt = Turbine('low pressure turbine')
        con = Condenser('condenser')
        pu1 = Pump('feed water pump')
        fwh1 = Condenser('feed water preheater 1')
        fwh2 = Condenser('feed water preheater 2')
        dsh = Desuperheater('desuperheater')
        me2 = Merge('merge2', num_in=2)
        pu2 = Pump('feed water pump 2')
        pu3 = Pump('feed water pump 3')
        me = Merge('merge', num_in=2)

        # cooling water
        cwi = Source('cooling water source')
        cwo = Sink('cooling water sink')

        # connections
        # main cycle
        cc_hpt = Connection(cc, 'out1', hpt, 'in1', label='feed steam')
        hpt_sp1 = Connection(hpt, 'out1', sp1, 'in1', label='extraction1')
        sp1_mpt = Connection(sp1, 'out1', mpt, 'in1', state='g')
        mpt_sp2 = Connection(mpt, 'out1', sp2, 'in1', label='extraction2')
        sp2_lpt = Connection(sp2, 'out1', lpt, 'in1')
        lpt_con = Connection(lpt, 'out1', con, 'in1')
        con_pu1 = Connection(con, 'out1', pu1, 'in1')
        pu1_fwh1 = Connection(pu1, 'out1', fwh1, 'in2')
        fwh1_me = Connection(fwh1, 'out2', me, 'in1', state='l')
        me_fwh2 = Connection(me, 'out1', fwh2, 'in2', state='l')
        fwh2_dsh = Connection(fwh2, 'out2', dsh, 'in2', state='l')
        dsh_me2 = Connection(dsh, 'out2', me2, 'in1')
        me2_eco = Connection(me2, 'out1', eco, 'in1', state='l')
        eco_eva = Connection(eco, 'out1', eva, 'in1')
        eva_sup = Connection(eva, 'out1', sup, 'in1')
        sup_cc = Connection(sup, 'out1', cc, 'in1')

        self.nw.add_conns(cc_hpt, hpt_sp1, sp1_mpt, mpt_sp2, sp2_lpt,
                          lpt_con, con_pu1, pu1_fwh1, fwh1_me, me_fwh2,
                          fwh2_dsh, dsh_me2, me2_eco, eco_eva, eva_sup, sup_cc)

        # cooling water
        cwi_con = Connection(cwi, 'out1', con, 'in2')
        con_cwo = Connection(con, 'out2', cwo, 'in1')

        self.nw.add_conns(cwi_con, con_cwo)

        # preheating
        sp1_dsh = Connection(sp1, 'out2', dsh, 'in1')
        dsh_fwh2 = Connection(dsh, 'out1', fwh2, 'in1')
        fwh2_pu2 = Connection(fwh2, 'out1', pu2, 'in1')
        pu2_me2 = Connection(pu2, 'out1', me2, 'in2')

        sp2_fwh1 = Connection(sp2, 'out2', fwh1, 'in1')
        fwh1_pu3 = Connection(fwh1, 'out1', pu3, 'in1')
        pu3_me = Connection(pu3, 'out1', me, 'in2')

        self.nw.add_conns(sp1_dsh, dsh_fwh2, fwh2_pu2, pu2_me2,
                          sp2_fwh1, fwh1_pu3, pu3_me)

        # busses
        # power bus
        self.power = Bus('power')
        self.power.add_comps(
            {'comp': hpt, 'char': -1}, {'comp': mpt, 'char': -1},
            {'comp': lpt, 'char': -1}, {'comp': pu1, 'char': -1},
            {'comp': pu2, 'char': -1}, {'comp': pu3, 'char': -1})

        # heating bus
        self.heat = Bus('heat')
        self.heat.add_comps(
            {'comp': eco, 'char': 1}, {'comp': eva, 'char': 1},
            {'comp': sup, 'char': 1})

        self.nw.add_busses(self.power, self.heat)

        # parametrization
        # components
        hpt.set_attr(eta_s=0.9)
        mpt.set_attr(eta_s=0.9)
        lpt.set_attr(eta_s=0.9)

        pu1.set_attr(eta_s=0.8)
        pu2.set_attr(eta_s=0.8)
        pu3.set_attr(eta_s=0.8)

        eco.set_attr(pr=0.99)
        eva.set_attr(pr=0.99)
        sup.set_attr(pr=0.99)

        con.set_attr(pr1=1, pr2=0.99, ttd_u=5)
        fwh1.set_attr(pr1=1, pr2=0.99, ttd_u=5)
        fwh2.set_attr(pr1=1, pr2=0.99, ttd_u=5)
        dsh.set_attr(pr1=0.99, pr2=0.99)

        # connections
        eco_eva.set_attr(x=0)
        eva_sup.set_attr(x=1)

        cc_hpt.set_attr(m=200, T=650, p=100, fluid={'water': 1})
        hpt_sp1.set_attr(p=20)
        mpt_sp2.set_attr(p=3)
        lpt_con.set_attr(p=0.05)

        cwi_con.set_attr(T=20, p=10, fluid={'water': 1})

        # test run
        self.nw.solve('design')
        document_model(self.nw)

    def calculate_efficiency(self, x):
        # set extraction pressure
        self.nw.get_conn('extraction1').set_attr(p=x[0])
        self.nw.get_conn('extraction2').set_attr(p=x[1])

        self.nw.solve('design')

        for cp in self.nw.comps['object']:
            if isinstance(cp, Condenser) or isinstance(cp, Desuperheater):
                if cp.Q.val > 0:
                    return np.nan
            elif isinstance(cp, Pump):
                if cp.P.val < 0:
                    return np.nan
            elif isinstance(cp, Turbine):
                if cp.P.val > 0:
                    return np.nan

        if self.nw.res[-1] > 1e-3 or self.nw.lin_dep:
            return np.nan
        else:
            return self.nw.busses['power'].P.val / self.nw.busses['heat'].P.val


class OptimizationProblem():

    def fitness(self, x):
        f1 = 1 / self.model.calculate_efficiency(x)
        ci1 = -x[0] + x[1]
        return [f1, ci1]

    def get_nobj(self):
        """Return number of objectives."""
        return 1

    # equality constraints
    def get_nec(self):
        return 0

    # inequality constraints
    def get_nic(self):
        return 1

    def get_bounds(self):
        """Return bounds of decision variables."""
        return ([1, 1], [40, 40])


optimize = OptimizationProblem()
optimize.model = PowerPlant()
prob = pg.problem(optimize)
num_gen = 15

pop = pg.population(prob, size=10)
algo = pg.algorithm(pg.ihs(gen=num_gen))

result = {'champion': [], 'efficiency': [], 'generation': [],
          'extraction 1': [], 'extraction 2': []}

for gen in range(num_gen):
    result["generation"].append(gen)
    result["champion"].append(100/pop.champion_f[0])

    decision_var = pop.get_x()
    for pressure in decision_var:
        result['extraction 1'].append(pressure[0])
        result['extraction 2'].append(pressure[1])

    fitness = pop.get_f()
    for efficiency in fitness:
        result['efficiency'].append(100/efficiency[0])

    print()
    print('Evolution: {}'.format(gen))
    print('Efficiency: {} %'.format(round(100 / pop.champion_f[0], 4)))
    pop = algo.evolve(pop)

print()
print('Efficiency: {} %'.format(round(100 / pop.champion_f[0], 4)))
print('Extraction 1: {} bar'.format(round(pop.champion_x[0], 4)))
print('Extraction 2: {} bar'.format(round(pop.champion_x[1], 4)))


# scatter plot
cm = plt.cm.get_cmap('RdYlBu')
sc = plt.scatter(result['extraction 2'], result['extraction 1'], linewidth=0.25,
                 c=result['efficiency'], cmap=cm, alpha=0.5, edgecolors='black')
plt.scatter(pop.champion_x[1], pop.champion_x[0], marker='x', linewidth=1,
            c='red')
plt.annotate('Optimum', xy=(pop.champion_x[1], pop.champion_x[0]),
             xytext=(pop.champion_x[1]+3, pop.champion_x[0]+3),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',
                             color='red')
            )
plt.ylabel('$p_{extraction, 1}$ in bar')
plt.xlabel('$p_{extraction, 2}$ in bar')
plt.colorbar(sc, label='Cycle efficiency (%)')
plt.savefig("scatterplot.svg")
plt.show()
