# %matplotlib inline
import config ##custom config file to load API Keys

import csv
import pandas as pd
import numpy as np
import time
from collections import defaultdict

import networkx as nx
import matplotlib.pyplot as plt

# import plotly
# import plotly.graph_objs as go
# import plotly.plotly as py

from datetime import datetime

# Ignore matplotlib warnings
import warnings
# warnings.filterwarnings("../ignore")

# plotly.tools.set_credentials_file(username=config.plotly_username, api_key=config.plotly_api_key)



startTime = time.time()



# searchTweet = "#ONBudget"
# searchTweet = "#pakistan_Zindabad"
searchTweet = "#OntarioTech"


df = pd.read_csv('data/'+searchTweet+'_users.csv')
dfT = pd.read_csv('data/'+searchTweet+'_tweets.csv')

# print(df)



G = nx.DiGraph()

for ind in range ( len(dfT['Username']) ):
    G.add_node(dfT['Username'][ind])

# print("nodesssssss",len(dfT['Username']) )

for ind in range ( len(df['source']) ):
    # print (df['source'][ind],df['target'][ind])
    G.add_edge(df['source'][ind],df['target'][ind])


# print("isolated---",list(nx.isolates(G)))
# G.remove_nodes_from(list(nx.isolates(G)))


### OLDER
# G = nx.from_pandas_edgelist(df, source='source', target='target',edge_attr=None, create_using=None)
# nx.draw(G, with_labels=True, node_size=500, node_color="skyblue",
#                 node_shape="o", font_size=5, arrowstyle='>', arrowsize=10,
#                 font_color="black", font_weight="bold", width=1, edge_color="grey",
#                 pos=nx.spring_layout(G,k=0.15,iterations=20),dist=None, weight=0.5, scale=1, center=None, dim=2)
#                 # pos=nx.shell_layout(G))
#                 # pos=nx.spectral_layout(G))
#                 # pos=nx.kamada_kawai_layout(G))
#                 # pos=nx.spring_layout(G))
#
#
#
# print("nodes---",len(G.nodes()))
#
#
# plt.draw()
# plt.show()



# import matplotlib as mpl
# pos = nx.layout.spring_layout(G,k=1.50,iterations=150)
# nodes = nx.draw_networkx_nodes(G, pos, node_size=200, node_color='skyblue', with_labels=True,
#                                 font_size=5, font_color="black", font_weight="bold")
# edges = nx.draw_networkx_edges(G, pos, node_size=200, arrowstyle='->',
#                                arrowsize=10, edge_color="grey", with_labels=True, width=0.5)
#
# nx.draw_networkx_labels(G, pos, font_size=8,font_color="black", font_weight="bold")
# plt.draw()
# plt.show()



# print("nx.average_neighbor_degree(G) - ",nx.average_neighbor_degree(G))
# print("nx.k_nearest_neighbors(G) - ",nx.k_nearest_neighbors(G))
# print("nx.average_degree_connectivity(G) - ",nx.average_degree_connectivity(G))
# print("nx.average_clustering(G) - ",nx.average_clustering(G))
# print("nx.betweenness_centrality(G) - ",nx.betweenness_centrality(G))


# print("G.degree() - ",G.degree())
# print("G.in_degree() - ",G.in_degree())
# print("G.out_degree() - ",G.out_degree())





degN = []
deg = []
import operator
for k,v in sorted(dict(G.degree()).items(), key=operator.itemgetter(1)):
    degN.append(k)
    deg.append(v)
INdeg = []
for k,v in sorted(dict(G.in_degree()).items(), key=operator.itemgetter(1)):
    INdeg.append(v)
OUTdeg = []
for k,v in sorted(dict(G.out_degree()).items(), key=operator.itemgetter(1)):
    OUTdeg.append(v)




btwn = nx.betweenness_centrality(G)

btwnN = []
btwnV = []
for k in sorted(btwn):
    btwnN.append(k)
    btwnV.append(btwn[k])


avgDeg = nx.average_degree_connectivity(G)
degK = []
degV = []
for k in sorted(avgDeg):
    degK.append(k)
    degV.append(avgDeg[k])



close = nx.closeness_centrality(G, u=None, distance=None, wf_improved=True)

closeN = []
closeV = []
for k in sorted(close):
    closeN.append(k)
    closeV.append(close[k])






import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def plot(data,degreetype):
    """ Plot Distribution """
    plt.plot(range(len(data)),data,'bo')
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Freq')
    plt.xlabel('Degree')
    plt.savefig('filename' + '_' + degreetype + '_distribution.eps')
    plt.clf()

    """ Plot CDF """
    s = float(data.sum())
    cdf = data.cumsum(0)/s
    plt.plot(range(len(cdf)),cdf,'bo')
    plt.xscale('log')
    plt.ylim([0,1])
    plt.ylabel('CDF')
    plt.xlabel('Degree')
    plt.savefig('filename' + '_' + degreetype + '_cdf.eps')
    plt.clf()

    """ Plot CCDF """
    ccdf = 1-cdf
    plt.plot(range(len(ccdf)),ccdf,'bo')
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim([0,1])
    plt.ylabel('CCDF')
    plt.xlabel('Degree')
    plt.savefig('filename' + '_' + degreetype + '_ccdf.eps')
    plt.clf()



# edgelist_file = sys.argv[1]

""" Load graph """
# G = nx.read_edgelist(edgelist_file, nodetype=int, create_using=nx.DiGraph())

""" To sparse adjacency matrix """
M = nx.to_scipy_sparse_matrix(G)

indegrees = M.sum(0).A[0]
outdegrees = M.sum(1).T.A[0]
indegree_distribution = np.bincount(indegrees)
outdegree_distribution = np.bincount(outdegrees)

plot(indegree_distribution, 'indegree')
plot(outdegree_distribution, 'outdegree')



# import plotly
# import plotly.graph_objs as go
# import plotly.plotly as py
#
# trace0 = go.Scatter(
#     x = closeN,
#     y = closeV,
#     mode = 'lines',
#     name = 'lines'
# )
#
#
# layout = go.Layout(
#     title=go.layout.Title(
#         text='Closeness Centrality (Wasserman-Faust )',
#         xref='paper',x=0),
#     xaxis=go.layout.XAxis(
#         title=go.layout.xaxis.Title(
#             text='Nodes',
#             font=dict(family='Arial, sans-serif',size=8,color='#7f7f7f'))),
#     yaxis=go.layout.YAxis(
#         title=go.layout.yaxis.Title(
#             text='Closeness Centrality',
#             font=dict(family='Arial, sans-serif',size=18,color='#7f7f7f'))))
#
# data = [trace0]
# fig = go.Figure(data=data, layout=layout)
# py.plot(fig, filename='closeness_centrality')




#
# import networkx as nx
# import community
#
# Gr = G.to_undirected()
#
# part = community.best_partition(Gr)
# values = [part.get(node) for node in Gr.nodes()]
#
# # nx.draw_spring(Gr,cmap = plt.get_cmap('jet'), node_color = values, node_size=200, with_labels=True,
#                     # font_size=8, font_color="black", font_weight="bold",edge_color="grey",
#                     # arrowstyle='->',arrowsize=10, width=1)
# pos = nx.layout.spring_layout(Gr,k=1.60,iterations=150)
# nodes = nx.draw_networkx_nodes(Gr, pos, node_size=200, cmap = plt.get_cmap('jet'), node_color = values, with_labels=True,
#                                 font_size=5, font_color="black", font_weight="bold")
# edges = nx.draw_networkx_edges(Gr, pos, node_size=200, arrowstyle='->',
#                                arrowsize=10, edge_color="grey", with_labels=True, width=0.5)
#
# nx.draw_networkx_labels(Gr, pos, font_size=8,font_color="black", font_weight="bold")
# # nx.draw_networkx_labels(Gr, pos, font_size=8,font_color="black", font_weight="bold")
# plt.draw()
# plt.show()




# import plotly
# import plotly.graph_objs as go
# import plotly.plotly as py
#
# trace0 = go.Scatter(
#     x = degN,
#     y = deg,
#     mode = 'lines',
#     name = 'Degree',
#     line = dict(
#         color = ('rgb(22, 96, 167)'),
#         width = 4,)
# )
# trace1 = go.Scatter(
#     x = degN,
#     y = INdeg,
#     mode = 'lines',
#     name = 'In Degree',
#     line = dict(
#         color = ('rgb(205, 12, 24)'),
#         width = 4,
#         dash = 'dash')
# )
# trace2 = go.Scatter(
#     x = degN,
#     y = OUTdeg,
#     mode = 'lines',
#     name = 'Out Degree',
#     line = dict(
#         color = ('rgb(12, 205, 24)'),
#         width = 4,
#         dash = 'dash')
# )
# layout = go.Layout(
#     title=go.layout.Title(
#         text='Degree Distribution',
#         xref='paper',x=0),
#     xaxis=go.layout.XAxis(
#         title=go.layout.xaxis.Title(
#             text='Nodes',
#             font=dict(family='Arial, sans-serif',size=8,color='#7f7f7f'))),
#     yaxis=go.layout.YAxis(
#         title=go.layout.yaxis.Title(
#             text='Degree (k)',
#             font=dict(family='Arial, sans-serif',size=18,color='#7f7f7f'))))
#
# data = [trace0, trace1, trace2]
# fig = go.Figure(data=data, layout=layout)
# py.plot(fig, filename='Degree Distribution')




# import plotly
# import plotly.graph_objs as go
# import plotly.plotly as py
#
# trace0 = go.Scatter(
#     x = btwnN,
#     y = btwnV,
#     mode = 'lines',
#     name = 'lines'
# )
#
#
# layout = go.Layout(
#     title=go.layout.Title(
#         text='Betweenness Centrality',
#         xref='paper',x=0),
#     xaxis=go.layout.XAxis(
#         title=go.layout.xaxis.Title(
#             text='Nodes',
#             font=dict(family='Arial, sans-serif',size=8,color='#7f7f7f'))),
#     yaxis=go.layout.YAxis(
#         title=go.layout.yaxis.Title(
#             text='Betweenness Centrality',
#             font=dict(family='Arial, sans-serif',size=18,color='#7f7f7f'))))
#
# data = [trace0]
# fig = go.Figure(data=data, layout=layout)
# py.plot(fig, filename='average_degree_connectivity')






#
# import plotly
# import plotly.graph_objs as go
# import plotly.plotly as py
#
# trace0 = go.Scatter(
#     x = degK,
#     y = degV,
#     mode = 'lines',
#     name = 'lines'
# )
#
#
# layout = go.Layout(
#     title=go.layout.Title(
#         text='Average Degree Connectivity',
#         xref='paper',
#         x=0
#     ),
#     xaxis=go.layout.XAxis(
#         title=go.layout.xaxis.Title(
#             text='k (# of Degree)',
#             font=dict(
#                 family='Courier New, monospace',
#                 size=18,
#                 color='#7f7f7f'
#             )
#         )
#     ),
#     yaxis=go.layout.YAxis(
#         title=go.layout.yaxis.Title(
#             text='Average Degree Connectivity',
#             font=dict(
#                 family='Courier New, monospace',
#                 size=18,
#                 color='#7f7f7f'
#             )
#         )
#     )
# )
#
# data = [trace0]
# fig = go.Figure(data=data, layout=layout)
#
# py.plot(fig, filename='average_degree_connectivity')









# graphs = list(nx.strongly_connected_component_subgraphs(G))
# nx.draw(graphs)
# plt.draw()
# plt.show()


#
# import json
# import flask
# from networkx.readwrite import json_graph
#
# for n in G:
#     G.node[n]['name'] = n
#
# d = json_graph.node_link_data(G)
# json.dump(d, open('data/force/force.json','w'))
# print('Wrote node-link JSON data to force/force.json')
#
# # Serve the file over http to allow for cross origin requests
# app = flask.Flask(__name__, static_folder="data/force/")
#
# @app.route('/')
# def static_proxy():
#     return app.send_static_file('force.html')
#
# print('\nGo to http://localhost:8000 to see the example\n')
# app.run(port=8000)






endTime = time.time()

print("running time= ",endTime-startTime)
