# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 18:16:51 2022

@author: harish.b.sampath
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
from wordcloud import WordCloud
import matplotlib.ticker as ticker

#st.set_page_config(layout="wide")
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#analyzer = SentimentIntensityAnalyzer()

#def text_sentiment_vader(text):
#    vs = analyzer.polarity_scores(text)
#    return "positive" if vs.get('compound')>0 else "negative" if vs.get('compound')<0 else "neutral"
 
#predictions_vader = df['text'].map(lambda x : text_sentiment_vader(x))
#df['Label'] = predictions_vader


def try1(df,stre):
    try:
        count=df[df['Sender Email Type']==stre]['count'][0]
    except :
        count=0
    return count

def app():
    #output_df=pd.read_csv('fgk.csv')    
    #output_df.to_csv("fgk.csv")
    output_df=pd.read_csv("fgk.csv")
    output_df['date_mod']=pd.to_datetime(output_df['date_mod'])
    df=output_df.groupby(['Receiver_Email_Type'])['From'].count().reset_index()
    df=df.rename(columns={"From":"count" ,"Receiver_Email_Type" : "Sender Email Type"})
    #df1=df.set_index("Sender Email Type")
    #st.write("func 2")
    #col1,col2=st.columns(2)
    st.session_state.email=['All']
    st.session_state.dept=['All']
    st.session_state.loc=['All']
    st.session_state.label=['All']
    
    
    
    
    
    
    col1,col2,col3,col4,col5,col6=st.columns([1,0.2,1,1,1,1])
    for j in output_df['Receiver_Email_Type'].unique():
        st.session_state.email.append(j)
    
    for j in output_df['Departments'].unique():
        if str(j)!="nan":
            st.session_state.dept.append(j)
            
    for j in output_df['Label'].unique():
        st.session_state.label.append(j)
        
    for j in output_df['Location'].unique():
        st.session_state.loc.append(j)
        
    st.session_state.loc.append('United States')   
    with col3:
        st.selectbox("Department",st.session_state.dept,key='dept_sel')
        
    with col1:
       st.slider('Date', output_df['date_mod'].min().date(), output_df['date_mod'].max().date() , (output_df['date_mod'].min().date(), output_df['date_mod'].max().date()),format="D/M",key='age_sel')
       
    with col4:
        st.selectbox("Email Type" ,st.session_state.email,key='email_sel')
    with col5:
        st.selectbox("Location", st.session_state.loc ,key='loc_sel')
    with col6:
        st.selectbox("Sentiment", st.session_state.label ,key='label_sel')
        
   
        
        
    if st.session_state['email_sel']=="All":
        output_df=output_df
    else :
        output_df=output_df[output_df['Receiver_Email_Type']==st.session_state['email_sel']]
                
        #if pred=="all":
            #df=df
       # else :
            #df=df[df['pred']==pred]
    if st.session_state['dept_sel']=="All":
        output_df=output_df
    else :
        output_df=output_df[output_df['Departments']==st.session_state['dept_sel']] 
        
    if st.session_state['label_sel']=="All":
        output_df=output_df
    else :
        output_df=output_df[output_df['Label']==st.session_state['label_sel']] 
        
    ls=pd.date_range(st.session_state.age_sel[0],st.session_state.age_sel[1],freq='d')    
    output_df=output_df[(output_df['date_mod'].isin(list(ls)))]
      
    text=""
    output_df.reset_index(inplace=True)
    for i in np.arange(0,len(output_df)): 
        text=text+str(output_df['smallwords_removed'][i]).replace("[","").replace("'","").replace(",","")
    #width = st.sidebar.slider("plot width", 1, 25, 3)
    #height = st.sidebar.slider("plot height", 1, 25, 1)
   
    df2=output_df.groupby(['date_mod'])['From'].count().reset_index()   
    col1,col2,col3,col4=st.columns([1,1,1,1])
    with col1:
        st.subheader("Overall Summary ")
        #st.write("Mails")
        fig, ax = plt.subplots(2, 2,figsize=(2, 2))
        pstr=str(output_df.shape[0])
        ax[0,0].text( -0.4,-0.2,pstr, fontsize = 12)
        ax[0,0].pie([output_df.shape[0],2], 
               wedgeprops={'width':0.3}, 
               startangle=90, 
               colors=['#5DADE2', '#515A5A'])
        ax[0,0].set_title("Mails")
        #fig.savefig('plot2.png')
        #img = Image.open("plot2.png")
        #newsize = (90, 90)
        #img = img.resize(newsize)
        #st.image(img)
        #st.write("Users")
       # fig, ax = plt.subplots(figsize=(1, 1))
        pstr=str(output_df['From'].nunique())
        ax[0,1].text( -0.2,-0.2,pstr, fontsize = 12)
        ax[0,1].pie([output_df['From'].nunique(),2], 
               wedgeprops={'width':0.3}, 
               startangle=90, 
               colors=['#5DADE2', '#515A5A'])
        ax[0,1].set_title("Users")
        #fig.savefig('plot1.png')
        #img = Image.open("plot1.png")
        #newsize = (90, 90)
        #img = img.resize(newsize)
        #st.image(img)
        #st.write("Country")
        #fig, ax = plt.subplots(figsize=(1, 1))
        pstr=str(output_df['Location'].nunique())
        ax[1,0].text( -0.2,-0.2,pstr, fontsize = 12)
        ax[1,0].pie([output_df['Location'].nunique(),2], 
               wedgeprops={'width':0.3}, 
               startangle=90, 
               colors=['#5DADE2', '#515A5A'])
        ax[1,0].set_title("Country",y=0.9)
        #fig.savefig('plot3.png')
        #img = Image.open("plot3.png")
        #newsize = (90, 90)
        #img = img.resize(newsize)
        #st.write(img)
        #st.write("Depts")
        #fig, ax = plt.subplots(figsize=(1, 1))
        pstr=str(output_df['Departments'].nunique())
        ax[1,1].text( -0.2,-0.2,pstr, fontsize = 12)
        ax[1,1].pie([output_df['Departments'].nunique(),2], 
               wedgeprops={'width':0.3}, 
               startangle=90, 
               colors=['#5DADE2', '#515A5A'])
        ax[1,1].set_title("Depts",y=0.9)
        #fig.savefig('plot4.png')
        #img = Image.open("plot4.png")
        #newsize = (90, 90)
        #img = img.resize(newsize)
        #st.image(img)
        #pstr=str(output_df['From'].nunique())+" Users"
        #st.subheader(pstr)
        #pstr=str(output_df['From'].nunique())
        #fig, ax = plt.subplots(figsize=(1, 1))
        #pstr=str(output_df.shape[0])
        #ax.text( -0.2,-0.2,pstr, fontsize = 12)
        #ax.pie([output_df['From'].nunique(),0], 
              # wedgeprops={'width':0.3}, 
               #startangle=90, 
              # colors=['#5DADE2', '#515A5A'])
        st.pyplot(fig)
        
         
       # pstr=str(output_df['Department'].nunique())+" Depts."
        #st.subheader(pstr)
       # pstr=str(output_df['Location'].nunique())+" Country"
        #st.subheader(pstr)
    


    with col2:
        st.subheader("Overall Sentiments")
        st.write(" ")
        fig,ax=plt.subplots(figsize=(2,2))
            #explode = (0, 0.1)
        temp1=output_df.groupby(['Label'])['From'].count().reset_index()
        temp1=temp1.sort_values('Label')
        t=temp1['From']
        classes=temp1['Label']
            #plt.pie(result['spam_probability'],labels=classes)
        ax.pie(t, labels=classes,wedgeprops={'linewidth':1.0 ,'edgecolor':'white'},autopct='%1.1f%%',colors=['r','y','g'])
        ax.axis('equal')
        st.pyplot(fig)
    with col3:
        st.subheader("Overall Emotions")
        st.write(" ")
        fig,ax=plt.subplots(figsize=(8,8))
            #explode = (0, 0.1)
        temp1=output_df.groupby(['emotions1'])['From'].count().reset_index()
        temp1=temp1.sort_values('emotions1')
        t=temp1['From']
        classes=temp1['emotions1']
            #plt.pie(result['spam_probability'],labels=classes)
        ax.pie(t, labels=classes,wedgeprops={'linewidth':1.0 ,'edgecolor':'white'},autopct='%1.1f%%',colors=['r','brown','g','y','magenta'],textprops={'fontsize': 25})
        ax.axis('equal')
        st.pyplot(fig)
        
    with col4:
        st.subheader("Daily trend of emails")
        fig,ax = plt.subplots(figsize=(6,6)) # try different values
        
        for axis in [ax.yaxis]:
            axis.set_major_locator(ticker.MaxNLocator(integer=True))
            #figsize=(15,5)
            #temp=word_freq1.head(age)
        ax.plot(df2['date_mod'],df2['From'])
        #ax.set_xlabel("Date")
        plt.xticks(rotation=30)
        ax.set_ylabel("No. of Mails")
            #fig.title("TREND")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)   
        st.pyplot(fig)
    
    
    col1,col2=st.columns(2)
    temp2=output_df.groupby(['Label','Departments'])['From'].count().reset_index()
    temp3=pd.pivot_table(temp2, values='From', index=['Departments'],columns=['Label'], aggfunc=np.sum)
    #temp3=temp3.sort_values(['Label'])
    #temp3.reset_index(inplace=True)
    with col1:
        st.subheader("Data Representation with Top Words")
        wordcloud = WordCloud(background_color = 'white',height=500,width=1000).generate(text)
        fig = plt.figure() # try different values
        ax = plt.axes()
            #plt.figure(figsize=(10,8))
        ax.imshow(wordcloud)
        ax.axis("off")
        #ax.
            #plt.title("WordCloud - Vocabulary from Reviews", fontsize = 22)
        st.pyplot(fig)
        
    with col2:
        st.subheader("Distribution of Key Topics")
        df=output_df.groupby(['Tags'])['From'].count().reset_index()
        df=df.rename(columns={"From":"count" ,"Tags" : "Sender Email Type"})
        df.sort_values('count',inplace=True)
        #temp1=output_df.groupby(['Tags'])['From'].count().reset_index()
        #temp1=temp1.sort_values(['emotions1'],ascending=False)
        fig,ax=plt.subplots(figsize=(10,10))
        hbars = ax.barh(df['Sender Email Type'],df['count'], align='center')
        ax.set_yticks(df['Sender Email Type'])
        ax.bar_label(hbars,label_type='edge',fontsize=18)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_xaxis().set_ticks([])
        plt.yticks(fontsize=25)
        st.pyplot(fig)
        #fig,ax=plt.subplots()
            #explode = (0, 0.1)
        #temp1=output_df.groupby(['Tags'])['From'].count().reset_index()
        #temp1=temp1.sort_values(['emotions1'])
        #t=temp1['From']
        #classes=temp1['Tags']
            #plt.pie(result['spam_probability'],labels=classes)
        #ax.pie(t, labels=classes,wedgeprops={'linewidth':1.0 ,'edgecolor':'white'},autopct='%1.1f%%',colors=['r','g','y','brown'],textprops={'fontsize': 18},pctdistance=0.7)
        #ax.axis('equal')
        #centre_circle = plt.Circle((0, 0), 0.50, fc='white')
        #fig = plt.gcf()
  
# Adding Circle in Pie chart
        #fig.gca().add_artist(centre_circle)
        #fig.legend(bbox_to_anchor=(2,2))
        #st.pyplot(fig)
        
       
if __name__ == "__main__":
    app()