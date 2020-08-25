# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 13:39:02 2020

@author: dsmit
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('C:/Users\Pablo\Documents\Data Challenges\Reddit\Datasets\comments_processed_sentiment.csv')



df.groupby('sentiment1')['score'].aggregate(['mean', 'sem', 'count'])

#religion
#This is interesting. There is a difference in score wwith sentiment for christian text
Christianity = df.groupby(['christian_text', 'sentiment1'])['score'].mean()

Judaism = df.groupby(['judiasm_text', 'sentiment1'])['score'].mean()

Islam = df.groupby(['islam_text', 'sentiment1'])['score'].mean()

Religion = df.groupby(['religion_text', 'sentiment1'])['score'].mean()


#try to plot it 
dfreligion = df[['score', 'christian_text', 'judiasm_text', 'islam_text', 'religion_text', 'sentiment1']]

dfreligion.loc[dfreligion['christian_text'] == True, 'christian_text'] = dfreligion['score']
dfreligion.loc[dfreligion['judiasm_text'] == True, 'judiasm_text'] = dfreligion['score']
dfreligion.loc[dfreligion['islam_text'] == True, 'islam_text'] = dfreligion['score']
dfreligion.loc[dfreligion['religion_text'] == True, 'religion_text'] = dfreligion['score']

dfreligion = dfreligion[['christian_text', 'judiasm_text', 'islam_text', 'religion_text', 'sentiment1']]
dfreligionlong = pd.melt(dfreligion, id_vars=['sentiment1'], var_name = 'group',  value_name = 'score')
dfreligionlong = dfreligionlong[dfreligionlong.score != False]
dfreligionlong['score'] = dfreligionlong.score.astype(float)

#now we  (I'm not sure these numbers add up tbh but whatever)
gr = dfreligionlong.groupby(['group', 'sentiment1'])['score'].aggregate(['mean','sem'])

fig, ax = plt.subplots()
ax.bar(x=gr.index, height=gr['mean'], yerr=gr['sem'], capsize=10)
ax.set_ylabel('Score (Standard Error)', fontsize=12)
ax.set_title("Overall")
ax.set_ylim(0,100)
plt.show()



g = sns.barplot(data = dfreligionlong, ci = 95, errwidth=.5
            ,x = 'group'
            ,y = 'score', hue = 'sentiment1',
            )
plt.title("Average Comment Score by Religion and Text Sentiment")
plt.legend(title = 'Sentiment')
g.set_xticklabels(['Christianity','Judaism','Islam', 'General Religion'])

#politics: not as interesting

Republican = df.groupby(['Republican_text', 'sentiment1'])['score'].mean()

Democrat = df.groupby(['Democrat_text', 'sentiment1'])['score'].mean()

Political = df.groupby(['Politics_text', 'sentiment1'])['score'].mean()


dfpolitics = df[['score', 'Republican_text', 'Democrat_text', 'Politics_text', 'sentiment1']]

dfpolitics.loc[dfpolitics['Republican_text'] == True, 'Republican_text'] = dfpolitics['score']
dfpolitics.loc[dfpolitics['Democrat_text'] == True, 'Democrat_text'] = dfpolitics['score']
dfpolitics.loc[dfpolitics['Politics_text'] == True, 'Politics_text'] = dfpolitics['score']


dfpolitics = dfpolitics[['Republican_text', 'Democrat_text', 'Politics_text',  'sentiment1']]
dfpoliticslong = pd.melt(dfpolitics, id_vars=['sentiment1'], var_name = 'group',  value_name = 'score')
dfpoliticslong = dfpoliticslong[dfpoliticslong.score != False]
dfpoliticslong['score'] = dfpoliticslong.score.astype(float)

sns.set()
sns.set_palette("Paired")
g = sns.barplot(data = dfpoliticslong, ci = 95, errwidth=.5
            ,x = 'group'
            ,y = 'score', hue = 'sentiment1',
            )
plt.title("Average Comment Score by Politics and Text Sentiment")
plt.legend(title = 'Sentiment')
g.set_xticklabels(['Republican','Democrat','General Politics'])


#Unsupervised Cluster Analyses
#hierarchical clustering in SciPy
#lets worth with a smaller subset of the data for speed
dfsample =  df.sample(n=50000, random_state=12)
from scipy.cluster.hierarchy import linkage, fcluster

#Z = linkage(dfsample, 'ward')
#dfsample['cluster_labels'] = fcluster(Z, 3, criterion='maxclust')





