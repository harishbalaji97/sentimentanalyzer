
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition
import matplotlib.pyplot as plt
import numpy as np
import re
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition
import matplotlib.pyplot as plt
import numpy as np
import re
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split

##BASIC PREPROCESS RELATED LIBRARIES
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from collections import Counter
import warnings
warnings.filterwarnings('ignore')
##NLP LIBRARIES - NLTK USED IN BUILDING NLP PIPE LINE
import nltk
nltk.download('stopwords')
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = nltk.stem.WordNetLemmatizer()
from nltk.stem.porter import PorterStemmer
import urllib.request as url
from bs4 import BeautifulSoup as bs
import re
import requests
from sklearn.preprocessing import LabelEncoder
import unicodedata

def scrub_words(outtext):
    # Replace \xao characters in text -
    # \xa0 is actually non-breaking space in Latin1 (ISO 8859-1), also chr(160).  
    outtext = str(outtext)
    outtext = re.sub('\xa0', ' ', outtext)
    outtext = re.sub("(\\W|\\d)", ' ', outtext) # Replace non ascii and digits
    outtext = re.sub('\n(\w*?)[\s]', '', outtext)    # Replace new line characters and following text untill space
    outtext = re.sub("<.*?>", ' ', outtext)    # Remove html markup
    outtext = re.sub(r'\\xa0',' ',outtext)    #outtext = re.sub('\n',' ',outtext)
    outtext = re.sub(r'\\n',' ',outtext)    #outtext = re.sub(r'\xa0',' ',outtext)
    outtext = re.sub(r'_',' ',outtext)
    outtext = re.sub(r'  ',' ',outtext)
    outtext = re.sub('[^a-zA-z\s]','',outtext)
    outtext = re.sub(' +', ' ',outtext)
    " ".join(outtext.strip())
    return outtext
  
def remove_accented_chars(text):
    """Remove non-ASCII characters from list of tokenized words"""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

def text_cleaning(scrapped_raw_text):   
    cleaned_text = scrub_words(scrapped_raw_text)
    return cleaned_text
  
def text_processing(text):     
    stop_words = stopwords.words('english')
    tokens = [token for token in word_tokenize(text) if not token in stop_words]
    tokens = [token for token in word_tokenize(text) if len(token)>2]
    tokens = [token.lower() for token in tokens]
    ##LEMMATIZING WORDS
    tokens = [wordnet_lemmatizer.lemmatize(token) for token in tokens]
    tokens = [token for token in word_tokenize(text) if len(token)>2]
    text = ' '.join(tokens)
    return text   

def topicmod(Test):
    # data= pd.read_csv('C:\\Users\\yellugari.gayathri\\Downloads\Email_Data.csv');
    df = pd.read_csv("Train_V1_yelp")
    #Test=pd.read_csv("Yelp_Test.csv")
    df["Industry"].unique(),df["Categories_1"].unique()
    df = df.loc[df["Industry"]=="Active Life"]
    df= df.loc[df["Categories_1"]!="Shopping"]
    df['Text'] = df['Text'].apply(str)
    df["label"] = df["stars"].apply(lambda x : "Negative" if 1<=x<=2 else ("Neutral" if x==3 else "Positive") )
    y = LabelEncoder().fit_transform(df['label'])

    #Remove Stop words 
    stop_words = stopwords.words('english')
    df['clean_text'] = df['Text'].apply(text_cleaning)
    df['clean_text'] = df['clean_text'].apply(text_processing)
    #Train data
    X_train=df.reset_index().copy()
    X_train.drop(columns=['Unnamed: 0','index'],inplace=True)
    X_train.reset_index(inplace=True)
    X_train.rename(columns={'index':'Id'},inplace=True)

    #Modeling
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_df=0.9, max_features=1000, lowercase=False, ngram_range=(1,3))
    tfidf_vectors = vectorizer.fit_transform(X_train.clean_text)
    clf = decomposition.NMF(n_components=5, random_state=111,init=None,max_iter=10)
    W1 = clf.fit_transform(tfidf_vectors)
    H1 = clf.components_

    #Topic Extraction
    num_words=40
    vocab = np.array(vectorizer.get_feature_names())
    top_words = lambda t: [vocab[i] for i in np.argsort(t)[:-num_words-1:-1]]
    topic_words = ([top_words(t) for t in H1])
    topics = [' '.join(t) for t in topic_words]

    #Dominant topic for data
    colnames = ["Topic" + str(i) for i in range(clf.n_components)]
    docnames = [str(i) for i in range(len(X_train.clean_text))]
    df_doc_topic = pd.DataFrame(np.round(W1, 2), columns=colnames, index=docnames)
    significant_topic = np.argmax(df_doc_topic.values, axis=1)
    df_doc_topic['dominant_topic'] = significant_topic

    #Mapping dominant topic,Topics names to main data frame
    Tags=pd.read_excel("Tags_2.xlsx")
    Topics_Tags=pd.DataFrame.from_dict({'Id':Tags['Id'],'Topics':Tags['Topics'],'Tags':Tags['Tags'],'Department':Tags['Department']})
    doc_topic_train=pd.DataFrame.from_dict({'dominant_topic':df_doc_topic['dominant_topic']})
    Train_Tag=pd.merge(left=doc_topic_train,right=Topics_Tags,left_on='dominant_topic',right_on='Id',how='left')
    Train_Tag.reset_index(level=0, inplace=True)
    Train_Tag.rename(columns={'index':'Tag_Id'},inplace=True)
    Train_Tag.to_csv('sdf.csv')
    Train_Tag=Train_Tag[['Tag_Id','Topics', 'Tags','Department']]
    Train_Data=pd.merge(left=X_train,right=Train_Tag,left_on='Id',right_on='Tag_Id',how='left')
    Train_Data.drop(columns=['Tag_Id'],inplace=True)

    #Testing Data
    # Test modeling
    WHold = clf.transform(vectorizer.transform(Test.Text))
    #dominant topic
    colnames = ["Topic" + str(i) for i in range(clf.n_components)]
    docnames = [str(i) for i in range(len(Test.Text))]
    df_doc_topic_test = pd.DataFrame(np.round(WHold, 2), columns=colnames, index=docnames)
    significant_topic = np.argmax(df_doc_topic_test.values, axis=1)
    df_doc_topic_test['dominant_topic'] = significant_topic
    #Mapping
    doc_topic=pd.DataFrame.from_dict({'dominant_topic':df_doc_topic_test['dominant_topic']})
    Final_Tag=pd.merge(left=doc_topic,right=Topics_Tags,left_on='dominant_topic',right_on='Id',how='left')
    Final_Tag.reset_index(level=0, inplace=True)
    Final_Tag.rename(columns={'index':'Tag_Id'},inplace=True)
    Final_Tag_v1=Final_Tag[['Tag_Id','Topics', 'Tags','Department']]
    #Final Data Frame
    Modeling_Data=pd.merge(left=Test,right=Final_Tag_v1,left_on='Id',right_on='Tag_Id',how='left')
    Modeling_Data=Modeling_Data.drop(columns=['Tag_Id'])
    Modeling_Data.to_csv("fgk_1.csv")
    return Modeling_Data