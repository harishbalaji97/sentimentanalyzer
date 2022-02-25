# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 11:53:35 2022

@author: harish.b.sampath
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def text_sentiment_vader(text):
    vs = analyzer.polarity_scores(text)
    return "positive" if vs.get('compound')>0 else "negative" if vs.get('compound')<0 else "neutral"
def sentimentpred(df): 
    predictions_vader = df['Text'].map(lambda x : text_sentiment_vader(x))
    df['Label'] = predictions_vader
    return(df)