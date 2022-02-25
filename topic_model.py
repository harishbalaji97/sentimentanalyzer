# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 14:01:32 2022

@author: sandhya.selvamani
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition
import matplotlib.pyplot as plt
import numpy as np
import re
import nltk
from nltk.stem.porter import PorterStemmer
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
nltk.download('punkt')

def TP_NMF(df):
    stop_words = list(set(nltk.corpus.stopwords.words('english')))
    stop_words.extend(["pm","ce","cc","ct","se","et","ze","tu","hou","hcu","ect","let","may","ann","enron"])
    df['Sender_Email_Type'][10:20]=df[ 'Sender_Email_Type'][10:20].replace('gmail','yahoo')
    df["smallwords_removed"].fillna("Happy",inplace=True)
    X_train, X_hold = train_test_split(df, test_size=0.3, random_state=111)
    train=X_train['lemmatized_text'].copy()
    train=pd.DataFrame(train)
    train=train.reset_index(drop=True)
    stop_words = list(set(nltk.corpus.stopwords.words('english')))
    stop_words.extend(["pm","ce","cc","ct","se","et","ze","tu","hou","hcu","ect","let","may","ann","enron"])
    
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_df=0.65, max_features=1000, lowercase=False, ngram_range=(1,3))
    tfidf_vectors = vectorizer.fit_transform(X_train.smallwords_removed)
    clf = decomposition.NMF(n_components=10,init=None, random_state=100,max_iter=20)

    W1 = clf.fit_transform(tfidf_vectors)
    H1 = clf.components_
    print(clf.reconstruction_err_)
    data=np.sort(W1.T,axis=1)
    eff=[]
    F=[]
    for i in range(0,data.shape[0]):
        print(i,(data[i][:10].sum()/data[i][:352].sum())*100)
        eff.append((data[i][:10].sum()/data[i][:352].sum())*100)
        F.append(i)
    eff=pd.DataFrame({'Topic':F,'Perct':eff})
    WHold = clf.transform(vectorizer.transform(X_hold.Text[:10]))
    colnames = ["Topic" + str(i) for i in range(clf.n_components)]
    docnames = ["Doc" + str(i) for i in range(len(X_hold[:10].Text))]
    df_doc_topic = pd.DataFrame(np.round(WHold, 2), columns=colnames, index=docnames)
    significant_topic = np.argmax(df_doc_topic.values, axis=1)
    df_doc_topic['max_topic']= df_doc_topic.idxmax(axis=1)
    df_doc_topic['dominant_topic'] = significant_topic
    return df_doc_topic