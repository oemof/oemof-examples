from tespy.connections import connection
from tespy.components import source, sink, pipe
from tespy.networks import network

import numpy as np
from matplotlib import pyplot as plt

nw = network(['water'], p_unit='bar', T_unit='C', h_unit='kJ / kg')

# %% components
pi = pipe('pipe')
si = sink('sink')
so = source('source')

# %% connections

a = connection(so, 'out1', pi, 'in1')
b = connection(pi, 'out1', si, 'in1')

nw.add_conns(a, b)

# %% connection parameters

a.set_attr(h=40, fluid={'water': 1}, p=1, m=10)


# %% component parameters

pi.set_attr(ks=1e-4, L=100, D='var', Q=0)

# %% solve
nw.set_attr(iterinfo=False)

# specify different pressure ratios for the pipe, calculate the diameter required

for pr in np.linspace(0.95, 0.999, 10):
    pi.set_attr(pr=pr)
    nw.solve(mode='design')
    print('Pressure ratio: ' + str(round(pr, 3)) + ', diameter: ' + str(round(pi.D.val * 1000, 0)))
