# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 13:21:52 2020

@author: dsmit
"""


import pandas as pd
import praw

reddit = praw.Reddit(client_id="2srEoGpH-ElTzw",
                     client_secret="iAoRJCVrTvCRQD90MBRPRW0UQzg",
                     user_agent="Python data scrap for analyses (by /u/oaky180)",
                     username="", #removed for public use
                     password="")

#Pulling comments from 3 subreddits that I think could be interesting

comments=[]
subreddit_list = ['Politics', 'worldnews', 'news']
for subreddits in subreddit_list:
    hot = reddit.subreddit(subreddits).top(limit=100, time_filter='month')
    sub = subreddits
    for submission in hot:
        print(submission.title)
        submission.comments.replace_more(limit=10)
        for comment in submission.comments.list():
            if type(comment.parent()) == praw.models.reddit.submission.Submission:
                comment.parent().body = 'NaN'
                comment.parent().score = 'NaN'
            comments.append([sub, submission.title, comment.author, comment.score, comment.body, comment.created_utc, comment.parent().body, comment.parent().score])
        
        
        
comments = pd.DataFrame(comments,columns=['subreddit','submission_title', 'author', 'score', 'body', 'time', 'parent_comment_body', 'parent_score'])
comments.to_csv(r'C:/Users/dsmit/Documents/Data Challenges/Reddit/Datasets/politics_comments.csv') 
