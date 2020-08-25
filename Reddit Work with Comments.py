# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 11:23:39 2020

@author: dsmit
"""


import pandas as pd
import seaborn as sns
from scipy.stats import zscore, linregress
import matplotlib.pyplot as plt
df = pd.read_csv('C:/Users/dsmit/Documents/Data Challenges/Reddit/Datasets/politics_comments.csv')
                 
#create some categorical variables
#Create a variable for the comment scores
df['scorecat'] = pd.qcut(df['score'].rank(method='first'), 8, labels = [0, 1, 2, 3, 4, 5, 6, 7])
#Create a variable for the parent scores
df['parscorecat'] = pd.qcut(df['parent_score'].rank(method='first'), 8, labels = [0, 1, 2, 3, 4, 5, 6, 7])

#calculate the length of some variables
df['body_length'] = df['body'].str.len()
df['parent_length'] = df['parent_comment_body'].str.len()
#Lets check out a correlation heatmap for the full dataset
corr = df[['score','parent_score', 'body_length', 'parent_length']].corr()
sns.heatmap(corr, 
        xticklabels=corr.columns,
        yticklabels=corr.columns)



#this section needs work
slope, intercept, r_value, p_value, std_err = linregress(df['score'], df['parent_score'])
line = slope*df['score'] +intercept

plt.xlabel = ('comment score')
plt.scatter(df['score'], df['parent_score'])
plt.ylabel = ('comment score')
plt.plot(df['score'], line, 'r',)
plt.show()
                 

"""
First real question of the data set
Does religious text predict comment score?
"""
#Lets define some religious text (non extensive of course)
christian_text = ('god|christian|jesus|faith|church|catholic|protestant|evangelical|christ|lord|baptist|orthodox|worship|bible|lutheran')
judiasm_text = ('judaism|jew|isreal|holocaust|hebrew|passover|synagogue|yiddish|jewish|isrealite|hannukah|yom kippur')
islam_text = ('muslim|sunni|islam|islamic|arabic|islamist|muhammad|shiite')
#now, create a variable in the data set for mentions of the text. 
#The text column is the one of interest
df['christian_text'] = df['body'].str.contains(christian_text, case = False)
df['judiasm_text'] = df['body'].str.contains(judiasm_text, case = False)
df['islam_text'] = df['body'].str.contains(islam_text, case = False)
df['religion_text'] = df['body'].str.contains('religion', case = False)

df['christian_text'].sum()
df['judiasm_text'].sum()
df['islam_text'].sum()
df['religion_text'].sum()

df['score'].mean()
df.groupby('christian_text')['score'].mean()
df.groupby('judiasm_text')['score'].mean()
df.groupby('islam_text')['score'].mean()
df.groupby('religion_text')['score'].mean()


#Look at politics too
Republican_text = ('Donald|Trump|DonaldTrump|Pence|Romney|Reagan|Gop|Polanski|Republican|conservative|Mccain')
Democrat_text = ('Clinton|Hillary|Sanders|Yang|Bernie|Sanders|Biden|Obama|Barack|Democrat|Pelosi|Huckabee')
Politics_text = ('politic|politics|president|government|political|state|politicion|vote|law|governor|court|supreme|justice|police|federal|office|impeach|political party|dictator|legal|illegal|lobby')


df['Republican_text'] = df['body'].str.contains(Republican_text, case = False)
df['Democrat_text'] = df['body'].str.contains(Democrat_text, case = False)
df['Politics_text'] = df['body'].str.contains(Politics_text, case = False)

df['Politics_text'].sum()
df['Republican_text'].sum()
df['Democrat_text'].sum()

df.groupby('Republican_text')['score'].mean()
df.groupby('Democrat_text')['score'].mean()
df.groupby('Politics_text')['score'].mean()

"""Going to add a couple bar graphs to compare comment scores"""
#Add sm bars 

a = df.groupby('Republican_text')['score'].mean()[True]
b = df.groupby('Democrat_text')['score'].mean()[True]
c = df.groupby('Politics_text')['score'].mean()[True]
d = df['score'].mean()
data = (a, b, c, d)


plt.tight_layout()
plt.bar(('Republican','Democrat','Politics','Average'), data)
plt.ylabel = ('comment score')
plt.show()


a = df.groupby('christian_text')['score'].mean()[True]
b = df.groupby('judiasm_text')['score'].mean()[True]
c = df.groupby('islam_text')['score'].mean()[True]
d = df.groupby('religion_text')['score'].mean()[True]
e = df['score'].mean()
data = (a, b, c, d, e)


plt.tight_layout()
plt.bar(('Christianity','Judiasm','Islam','Religion', 'Average'), data)
plt.ylabel = ('comment score')
plt.show()



#Trying to make better plots lmao

#This part was tricky. I had to assign the column with the value of score if it was true, then make it in long form and drop
#all false values
dfpolitics = df[['score', 'Republican_text', 'Democrat_text', 'Politics_text']]
'''
a = dfpolitics.groupby('Republican_text')['score'].mean()[True]
b = dfpolitics.groupby('Democrat_text')['score'].mean()[True]
c = dfpolitics.groupby('Politics_text')['score'].mean()[True]


dfpolitics = dfpolitics[dfpolitics.Republican_text != False]
dfpolitics['Republican_text'].mean()
'''
dfpolitics.loc[dfpolitics['Republican_text'] == True, 'Republican_text'] = dfpolitics['score']
dfpolitics.loc[dfpolitics['Democrat_text'] == True, 'Democrat_text'] = dfpolitics['score']
dfpolitics.loc[dfpolitics['Politics_text'] == True, 'Politics_text'] = dfpolitics['score']


dfpolitics = dfpolitics[['Republican_text', 'Democrat_text', 'Politics_text']]
dfpoliticslong = pd.melt(dfpolitics, var_name = 'group',  value_name = 'score')
dfpoliticslong = dfpoliticslong[dfpoliticslong.score != False]
dfpoliticslong['score'] = dfpoliticslong.score.astype(float)

#now we  (I'm not sure these numbers add up tbh but whatever)
gr = dfpoliticslong.groupby('group')['score'].aggregate(['mean','sem'])

fig, ax = plt.subplots()
ax.bar(x=gr.index, height=gr['mean'], yerr=gr['sem'], capsize=10)
ax.set_ylabel('Score (Standard Error)', fontsize=12)
ax.set_title("Overall")
ax.set_ylim(0,100)
plt.show()



#Lets try something similar for the religious questions
dfreligion = df[['score', 'christian_text', 'judiasm_text', 'islam_text', 'religion_text']]

dfreligion.loc[dfreligion['christian_text'] == True, 'christian_text'] = dfreligion['score']
dfreligion.loc[dfreligion['judiasm_text'] == True, 'judiasm_text'] = dfreligion['score']
dfreligion.loc[dfreligion['islam_text'] == True, 'islam_text'] = dfreligion['score']
dfreligion.loc[dfreligion['religion_text'] == True, 'religion_text'] = dfreligion['score']

dfreligion = dfreligion[['christian_text', 'judiasm_text', 'islam_text', 'religion_text']]
dfreligionlong = pd.melt(dfreligion, var_name = 'group',  value_name = 'score')
dfreligionlong = dfreligionlong[dfreligionlong.score != False]
dfreligionlong['score'] = dfreligionlong.score.astype(float)

#now we  (I'm not sure these numbers add up tbh but whatever)
gr = dfreligionlong.groupby('group')['score'].aggregate(['mean','sem'])

fig, ax = plt.subplots()
ax.bar(x=gr.index, height=gr['mean'], yerr=gr['sem'], capsize=10)
ax.set_ylabel('Score (Standard Error)', fontsize=12)
ax.set_title("Overall")
ax.set_ylim(0,100)
plt.show()


sns.barplot(data = dfreligionlong
            ,x = 'group'
            ,y = 'score'
            )

df.to_csv(r'C:/Users/dsmit/Documents/Data Challenges/Reddit/Datasets/comments_processed.csv') 
