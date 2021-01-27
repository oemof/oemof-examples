# -*- coding: utf-8 -*-
from tespy.connections import Connection
from tespy.components import Source, Sink, Pipe
from tespy.networks import Network
from tespy.tools import document_model

import numpy as np
from matplotlib import pyplot as plt

nw = Network(['water'], p_unit='bar', T_unit='C', h_unit='kJ / kg')

# %% components
pi = Pipe('pipe')
si = Sink('sink')
so = Source('source')

# %% connections

a = Connection(so, 'out1', pi, 'in1')
b = Connection(pi, 'out1', si, 'in1')

nw.add_conns(a, b)

# %% connection parameters

a.set_attr(h=40, fluid={'water': 1}, p=1, m=10)


# %% component parameters

pi.set_attr(ks=1e-5, L=100, D='var', Q=0)

# %% solve
nw.set_attr(iterinfo=False)

# specify different pressure ratios for the pipe,
# calculate the diameter required

for pr in np.linspace(0.9, 0.999, 10):
    pi.set_attr(pr=pr)
    nw.solve(mode='design')
    print('Pressure ratio: ' + str(round(pr, 3)) +
          ', diameter: ' + str(round(pi.D.val * 1000, 0)) + ' mm.')

document_model(nw)
