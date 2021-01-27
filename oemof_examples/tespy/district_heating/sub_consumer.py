# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from tespy.components import (Subsystem, Splitter, Merge, Pipe, Valve,
                              HeatExchangerSimple)
from tespy.connections import Connection

from tespy.tools.helpers import TESPyComponentError


class LinConsumOpen(Subsystem):

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
            self.comps['feed_' + j] = Pipe(self.label + '_pipe feed_' + j)
            self.comps['return_' + j] = Pipe(self.label + '_pipe return_' + j)

        for i in range(self.num_consumer):
            j = str(i)
            self.comps['splitter_' + j] = Splitter(self.label + '_splitter_' + j)
            self.comps['merge_' + j] = Merge(self.label + '_merge_' + j)
            self.comps['consumer_' + j] = HeatExchangerSimple(self.label + '_consumer_' + j)
            self.comps['valve_' + j] = Valve(self.label + '_valve_' + j)

    def create_conns(self):

        for i in range(self.num_consumer):
            j = str(i)
            if i > 0:
                self.conns['fesp_' + j] = Connection(self.comps['feed_' + str(i - 1)], 'out1', self.comps['splitter_' + j], 'in1')
                self.conns['mere_' + j] = Connection(self.comps['merge_' + j], 'out1', self.comps['return_' + str(i - 1)], 'in1')

            self.conns['spco_' + j] = Connection(self.comps['splitter_' + j], 'out1', self.comps['consumer_' + j], 'in1')
            self.conns['cova_' + j] = Connection(self.comps['consumer_' + j], 'out1', self.comps['valve_' + j], 'in1')
            self.conns['vame_' + j] = Connection(self.comps['valve_' + j], 'out1', self.comps['merge_' + j], 'in2')

            if i < self.num_consumer - 1:
                self.conns['spfe_' + j] = Connection(self.comps['splitter_' + j], 'out2', self.comps['feed_' + j], 'in1')
                self.conns['reme_' + j] = Connection(self.comps['return_' + j], 'out1', self.comps['merge_' + j], 'in1')


class LinConsumClosed(Subsystem):

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
            self.comps['splitter_' + j] = Splitter(self.label + '_splitter_' + j)
            self.comps['merge_' + j] = Merge(self.label + '_merge_' + j)
            self.comps['consumer_' + j] = HeatExchangerSimple(self.label + '_consumer_' + j)
            self.comps['valve_' + j] = Valve(self.label + '_valve_' + j)
            self.comps['feed_' + j] = Pipe(self.label + '_pipe feed_' + j)
            self.comps['return_' + j] = Pipe(self.label + '_pipe return_' + j)

        j = str(i + 1)
        self.comps['consumer_' + j] = HeatExchangerSimple(self.label + '_consumer_' + j)

    def create_conns(self):

        for i in range(self.num_consumer - 1):
            j = str(i)

            if i > 0:
                self.conns['fesp_' + j] = Connection(self.comps['feed_' + str(i - 1)], 'out1', self.comps['splitter_' + j], 'in1')
                self.conns['mere_' + j] = Connection(self.comps['merge_' + j], 'out1', self.comps['return_' + str(i - 1)], 'in1')

            self.conns['spco_' + j] = Connection(self.comps['splitter_' + j], 'out1', self.comps['consumer_' + j], 'in1')
            self.conns['cova_' + j] = Connection(self.comps['consumer_' + j], 'out1', self.comps['valve_' + j], 'in1')
            self.conns['vame_' + j] = Connection(self.comps['valve_' + j], 'out1', self.comps['merge_' + j], 'in2')
            self.conns['spfe_' + j] = Connection(self.comps['splitter_' + j], 'out2', self.comps['feed_' + j], 'in1')
            self.conns['reme_' + j] = Connection(self.comps['return_' + j], 'out1', self.comps['merge_' + j], 'in1')

        self.conns['spco_' + str(i + 1)] = Connection(self.comps['feed_' + j], 'out1', self.comps['consumer_' + str(i + 1)], 'in1')
        self.conns['cova_' + str(i + 1)] = Connection(self.comps['consumer_' + str(i + 1)], 'out1', self.comps['return_' + j], 'in1')


class Fork(Subsystem):

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

        self.comps['splitter'] = Splitter(self.label + '_splitter')
        self.comps['merge'] = Merge(self.label + '_merge')

        for i in range(self.num_branch):
            j = str(i)
            self.comps['valve_' + j] = Valve(self.label + '_valve_' + j)

    def create_conns(self):

        for i in range(self.num_branch):
            j = str(i)
            k = str(i + 1)
            self.conns['vame_' + j] = Connection(self.comps['valve_' + j], 'out1', self.comps['merge'], 'in' + k)
