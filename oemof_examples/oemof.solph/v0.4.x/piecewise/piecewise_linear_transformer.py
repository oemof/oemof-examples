import pandas as pd
from oemof.solph import (Sink, Source, Bus, Flow, Model,
                         EnergySystem)

import oemof.outputlib as outputlib
import oemof.solph as solph
import numpy as np
import matplotlib.pyplot as plt

solver = 'cbc'

# set timeindex and create data
periods = 20
datetimeindex = pd.date_range('1/1/2019', periods=periods, freq='H')
step = 5
demand = np.arange(0, step*periods, step)

# set up EnergySystem
energysystem = EnergySystem(timeindex=datetimeindex)
b_gas = Bus(label='gas', balanced=False)
b_el = Bus(label='electricity')
energysystem.add(b_gas, b_el)
energysystem.add(Source(label='shortage', outputs={b_el: Flow(variable_costs=1e6)}))
energysystem.add(Sink(label='demand', inputs={b_el: Flow(
    nominal_value=1, fix=demand, fixed=0)}))

conv_func = lambda x: 0.01 * x**2
in_breakpoints = np.arange(0, 110, 25)

pwltf = solph.custom.PiecewiseLinearTransformer(
    label='pwltf',
    inputs={b_gas: solph.Flow(
    nominal_value=100,
    variable_costs=1)},
    outputs={b_el: solph.Flow()},
    in_breakpoints=in_breakpoints,
    conversion_function=conv_func,
    pw_repn='CC') # 'CC', 'DCC', 'INC', 'MC'

# DCC TODO: Solve problem in outputlib with DCC

energysystem.add(pwltf)

# create and solve the optimization model
optimization_model = Model(energysystem)
optimization_model.write('/home/jann/Desktop/my_model.lp', io_options={'symbolic_solver_labels': True})
optimization_model.solve(solver=solver,
                         solve_kwargs={'tee': False, 'keepfiles': False})

results = outputlib.processing.results(optimization_model)
string_results = outputlib.processing.convert_keys_to_strings(results)
df = outputlib.processing.create_dataframe(optimization_model)
sequences = {k:v['sequences'] for k, v in string_results.items()}
df = pd.concat(sequences, axis=1)
df[('efficiency', None, None)] = df[('pwltf', 'electricity', 'flow')].divide(df[('gas', 'pwltf', 'flow')])

def linearized_func(func, x_break, x):
    y_break=func(x_break)
    condlist = [(x_l <= x)&(x < x_u) for x_l, x_u in zip(x_break[:-1], x_break[1:])]
    funclist = []
    for i in range(len(x_break)-1):
        b = y_break[i]
        a = (y_break[i+1] - y_break[i]) * 1/((x_break[i+1] - x_break[i]))
        funclist.append(lambda x, b=b, a=a, i=i: b + a*(x-x_break[i]))
    return np.piecewise(x, condlist, funclist)

production_expected = linearized_func(conv_func, in_breakpoints, df[('gas', 'pwltf')]['flow'].values)
production_modeled = df[('pwltf', 'electricity')]['flow'].values
print(np.allclose(production_modeled, production_expected))

fig, ax = plt.subplots()
ax.scatter(df[('gas', 'pwltf', 'flow')], df[('pwltf', 'electricity','flow')], marker='x', c='r', s=40)
x = in_breakpoints
y = conv_func(x)
ax.plot(x, y, marker='+', markersize=15)
ax.set_ylabel('electricity output')
ax.set_xlabel('gas input')
plt.show()
