# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 19:18:45 2021

@author: Vamsi
"""

import pandas as pd
import json
import matplotlib.pyplot as plt

import nltk
from nltk import bigrams
from nltk.corpus import  stopwords as sw
from nltk.tokenize import word_tokenize

import itertools
import networkx
import re
from collections import Counter

nltk.download('stopwords')
nltk.download('punkt')
stopwords = set(sw.words('english'))

df = pd.read_json('messages.json')

media = (df['media'].apply(pd.Series))['webpage'].apply(pd.Series)

data = media[['id', 'title' ,'description']]

data = data.dropna()

data['title']       = data['title'].apply( lambda text: re.sub('[^A-Za-z0-9 ]+', '', text))
data['description'] = data['description'].apply( lambda text: re.sub('[^A-Za-z0-9 ]+', '', text))
data['title']       = data['title'].apply( lambda text: ' '.join([word for word in word_tokenize(text) if not word in stopwords and len(word)>2 ]))
data['description'] = data['description'].apply( lambda text: ' '.join([word for word in word_tokenize(text) if not word in stopwords and len(word)>2 ]))
data['title']       = data['title'].apply(lambda x: x.upper())
data['description'] = data['description'].apply(lambda x: x.upper())

network_title = []
for title in data['title']:  network_title.append((list(bigrams(title.split()))))

bigram_graph = list(itertools.chain(*network_title))
bigram_graph_counts = Counter(bigram_graph)
bigram_graph_df = pd.DataFrame(bigram_graph_counts.most_common(250), columns = ['bigram','count'])

d = bigram_graph_df.set_index('bigram').T.to_dict('records')
graph = networkx.Graph()

for k, v in d[0].items():  graph.add_edge(k[0], k[1], weight=(v * 15))


degreeCentrality   = networkx.algorithms.centrality.degree_centrality(graph)
plt.bar(degreeCentrality.keys(),degreeCentrality.values(),color='y')
plt.xlabel("words")
plt.ylabel("Degree centrality")
plt.title("Degree Distribution")
plt.xticks(rotation=90)
plt.show()

betweenness         = networkx.algorithms.centrality.betweenness_centrality(graph)
plt.bar(betweenness.keys(),betweenness.values(),color='y')
plt.xlabel("words")
plt.ylabel("Betweenness")
plt.title("Betweenness")
plt.xticks(rotation=90)
plt.show()

closeness          = networkx.algorithms.centrality.closeness_centrality(graph)
plt.bar(closeness.keys(),closeness.values(),color='y')
plt.xlabel("words")
plt.ylabel("Closeness")
plt.title("Closeness")
plt.xticks(rotation=90)
plt.show()

fig, axis = plt.subplots(figsize=(100, 80))
position = networkx.spring_layout(graph, k=3)
networkx.draw_networkx(graph, position, font_size=30, width=6, edge_color='grey', node_color='green', with_labels = False, ax = axis)
for key, value in position.items():
    x, y = value[0], value[1]
    axis.text(x, y, s=key, bbox=dict(facecolor='yellow', alpha = 0.25), horizontalalignment='center', fontsize = 30)
plt.show()

measures = pd.DataFrame([degreeCentrality, betweenness, closeness])
measures = measures.rename(index = {0: 'Degree Centrality', 1: 'Betweenness', 2: 'Closeness'}).transpose()
measures.to_csv('measures_results.csv')