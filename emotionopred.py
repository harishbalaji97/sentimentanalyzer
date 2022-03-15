import pandas as pd
import ast
from nrclex import NRCLex
import numpy as np


def emotion(df):
    df['stars']=np.nan
    for i in np.arange(0,len(df)):
        if df['Label'][i]=="Positive":
            df['stars'][i]=5
        elif df['Label'][i]=="Negative":
            df['stars'][i]=1
        elif df['Label'][i]=='Neutral':
            df['stars'][i]=3
    ##finding top 10 emotions using NRCLex
    df['raw_emotion_scores'] = df['smallwords_removed'].apply(lambda x:NRCLex(x).raw_emotion_scores if type(x)==str else False)
    df['top_emotions'] = df['smallwords_removed'].apply(lambda x:NRCLex(x).top_emotions if type(x)==str else False)
   # df['affect_frequencies'] = df['text'].apply(lambda x:NRCLex(x).affect_frequencies if type(x)==str else False)
    df['affect_dict'] = df['smallwords_removed'].apply(lambda x:NRCLex(x).affect_dict if type(x)==str else False)
    
    ##
   # df['updated_format']=[ast.literal_eval(df.raw_emotion_scores[x])for x in range(len(df.raw_emotion_scores))]
    l=[]
    for i in range(0,len(df)):
        l1={}
        if df.raw_emotion_scores[i]==False:
            l.append('false')
        elif len(df.raw_emotion_scores[i])==1:
            l.append(df.raw_emotion_scores[i])
        else:
            for x,y in df.raw_emotion_scores[i].items():
                if x=='positive':
                    pass
                elif x=='negative':
                    pass
                elif x=='FALSE':
                     pass
                else :
                    l1[x]=y
            l.append(l1)    
    df['new_dict']=l 
    ####
    l2=[]
    for i in range(0,len(df)):
        if df['new_dict'][i]=='false':
            l2.append('false')
            pass
        elif df['new_dict'][i]=={}:
            l2.append('false')
            pass
        else:
            maxValue = max(df['new_dict'][i].values())
            l3=[k for k, v in df['new_dict'][i].items() if v == maxValue]
            l2.append(l3)
    df['new_top_emotions']=l2
    #####
    df1=df[['Text','raw_emotion_scores','stars','new_dict','affect_dict','top_emotions','new_top_emotions']]

    y=[]
    for x in range(len(df)):
        if df1['top_emotions'][x][0][0]==False:
            y.append('neutral')
        else:
            y.append(df1['top_emotions'][x][0][0])
   
    df1['original_top_emotions']=y
    l4=[]
    for i in range(0,len(df1)):
    
    ##positive
        if (df1.stars[i].item()==4 or df1.stars[i].item()==5):
            if df1.original_top_emotions[i]=='negative':
                l4.append("positive")
            else:
                if(df1['new_top_emotions'][i]=='false'):
                    l4.append('positive')
                    
                else  : 
                    l4.append(df1['new_top_emotions'][i][0])
            
        elif (df1.stars[i].item()==1 or df1.stars[i].item()==2) :
            if df1.original_top_emotions[i]=='positive':
                l4.append("negative")
            else:
                if(df1['new_top_emotions'][i]=='false'):
                    l4.append('negative')
                else: 
                    l4.append(df1['new_top_emotions'][i][0])
        else:
            if(df1['new_top_emotions'][i]=='false'):
                    l4.append('anticipation ')
            else:        
                l4.append(df1['new_top_emotions'][i][0])
        
    df1['Final']=l4
    
    df['emotions1']=df1['Final']
    df['emotions1']=df.emotions1.str.capitalize()
    return df