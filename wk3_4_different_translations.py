# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:54:44 2020

@author: Daria
"""
import pandas as pd 
from collections import Counter
import matplotlib.pyplot as plt


def count_words_fast(text): 
    text = text.lower() 
    skips = [".", ",", ";", ":", "'", '"', "\n", "!", "?", "(", ")"] 
    for ch in skips: 
        text = text.replace(ch, "") 
    word_counts = Counter(text.split(" ")) 
    return word_counts

def word_stats(word_counts): 
    num_unique = len(word_counts) 
    counts = word_counts.values() 
    return (num_unique, counts)

hamlets=pd.read_csv(r'C:/Users/Daria/Documents/PythonScripts/asset-v1_HarvardX+PH526x+2T2019+type@asset+block@hamlets.csv', index_col=0)
language, text = hamlets.iloc[2]
def summarize_text(language, text):
    
    counted_text = count_words_fast(text)
    
    data = pd.DataFrame({
        "word": list(counted_text.keys()),
        "count": list(counted_text.values()),      
    })
    
    data['length']=data['word'].apply(len)
    
    data['frequency'] = ['frequent' if x >10 else('infrequent' if 1<x<=10 else 'uniq') for x in data['count']]
    
    print(data.groupby('frequency').count())
    
    #subdata['mean']=subdata.groupby(by=['frequency'])['length'].mean()
    
    sub_data = pd.DataFrame({
        "language": language,
        "frequency": ["frequent","infrequent","unique"],
        "mean_word_length": data.groupby(by = "frequency")["length"].mean(),
        "num_words": data.groupby(by = "frequency").size()
    })
    #print (sub_data)
    return sub_data

grouped_data = pd.DataFrame(columns = ["language", "frequency", "mean_word_length", "num_words"])

for i in range(hamlets.shape[0]):
    language, text = hamlets.iloc[i]
    sub_data = summarize_text(language, text)
    grouped_data = grouped_data.append(sub_data)

colors = {"Portuguese": "green", "English": "blue", "German": "red"}
markers = {"frequent": "o","infrequent": "s", "unique": "^"}

for i in range(grouped_data.shape[0]):
    row = grouped_data.iloc[i]
    plt.plot(row.mean_word_length, row.num_words,
        marker=markers[row.frequency],
        color = colors[row.language],
        markersize = 10
    )

color_legend = []
marker_legend = []
for color in colors:
    color_legend.append(
        plt.plot([], [],
        color=colors[color],
        marker="o",
        label = color, markersize = 10, linestyle="None")
    )
for marker in markers:
    marker_legend.append(
        plt.plot([], [],
        color="k",
        marker=markers[marker],
        label = marker, markersize = 10, linestyle="None")
    )
plt.legend(numpoints=1, loc = "upper left")

plt.xlabel("Mean Word Length")
plt.ylabel("Number of Words")