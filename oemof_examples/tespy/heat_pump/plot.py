#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 08:44:36 2018

@author: witte
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

T_range = [6, 9, 12, 15, 18, 21, 24]
Q_range = np.array([120e3, 140e3, 160e3, 180e3, 200e3, 220e3])

df = pd.read_csv('COP.csv', index_col=0)

colors = ['#00395b', '#74adc1', '#b54036', '#ec6707',
          '#bfbfbf', '#999999', '#010101']

fig, ax = plt.subplots()

i = 0
for T in T_range:
    plt.plot(Q_range / 200e3, df.loc[T], '-x', Color=colors[i],
             label='$T_{resvr}$ = ' + str(T) + ' °C', markersize=7,
             linewidth=2)
    i += 1

ax.set_ylabel('COP')
ax.set_xlabel('relative load')
plt.title('heat pump COP')
plt.legend(loc='lower left')
plt.ylim([0, 3.2])
plt.xlim([0, 1.2])
plt.show()

fig.savefig('COP.svg')
