# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 10:06:30 2022

@author: harish.b.sampath
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition
import matplotlib.pyplot as plt
import numpy as np
import re
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split
def topicmod(df):
    # data= pd.read_csv('C:\\Users\\yellugari.gayathri\\Downloads\Email_Data.csv');
    X_train=pd.read_csv("PreprocessResult_Lemmatized_14_2_2022.csv")
    X_test = df
    X_train.drop(columns=['Unnamed: 0', 'Unnamed: 0.1','Id'],inplace=True)
    try:
        X_test.drop(columns=['Unnamed: 0','Id'],inplace=True)
    except:
        X_test=X_test
    X_train.reset_index(level=0,inplace=True)
    X_train.rename(columns={'index':'Id'},inplace=True)
    X_test.reset_index(level=0,inplace=True)
    #X_test.rename(columns={'index':'Id'},inplace=True)
    X_train["smallwords_removed"].fillna("Happy",inplace=True)
    stop_words = list(set(nltk.corpus.stopwords.words('english')))
    stop_words.extend(["pm","ce","cc","ct","se","et","ze","tu","hou","hcu","ect","let","may","ann","enron"])
    stop_words
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_df=0.65, max_features=1000, lowercase=False, ngram_range=(1,3))
    tfidf_vectors = vectorizer.fit_transform(X_train.smallwords_removed)
    clf = decomposition.NMF(n_components=10,init=None, random_state=100,max_iter=20)
    
    W1 = clf.fit_transform(tfidf_vectors)
    H1 = clf.components_
    eff=[]
    F=[]
    data=np.sort(W1.T,axis=1)
    #data.shape
    data=data[:,::-1]
    for i in range(0,data.shape[0]):
        #print(i+1,(data[i][:20].sum()/data[i][:data.shape[1]].sum())*100)
        eff.append((data[i][:20].sum()/data[i][:data.shape[1]].sum())*100)
        F.append(i+1)
    eff=pd.DataFrame({'Topic':F,'Perct':eff})
    num_words=20
    vocab = np.array(vectorizer.get_feature_names())
    top_words = lambda t: [vocab[i] for i in np.argsort(t)[:-num_words-1:-1]]
    topic_words = ([top_words(t) for t in H1])
    topics = [' '.join(t) for t in topic_words]
    Tags=pd.read_excel("Topic_Modeling_Tags.xlsx")
    Topics_Tags=pd.DataFrame.from_dict({'Id':Tags['Tag_Id'],'Topics':Tags['Topics'],'Tags':Tags['Tags-NS']})
    colnames = ["Topic" + str(i) for i in range(clf.n_components)]
    docnames = [str(i) for i in range(len(X_train.smallwords_removed))]
    df_doc_topic = pd.DataFrame(np.round(W1, 2), columns=colnames, index=docnames)
    significant_topic = np.argmax(df_doc_topic.values, axis=1)
    df_doc_topic['dominant_topic'] = significant_topic
    WHold = clf.transform(vectorizer.transform(X_test.smallwords_removed))
    colnames = ["Topic" + str(i) for i in range(clf.n_components)]
    docnames = [str(i) for i in range(len(X_test.smallwords_removed))]
    df_doc_topic_test = pd.DataFrame(np.round(WHold, 2), columns=colnames, index=docnames)
    significant_topic = np.argmax(df_doc_topic_test.values, axis=1)
    df_doc_topic_test['dominant_topic'] = significant_topic
    doc_topic=pd.DataFrame.from_dict({'dominant_topic':df_doc_topic_test['dominant_topic']})
    Final_Tag=pd.merge(left=doc_topic,right=Topics_Tags,left_on='dominant_topic',right_on='Id',how='left')
    Final_Tag.reset_index(level=0, inplace=True)
    Final_Tag.rename(columns={'index':'Tag_Id'},inplace=True)
    X_test.to_csv("X_test.csv")
    
    Final_Tag_v1=Final_Tag[['Tag_Id','Topics', 'Tags']]
    Modeling_Data=pd.merge(left=X_test,right=Final_Tag_v1,left_on='Id',right_on='Tag_Id',how='left')
    Modeling_Data=Modeling_Data.drop(columns=['Tag_Id'])
    Departments=['Finance','Finance','Operations','Operations','Operations','Procurement','HR','HR']
    topics=['Invoice & related documents','Utility & Energy trade and bill report','Feedback and reviews','Customer Support','Telecom install,upgrade and removal','Purchase, promotion & announcements','Contract, tax and other documents','Tracking Updates and Meeting Schedules']
    dep=pd.DataFrame({'Departments':Departments,'Tags_v1':topics})
    model_dep=pd.merge(left=Modeling_Data,right=dep,left_on='Tags',right_on='Tags_v1',how='left')
    model_dep.drop(columns=['Tags_v1'],inplace=True)
    model_dep.to_csv('fgkh.csv')
    return(model_dep)