#!/usr/bin/env python
# coding: utf-8

# In[3]:


import networkx as nx
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB


# In[4]:


def cal_flow(G, T, sink_nodes):
    vertices = G.nodes()
    print("Vertices - ", vertices)

    inflow = dict(G.nodes().data("weight"))
    print("Inflow - ", inflow)

    edges = G.edges()
    print("Edges - ", edges)

    capacity={}
    cost={}
    for i,j in edges:
        d = G.edges[i,j]
        capacity[i,j] = d['capacity']
        cost[i,j] = d['length']

    print("Capacity - ", capacity)
    print("Cost - ", cost)

    # create model
    m = gp.Model("Maximum Flow Problem")

    # define variables
    flow=gp.tupledict({})

    for i, j in edges:
        flow.update(m.addVars(i, j, range(cost[i,j],T+1), ub=capacity[i,j], name = "flow"))

    holdover_var = m.addVars(vertices, range(1,T+1), name = "holdover_var")

    dummy=gp.tupledict({})
    for i in vertices:
        dummy.update(m.addVars(i, lb=0, ub=inflow[i], name = "dummy"))

    # flow conservation 
    for i in vertices:
        for t in range(1,T):
            exp = holdover_var[i, t] + flow.sum('*', i, t) - holdover_var[i, t+1]
            for a,b in edges:
                if a==i:
                    exp -= flow.sum(a, b, t + cost[a , b])
            m.addConstr(exp==0,"node")

    # special case when t=0
    for i in vertices:
        expr = dummy[i] - holdover_var[i, 1]
        for x,y in edges:
            if x==i:
                expr += flow[x, y, cost[x,y]]
        m.addConstr(expr==0)

    #special case when t=T
    m.addConstrs(flow.sum('*', j , T) + holdover_var[j, T] == 0 for j in vertices if j not in sink_nodes)

    # objective maximize
    obj=dummy.sum()
    m.setObjective(obj, GRB.MAXIMIZE)

    m.optimize()

    for v in m.getVars():
        print(v.VarName, v.X)

    print('Obj: ',m.ObjVal)    
    


# In[6]:


graph = nx.read_gml("graph.gml")
time = 5
sink_nodes = ['C','O']
cal_flow(graph, time, sink_nodes)


# In[ ]:




