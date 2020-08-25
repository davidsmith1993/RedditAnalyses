# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:51:19 2020

@author: dsmit
"""
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
nltk.download('punkt')
df = pd.read_csv('C:/Users/dsmit/Documents/Data Challenges/Reddit/Datasets/comments_processed.csv')
#lets cut down the load for the moment
#df =  df.sample(n=20, random_state=12)
#Our goal here is to conduct sentiment analyses of the comments
df = df.dropna(subset=['body'])
sid = SentimentIntensityAnalyzer()
df2 = pd.DataFrame()


for i in df['body']:
    scores = sid.polarity_scores(i)

    #for key in sorted(scores):
        #print('{0}: {1} '.format(key, scores[key]), end='')

    if scores["compound"] >= 0.05:
        df2.loc[i,'sentiment1'] = 'positive'

    elif scores["compound"] <= -0.05:
        df2.loc[i,'sentiment1'] = 'negative'
    else:
        df2.loc[i,'sentiment1'] = 'neutral'
 
df.reset_index(drop=True, inplace=True)
df2.reset_index(drop=True, inplace=True)      
df = pd.concat([df, df2], axis=1)

df.to_csv(r'C:/Users/dsmit/Documents/Data Challenges/Reddit/Datasets/comments_processed_sentiment.csv') 

#df3 = df2
