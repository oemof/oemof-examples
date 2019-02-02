import numpy as np
import pandas as pd

from tespy import subsys, cmp, con
from tespy.tools.helpers import TESPyComponentError


class lin_consum_open(subsys.subsystem):

    def __init__(self, label, num_consumer, **kwargs):

        if not isinstance(label, str):
            raise TESPyComponentError('Subsystem label must be of type str!')

        elif len([x for x in [';', ', ', '.'] if x in label]) > 0:
            raise TESPyComponentError('Can\'t use ' + str([';', ', ', '.']) + ' ',
                                   'in label.')
        else:
            self.label = label

        if num_consumer <= 1:
            raise TESPyComponentError('Minimum number of consumers is 2.')
        else:
            self.num_consumer = num_consumer

        for key in self.attr():
            self.__dict__.update({key: np.nan})
            self.__dict__.update({key + '_set': False})

        self.subsys_init()
        self.set_attr(**kwargs)

    def attr(self):

        values = ([n for n in subsys.subsystem.attr(self) if
                   n != 'num_i' and n != 'num_o'])

        for i in range(self.num_consumer):
            j = str(i)
            values += ['pr' + j, 'Q' + j]  # 'pr' + i -> pr0
            values += ['T_in' + j]
            values += ['T_out' + j]

            if i < self.num_consumer - 1:
                j = str(i)
                values += ['pr_pf' + j, 'Q_pf' + j, 'ks_pf' + j, 'D_pf' + j,
                           'L_pf' + j, 'dT_pf' + j]
                values += ['pr_pb' + j, 'Q_pb' + j, 'ks_pb' + j, 'D_pb' + j,
                           'L_pb' + j, 'dT_pb' + j]

        values += ['Tamb']

        return values

    def create_comps(self):

        self.num_i = 2
        self.num_o = 2
        self.inlet = cmp.subsys_interface(label=self.label + '_inlet',
                                          num_inter=self.num_i)
        self.outlet = cmp.subsys_interface(label=self.label + '_outlet',
                                           num_inter=self.num_o)

        self.splitter = []
        self.merge = []
        self.heat_ex = []
        self.valve = []
        self.pipe_feed = []
        self.pipe_back = []

        for i in range(self.num_consumer - 1):
            j = str(i)
            self.pipe_feed += [cmp.pipe(label=self.label + '_pipe feed_' + j,
                                        offdesign=['kA'])]
            self.pipe_back += [cmp.pipe(label=self.label + '_pipe back_' + j,
                                        offdesign=['kA'])]

        for i in range(self.num_consumer):
            j = str(i)
            self.splitter += [cmp.splitter(label=self.label +
                                           '_splitter_' + j)]
            self.merge += [cmp.merge(label=self.label + '_merge_' + j)]
            self.valve += [cmp.valve(label=self.label + '_valve_' + j,
                                       mode='man')]
            self.heat_ex += [cmp.heat_exchanger_simple(label=self.label +
                                                       '_heat exchanger_' + j,
                                                       mode='man')]

    def set_comps(self):

        for i in range(self.num_consumer):
            j = str(i)
            self.heat_ex[i].set_attr(pr=self.get_attr('pr' + j))
            self.heat_ex[i].set_attr(Q=self.get_attr('Q' + j))

        for i in range(self.num_consumer - 1):
            j = str(i)
            self.pipe_feed[i].set_attr(pr=self.get_attr('pr_pf' + j))
            self.pipe_feed[i].set_attr(Q=self.get_attr('Q_pf' + j))
            self.pipe_feed[i].set_attr(ks=self.get_attr('ks_pf' + j))
            self.pipe_feed[i].set_attr(D=self.get_attr('D_pf' + j))
            self.pipe_feed[i].set_attr(L=self.get_attr('L_pf' + j))

            self.pipe_back[i].set_attr(pr=self.get_attr('pr_pb' + j))
            self.pipe_back[i].set_attr(Q=self.get_attr('Q_pb' + j))
            self.pipe_back[i].set_attr(ks=self.get_attr('ks_pb' + j))
            self.pipe_back[i].set_attr(D=self.get_attr('D_pb' + j))
            self.pipe_back[i].set_attr(L=self.get_attr('L_pb' + j))

        self.pipe_back[i].set_attr(Tamb=self.Tamb)
        self.pipe_feed[i].set_attr(Tamb=self.Tamb)

    def create_conns(self):

        self.conns = []

        for i in range(self.num_consumer):
            if i == 0:
                self.conns += [con.connection(self.inlet, 'out1',
                                              self.splitter[i], 'in1')]
                self.conns += [con.connection(self.merge[i], 'out1',
                                              self.outlet, 'in1')]
            else:
                self.conns += [con.connection(self.pipe_feed[i - 1], 'out1',
                                              self.splitter[i], 'in1')]
                self.conns += [con.connection(self.merge[i], 'out1',
                                              self.pipe_back[i - 1], 'in1')]

            self.conns += [con.connection(self.splitter[i], 'out1',
                                          self.heat_ex[i], 'in1')]
            self.conns += [con.connection(self.heat_ex[i], 'out1',
                                          self.valve[i], 'in1')]
            self.conns += [con.connection(self.valve[i], 'out1',
                                          self.merge[i], 'in2')]

            if i == self.num_consumer - 1:

                self.conns += [con.connection(self.splitter[i], 'out2',
                                              self.outlet, 'in2')]
                self.conns += [con.connection(self.inlet, 'out2',
                                              self.merge[i], 'in1')]
            else:

                self.conns += [con.connection(self.splitter[i], 'out2',
                                              self.pipe_feed[i], 'in1',
                                              design=['T'])]
                self.conns += [con.connection(self.pipe_back[i], 'out1',
                                              self.merge[i], 'in1',
                                              design=['T'])]

    def set_conns(self):

        if not hasattr(self, 'nw'):
            self.create_network()

        i = 0
        for he in self.heat_ex:
            j = str(i)

            inconn = self.nw.conns.loc[self.nw.conns['t'].isin([he]) &
                                       self.nw.conns['t_id'].isin(['in1'])].index[0]
            outconn = self.nw.conns.loc[self.nw.conns['s'].isin([he]) &
                                        self.nw.conns['s_id'].isin(['out1'])].index[0]

            inconn.set_attr(T=self.get_attr('T_in' + j))
            outconn.set_attr(T=self.get_attr('T_out' + j))
            i += 1

        i = 0
        for pipe in self.pipe_feed:
            j = str(i)

            inconn = self.nw.conns.loc[self.nw.conns['t'].isin([pipe]) &
                                       self.nw.conns['t_id'].isin(['in1'])].index[0]
            outconn = self.nw.conns.loc[self.nw.conns['s'].isin([pipe]) &
                                        self.nw.conns['s_id'].isin(['out1'])].index[0]

            if self.get_attr('dT_pf' + j + '_set'):
                inconn.set_attr(T=con.ref(outconn, 1,
                                self.get_attr('dT_pf' + j)))
            else:
                inconn.set_attr(T=np.nan)
            i += 1

        i = 0
        for pipe in self.pipe_back:
            j = str(i)

            inconn = self.nw.conns.loc[self.nw.conns['t'].isin([pipe]) &
                                       self.nw.conns['t_id'].isin(['in1'])].index[0]
            outconn = self.nw.conns.loc[self.nw.conns['s'].isin([pipe]) &
                                        self.nw.conns['s_id'].isin(['out1'])].index[0]

            if self.get_attr('dT_pb' + j + '_set'):
                outconn.set_attr(T=con.ref(inconn, 1,
                                 -self.get_attr('dT_pb' + j)))
            else:
                outconn.set_attr(T=np.nan)
            i += 1


class lin_consum_closed(subsys.subsystem):

    def __init__(self, label, num_consumer, **kwargs):

        if not isinstance(label, str):
            raise TESPyComponentError('Subsystem label must be of type str!')

        elif len([x for x in [';', ', ', '.'] if x in label]) > 0:
            raise TESPyComponentError('Can\'t use ' + str([';', ', ', '.']) + ' ',
                                   'in label.')
        else:
            self.label = label

        if num_consumer <= 1:
            raise TESPyComponentError('Minimum number of consumers is 2.')
        else:
            self.num_consumer = num_consumer

        for key in self.attr():
            self.__dict__.update({key: np.nan})
            self.__dict__.update({key + '_set': False})

        self.subsys_init()
        self.set_attr(**kwargs)

    def attr(self):

        values = ([n for n in subsys.subsystem.attr(self) if
                   n != 'num_i' and n != 'num_o'])

        for i in range(self.num_consumer):
            j = str(i)
            values += ['pr' + j, 'Q' + j]  # 'pr' + i -> pr0
            values += ['T_in' + j]
            values += ['T_out' + j]

            if i < self.num_consumer - 1:
                j = str(i)
                values += ['pr_pf' + j, 'Q_pf' + j, 'ks_pf' + j, 'D_pf' + j,
                           'L_pf' + j, 'dT_pf' + j]
                values += ['pr_pb' + j, 'Q_pb' + j, 'ks_pb' + j, 'D_pb' + j,
                           'L_pb' + j, 'dT_pb' + j]

        values += ['Tamb']

        return values

    def create_comps(self):

        self.num_i = 1
        self.num_o = 1
        self.inlet = cmp.subsys_interface(label=self.label + '_inlet',
                                          num_inter=self.num_i)
        self.outlet = cmp.subsys_interface(label=self.label + '_outlet',
                                           num_inter=self.num_o)

        self.splitter = []
        self.merge = []
        self.heat_ex = []
        self.valve = []
        self.pipe_feed = []
        self.pipe_back = []
        for i in range(self.num_consumer - 1):
            j = str(i)
            self.splitter += [cmp.splitter(label=self.label +
                                           '_splitter_' + j)]
            self.merge += [cmp.merge(label=self.label + '_merge_' + j)]
            self.heat_ex += [cmp.heat_exchanger_simple(label=self.label +
                                                       '_heat exchanger_' + j,
                                                       mode='man')]
            self.valve += [cmp.valve(label=self.label + '_valve_' + j,
                                       mode='man')]
            self.pipe_feed += [cmp.pipe(label=self.label + '_pipe feed_' + j,
                                        offdesign=['kA'])]
            self.pipe_back += [cmp.pipe(label=self.label + '_pipe back_' + j,
                                        offdesign=['kA'])]

        self.heat_ex += [cmp.heat_exchanger_simple(label=self.label +
                                                   '_heat exchanger_' +
                                                   str(i + 1), mode='man')]

    def set_comps(self):

        for i in range(self.num_consumer):
            j = str(i)
            self.heat_ex[i].set_attr(pr=self.get_attr('pr' + j))
            self.heat_ex[i].set_attr(Q=self.get_attr('Q' + j))

        for i in range(self.num_consumer - 1):
            j = str(i)
            self.pipe_feed[i].set_attr(pr=self.get_attr('pr_pf' + j))
            self.pipe_feed[i].set_attr(Q=self.get_attr('Q_pf' + j))
            self.pipe_feed[i].set_attr(ks=self.get_attr('ks_pf' + j))
            self.pipe_feed[i].set_attr(D=self.get_attr('D_pf' + j))
            self.pipe_feed[i].set_attr(L=self.get_attr('L_pf' + j))

            self.pipe_back[i].set_attr(pr=self.get_attr('pr_pb' + j))
            self.pipe_back[i].set_attr(Q=self.get_attr('Q_pb' + j))
            self.pipe_back[i].set_attr(ks=self.get_attr('ks_pb' + j))
            self.pipe_back[i].set_attr(D=self.get_attr('D_pb' + j))
            self.pipe_back[i].set_attr(L=self.get_attr('L_pb' + j))

        self.pipe_back[i].set_attr(Tamb=self.Tamb)
        self.pipe_feed[i].set_attr(Tamb=self.Tamb)

    def create_conns(self):

        self.conns = []

        for i in range(self.num_consumer - 1):
            if i == 0:
                self.conns += [con.connection(self.inlet, 'out1',
                                              self.splitter[i], 'in1')]
                self.conns += [con.connection(self.merge[i], 'out1',
                                              self.outlet, 'in1')]
            else:
                self.conns += [con.connection(self.pipe_feed[i - 1], 'out1',
                                              self.splitter[i], 'in1')]
                self.conns += [con.connection(self.merge[i], 'out1',
                                              self.pipe_back[i - 1], 'in1')]

            self.conns += [con.connection(self.splitter[i], 'out1',
                                          self.heat_ex[i], 'in1')]
            self.conns += [con.connection(self.heat_ex[i], 'out1',
                                          self.valve[i], 'in1')]
            self.conns += [con.connection(self.valve[i], 'out1',
                                          self.merge[i], 'in2')]
            self.conns += [con.connection(self.splitter[i], 'out2',
                                          self.pipe_feed[i], 'in1',
                                          design=['T'])]
            self.conns += [con.connection(self.pipe_back[i], 'out1',
                                          self.merge[i], 'in1',
                                          design=['T'])]

        self.conns += [con.connection(self.pipe_feed[i], 'out1',
                                      self.heat_ex[i + 1], 'in1')]
        self.conns += [con.connection(self.heat_ex[i + 1], 'out1',
                                      self.pipe_back[i], 'in1')]

    def set_conns(self):

        if not hasattr(self, 'nw'):
            self.create_network()

        i = 0
        for he in self.heat_ex:
            j = str(i)

            inconn = self.nw.conns.loc[self.nw.conns['t'].isin([he]) &
                                       self.nw.conns['t_id'].isin(['in1'])].index[0]
            outconn = self.nw.conns.loc[self.nw.conns['s'].isin([he]) &
                                        self.nw.conns['s_id'].isin(['out1'])].index[0]

            inconn.set_attr(T=self.get_attr('T_in' + j))
            outconn.set_attr(T=self.get_attr('T_out' + j))
            i += 1

        i = 0
        for pipe in self.pipe_feed:
            j = str(i)

            inconn = self.nw.conns.loc[self.nw.conns['t'].isin([pipe]) &
                                       self.nw.conns['t_id'].isin(['in1'])].index[0]
            outconn = self.nw.conns.loc[self.nw.conns['s'].isin([pipe]) &
                                        self.nw.conns['s_id'].isin(['out1'])].index[0]

            if self.get_attr('dT_pf' + j + '_set'):
                inconn.set_attr(T=con.ref(outconn, 1,
                                self.get_attr('dT_pf' + j)))
            else:
                inconn.set_attr(T=np.nan)
            i += 1

        i = 0
        for pipe in self.pipe_back:
            j = str(i)

            inconn = self.nw.conns.loc[self.nw.conns['t'].isin([pipe]) &
                                       self.nw.conns['t_id'].isin(['in1'])].index[0]
            outconn = self.nw.conns.loc[self.nw.conns['s'].isin([pipe]) &
                                        self.nw.conns['s_id'].isin(['out1'])].index[0]

            if self.get_attr('dT_pb' + j + '_set'):
                outconn.set_attr(T=con.ref(inconn, 1,
                                 -self.get_attr('dT_pb' + j)))
            else:
                outconn.set_attr(T=np.nan)
            i += 1


class fork(subsys.subsystem):

    def __init__(self, label, num_branch, **kwargs):

        if not isinstance(label, str):
            raise TESPyComponentError('Subsystem label must be of type str!')

        elif len([x for x in [';', ', ', '.'] if x in label]) > 0:
            raise TESPyComponentError('Can\'t use ' + str([';', ', ', '.']) + ' ',
                                   'in label.')
        else:
            self.label = label

        if num_branch <= 1:
            raise TESPyComponentError('Minimum number of branches is 2.')
        else:
            self.num_branch = num_branch

        for key in self.attr():
            self.__dict__.update({key: np.nan})
            self.__dict__.update({key + '_set': False})

        self.subsys_init()
        self.set_attr(**kwargs)

    def attr(self):

        values = ([n for n in subsys.subsystem.attr(self) if
                   n != 'num_i' and n != 'num_o'])

        return values

    def create_comps(self):

        self.inlet = cmp.subsys_interface(label=self.label + '_inlet',
                                          num_inter=self.num_branch + 1)
        self.outlet = cmp.subsys_interface(label=self.label + '_outlet',
                                           num_inter=self.num_branch + 1)

        self.splitter = cmp.splitter(label=self.label + '_splitter')
        self.merge = cmp.merge(label=self.label + '_merge')
        self.valve = []

        for i in range(self.num_branch):
            j = str(i)
            self.valve += [cmp.valve(label=self.label + '_valve_' + j,
                                       mode='man')]

    def create_conns(self):

        self.conns = []

        self.conns += [con.connection(self.inlet, 'out1',
                                      self.splitter, 'in1')]
        self.conns += [con.connection(self.merge, 'out1',
                                      self.outlet, 'in1')]

        for i in range(self.num_branch):
            j = str(i + 1)
            k = str(i + 2)
            self.conns += [con.connection(self.splitter, 'out' + j,
                                          self.outlet, 'in' + k)]
            self.conns += [con.connection(self.inlet, 'out' + k,
                                          self.valve[i], 'in1')]
            self.conns += [con.connection(self.valve[i], 'out1',
                                          self.merge, 'in' + j)]
