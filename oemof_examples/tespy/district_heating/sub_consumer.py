import numpy as np
import pandas as pd

from tespy.components import (subsystem, splitter, merge, pipe, valve,
                              heat_exchanger_simple)
from tespy.connections import connection

from tespy.tools.helpers import TESPyComponentError


class lin_consum_open(subsystem):

    def __init__(self, label, num_consumer):

        if not isinstance(label, str):
            msg = 'Subsystem label must be of type str!'
            logging.error(msg)
            raise ValueError(msg)

        elif len([x for x in [';', ', ', '.'] if x in label]) > 0:
            msg = 'Can\'t use ' + str([';', ', ', '.']) + ' in label.'
            logging.error(msg)
            raise ValueError(msg)
        else:
            self.label = label

        if num_consumer <= 1:
            raise TESPyComponentError('Minimum number of consumers is 2.')
        else:
            self.num_consumer = num_consumer

        self.comps = {}
        self.conns = {}
        self.create_comps()
        self.create_conns()

    def create_comps(self):

        for i in range(self.num_consumer - 1):
            j = str(i)
            self.comps['feed_' + j] = pipe(self.label + '_pipe feed_' + j)
            self.comps['return_' + j] = pipe(self.label + '_pipe return_' + j)

        for i in range(self.num_consumer):
            j = str(i)
            self.comps['splitter_' + j] = splitter(self.label + '_splitter_' + j)
            self.comps['merge_' + j] = merge(self.label + '_merge_' + j)
            self.comps['consumer_' + j] = heat_exchanger_simple(self.label + '_consumer_' + j)
            self.comps['valve_' + j] = valve(self.label + '_valve_' + j)

    def create_conns(self):

        for i in range(self.num_consumer):
            j = str(i)
            if i > 0:
                self.conns['fesp_' + j] = connection(self.comps['feed_' + str(i - 1)], 'out1', self.comps['splitter_' + j], 'in1')
                self.conns['mere_' + j] = connection(self.comps['merge_' + j], 'out1', self.comps['return_' + str(i - 1)], 'in1')

            self.conns['spco_' + j] = connection(self.comps['splitter_' + j], 'out1', self.comps['consumer_' + j], 'in1')
            self.conns['cova_' + j] = connection(self.comps['consumer_' + j], 'out1', self.comps['valve_' + j], 'in1')
            self.conns['vame_' + j] = connection(self.comps['valve_' + j], 'out1', self.comps['merge_' + j], 'in2')

            if i < self.num_consumer - 1:
                self.conns['spfe_' + j] = connection(self.comps['splitter_' + j], 'out2', self.comps['feed_' + j], 'in1')
                self.conns['reme_' + j] = connection(self.comps['return_' + j], 'out1', self.comps['merge_' + j], 'in1')


class lin_consum_closed(subsystem):

    def __init__(self, label, num_consumer):

        if not isinstance(label, str):
            msg = 'Subsystem label must be of type str!'
            logging.error(msg)
            raise ValueError(msg)

        elif len([x for x in [';', ', ', '.'] if x in label]) > 0:
            msg = 'Can\'t use ' + str([';', ', ', '.']) + ' in label.'
            logging.error(msg)
            raise ValueError(msg)
        else:
            self.label = label

        if num_consumer <= 1:
            raise TESPyComponentError('Minimum number of consumers is 2.')
        else:
            self.num_consumer = num_consumer

        self.comps = {}
        self.conns = {}
        self.create_comps()
        self.create_conns()

    def create_comps(self):

        for i in range(self.num_consumer - 1):
            j = str(i)
            self.comps['splitter_' + j] = splitter(self.label + '_splitter_' + j)
            self.comps['merge_' + j] = merge(self.label + '_merge_' + j)
            self.comps['consumer_' + j] = heat_exchanger_simple(self.label + '_consumer_' + j)
            self.comps['valve_' + j] = valve(self.label + '_valve_' + j)
            self.comps['feed_' + j] = pipe(self.label + '_pipe feed_' + j)
            self.comps['return_' + j] = pipe(self.label + '_pipe return_' + j)

        j = str(i + 1)
        self.comps['consumer_' + j] = heat_exchanger_simple(self.label + '_consumer_' + j)

    def create_conns(self):

        for i in range(self.num_consumer - 1):
            j = str(i)

            if i > 0:
                self.conns['fesp_' + j] = connection(self.comps['feed_' + str(i - 1)], 'out1', self.comps['splitter_' + j], 'in1')
                self.conns['mere_' + j] = connection(self.comps['merge_' + j], 'out1', self.comps['return_' + str(i - 1)], 'in1')

            self.conns['spco_' + j] = connection(self.comps['splitter_' + j], 'out1', self.comps['consumer_' + j], 'in1')
            self.conns['cova_' + j] = connection(self.comps['consumer_' + j], 'out1', self.comps['valve_' + j], 'in1')
            self.conns['vame_' + j] = connection(self.comps['valve_' + j], 'out1', self.comps['merge_' + j], 'in2')
            self.conns['spfe_' + j] = connection(self.comps['splitter_' + j], 'out2', self.comps['feed_' + j], 'in1')
            self.conns['reme_' + j] = connection(self.comps['return_' + j], 'out1', self.comps['merge_' + j], 'in1')

        self.conns['spco_' + str(i + 1)] = connection(self.comps['feed_' + j], 'out1', self.comps['consumer_' + str(i + 1)], 'in1')
        self.conns['cova_' + str(i + 1)] = connection(self.comps['consumer_' + str(i + 1)], 'out1', self.comps['return_' + j], 'in1')

        # for easy access
        self.conns['fesp_' + str(i + 1)] = self.conns['spco_' + str(i + 1)]
        self.conns['mere_' + str(i + 1)] = self.conns['cova_' + str(i + 1)]


class fork(subsystem):

    def __init__(self, label, num_branch):

        if not isinstance(label, str):
            msg = 'Subsystem label must be of type str!'
            logging.error(msg)
            raise ValueError(msg)

        elif len([x for x in [';', ', ', '.'] if x in label]) > 0:
            msg = 'Can\'t use ' + str([';', ', ', '.']) + ' in label.'
            logging.error(msg)
            raise ValueError(msg)
        else:
            self.label = label

        if num_branch <= 1:
            raise TESPyComponentError('Minimum number of branches is 2.')
        else:
            self.num_branch = num_branch

        self.comps = {}
        self.conns = {}
        self.create_comps()
        self.create_conns()

    def create_comps(self):

        self.comps['splitter'] = splitter(self.label + '_splitter')
        self.comps['merge'] = merge(self.label + '_merge')

        for i in range(self.num_branch):
            j = str(i)
            self.comps['valve_' + j] = valve(self.label + '_valve_' + j)

    def create_conns(self):

        for i in range(self.num_branch):
            j = str(i)
            k = str(i + 1)
            self.conns['vame_' + j] = connection(self.comps['valve_' + j], 'out1', self.comps['merge'], 'in' + k)
