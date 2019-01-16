# -*- coding: utf-8 -*-

from oemof.network import Node, Component, Bus, Edge

n1 = Node(label='n1')

n2 = Node(label='n2', inputs={n1: Edge()})

# Is there a simpler / smater way to do this?
buses = {b.label: b for b in [Bus(label='b{}'.format(i)) for i in range(3)]}

c1 = Component('c1')

print(c1.label)

c2 = Component(
    label='c2',
    outputs={buses['b1']: None},
    inputs={buses['b2']: None})

e = Edge(input=buses['b1'], output=buses['b2'], flow={'a': 10})

print(e)

e3 = Edge(flow={'a': 10})
e4 = Edge(flow={'b': 10})
c3 = Component(
    label='c3',
    outputs={buses['b1']: e3},
    inputs={buses['b2']: e4})
# Update edge value afterwards, updates flow value also in edge inside c3
e3.flow['a'] = 11

c4 = Component(
    label='c4')
c5 = Component(
    label='c5')
e = Edge(input=c4, output=c5, flow={'a': 10})

print(e.input, e.output)
