# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 11:53:35 2022

@author: harish.b.sampath
"""
import pandas as pd
import pickle
import lightgbm

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def text_sentiment_vader(text):
    vs = analyzer.polarity_scores(text)
    return "positive" if vs.get('compound')>0 else "negative" if vs.get('compound')<0 else "neutral"
def sentimentpred(data): 
    X_test = data["lemmatized_text"].copy()
    vectorizer = pickle.load(open("vector_v6_balanced.pkl", "rb"))
    X_bow_ngram_test = vectorizer.transform(X_test).toarray()
    bst = lightgbm.Booster(model_file='model_v6_lgbm_balanced.txt')
    test_predictions = bst.predict(X_bow_ngram_test)
    s = pd.DataFrame(test_predictions,columns=[0,1,2])
    df_prediction = pd.concat([data, s], axis=1)
    df_prediction['Max'] = df_prediction[[0,1,2]].idxmax(axis=1)
    df_prediction['predictions'] = df_prediction["Max"].apply(lambda x : "Negative" if x==0 else("Neutral" if x==1 else "Positive"))
    df_prediction['Label']=df_prediction['predictions']
    return df_prediction