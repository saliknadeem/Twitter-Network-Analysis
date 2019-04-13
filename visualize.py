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
searchTweet = "#pakistan_Zindabad"



df = pd.read_csv('data/'+searchTweet+'_users.csv')
dfT = pd.read_csv('data/'+searchTweet+'_tweets.csv')

print(df)


G = nx.from_pandas_edgelist(df, source='source', target='target',edge_attr=None, create_using=None)


for user in dfT['Username']:
    G.add_node(user)


nx.draw(G, with_labels=True, node_size=500, node_color="skyblue",
                node_shape="o", alpha=0.5, font_size=10,
                font_color="grey", font_weight="bold", width=2, edge_color="grey",
                pos=nx.kamada_kawai_layout(G),dist=None, weight='weight', scale=1, center=None, dim=20)
                # pos=nx.shell_layout(G))
                # pos=nx.spectral_layout(G))
                # pos=nx.spring_layout(G))


print("nodes---",len(G.nodes()))


plt.show()





import json
import flask
from networkx.readwrite import json_graph

for n in G:
    G.node[n]['name'] = n

d = json_graph.node_link_data(G)
json.dump(d, open('data/force/force.json','w'))
print('Wrote node-link JSON data to force/force.json')

# Serve the file over http to allow for cross origin requests
app = flask.Flask(__name__, static_folder="data/force/")

@app.route('/')
def static_proxy():
    return app.send_static_file('force.html')

print('\nGo to http://localhost:8000 to see the example\n')
app.run(port=8000)






endTime = time.time()

print("running time= ",endTime-startTime)
