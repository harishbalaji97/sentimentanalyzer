# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 11:55:09 2022

@author: harish.b.sampath
"""

import pandas as pd
import os
import re
import text2emotion as te
import unicodedata
import nltk
nltk.download('stopwords')

# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize

from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = nltk.stem.WordNetLemmatizer()

from nltk.stem.porter import PorterStemmer

def extract_emotion(data):
    data["emotion"] = data["whitespace_removed"].apply(lambda x : te.get_emotion(x))
    return data

def emotion(data):
    data["emotion"] = data["whitespace_removed"].apply(lambda x : te.get_emotion(x))
    return data