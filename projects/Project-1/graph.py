# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 19:18:45 2021

@author: Vamsi
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import itertools
import networkx as nx
import string
import re
from nltk import bigrams
from nltk.corpus import  stopwords as sw
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('stopwords')
nltk.download('punkt')
stopwords = set(sw.words('english'))

df = pd.read_json('messages.json')

media = (df['media'].apply(pd.Series))['webpage'].apply(pd.Series)

data = media[['id', 'title' ,'description']]

data = data.dropna()

data['title'] = data['title'].apply( lambda text: re.sub('[^A-Za-z0-9 ]+', '', text))
data['description'] = data['description'].apply( lambda text: re.sub('[^A-Za-z0-9 ]+', '', text))
data['title'] = data['title'].apply( lambda text: ' '.join([word for word in word_tokenize(text) if not word in stopwords and len(word)>2 ]))
data['description'] = data['description'].apply( lambda text: ' '.join([word for word in word_tokenize(text) if not word in stopwords and len(word)>2 ]))
data['title'] = data['title'].apply(lambda x: x.upper())
data['description'] = data['description'].apply(lambda x: x.upper())

title_bigram = []
for title in data['title']:
    title_bigram.append((list(bigrams(title.split()))))

bigrams = list(itertools.chain(*title_bigram))
bigram_counts = Counter(bigrams)
bigram_df = pd.DataFrame(bigram_counts.most_common(250), columns = ['bigram','count'])

d = bigram_df.set_index('bigram').T.to_dict('records')
G = nx.Graph()

for k, v in d[0].items():
    G.add_edge(k[0], k[1], weight=(v * 10))

fig, ax = plt.subplots(figsize=(50, 40))

pos = nx.spring_layout(G, k=2)

nx.draw_networkx(G, pos,
                 font_size=16,
                 width=3,
                 edge_color='black',
                 node_color='blue',
                 with_labels = False,
                 ax=ax)

for key, value in pos.items():
    x, y = value[0]+.13, value[1]+.03
    ax.text(x, y,
            s=key,
            bbox=dict(facecolor='red', alpha=0.25),
            horizontalalignment='center', fontsize=13)
    
plt.show()


def drawHistogram(dict,title,xlabel,ylabel):
    plt.bar(dict.keys(),dict.values(),color='g')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=90)
    plt.show()
    
    
pos = nx.spring_layout(G,scale=10,k=0.25)
nx.draw(G,pos,with_labels=True,node_size=1200,node_shape='s',alpha=0.5,font_size=16)
plt.show() #Shows the window containing the graph
degreeCentrality=nx.algorithms.centrality.degree_centrality(G)
betweeness=nx.algorithms.centrality.betweenness_centrality(G)
closeness=nx.algorithms.centrality.closeness_centrality(G)
df_measures=pd.DataFrame([degreeCentrality,betweeness,closeness])
df_measures=df_measures.rename(index={0:'DegreeCentrality',1:'Betweenness',2:'Closeness'}).transpose()
drawHistogram(degreeCentrality,"Degree Centrality Histogram","Screen Name","Degree Centrality")
drawHistogram(betweeness, "Betweeness Histogram", "Screen Name","Betweeness")
drawHistogram(closeness, "Closeness Histogram", "Screen Name","Closeness")