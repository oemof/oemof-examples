# -*- coding: utf-8 -*-
import pandas as pd

from oemof.network import Node
from oemof.solph import (Bus, Model, EnergySystem)
from oemof.solph.facades import Generator

es = EnergySystem(timeindex=pd.date_range('1/1/2012', periods=4, freq='H'))
Node.registry = es


b = Bus(label='el')

Generator(label="gen_0", Pmax=100, opex=50, bus=b)

m = Model(es)