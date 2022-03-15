# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 10:05:08 2022

@author: harish.b.sampath
"""
import streamlit as st
import pandas as pd
import os
print(os.getcwd())
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

from PIL import Image


def app():
    

    output_df=pd.read_csv('fgk.csv') 
    output_df['date_mod']=pd.to_datetime(output_df['date_mod'])
    topic_df=output_df
    df=output_df.groupby(['Receiver_Email_Type'])['From'].count().reset_index()
    df=df.rename(columns={"From":"count" ,"Receiver_Email_Type" : "Sender Email Type"})
    #df1=df.set_index("Sender Email Type")
    #st.write("func 2")
    #col1,col2=st.columns(2)
    st.session_state.email=['All']
    st.session_state.dept=['All']
    st.session_state.loc=['All']
    st.session_state.age=5
    st.session_state.label=['All']
    
    
    
    
    
    col1,col3,col4,col5,col6=st.columns([1,1,1,1,1])
    for j in output_df['Receiver_Email_Type'].unique():
        st.session_state.email.append(j)
    
    for j in output_df['Departments'].unique():
        if str(j)!="nan":
            st.session_state.dept.append(j)
            
    for j in output_df['Label'].unique():
        st.session_state.label.append(j)
        
    for j in output_df['Location'].unique():
        st.session_state.loc.append(j)
        
        
          
    with col3:
        st.selectbox("Department",st.session_state.dept,key='dept_sel')
    with col1:
       st.slider('Date', output_df['date_mod'].min().date(), output_df['date_mod'].max().date() , (output_df['date_mod'].min().date(), output_df['date_mod'].max().date()),format="D/M",key='age_sel')
       print(st.session_state['age_sel'][0])
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
           
    text1=text.split(" ")
    counter=Counter(text1)
    word_freq=pd.DataFrame()
    word_freq['word']=counter.keys()
    word_freq['freq']=counter.values()
    word_freq.reset_index(inplace=True,drop=True)
    word_freq1=word_freq.sort_values('freq',ascending=False)
    c1,c2=st.columns([3,5])
    with c1:
        st.subheader("Sentiments : Overview")
    with c2:
        st.subheader("Sentiments of Key Topics")
            


    
    col1,col2,col3,col5,col4=st.columns([1,1,1,0.3,5])
    temp1=output_df.groupby(['Label'])['From'].count().reset_index()
    temp1=temp1.sort_values('From')
    t=temp1['From']
    classes=temp1['Label']
    #temp1['Perc']=(temp1['From']/data.shape[0])*100
    temp1['perc%'] = (temp1['From'] / output_df.shape[0]).map(lambda num: '{0:.1f}%'.format(round(num * 100, 1)))
    temp1.reset_index(inplace=True)
    with col1:
        #st.subheader("  ")
        st.write("Positive")
        try:
            tr=temp1[temp1['Label']=='Positive']['perc%'].values[0]
        except:
            tr="0 %"
        st.write(tr)
        img = Image.open("positive_2.jpg")
        newsize = (75, 75)
        img = img.resize(newsize)
        #col1,col2,col3=st.columns([1,4,1])
        #with col2:
        #st.title("E-MAIL SENTIMENT ANALYZER")
        st.image(img)
        
        #st.image(img)
    with col2:
        #st.subheader("Sentiment : Overview")
        st.write("Negative")
        try:
            tr=temp1[temp1['Label']=='Negative']['perc%'].values[0]
        except:
            tr="0 %"
        st.write(tr)
        img = Image.open("negative_2.jpg")
        newsize = (75, 75)
        img = img.resize(newsize)
        #col1,col2,col3=st.columns([1,4,1])
        #with col2:
        #st.title("E-MAIL SENTIMENT ANALYZER")
        st.image(img)
    with col3:
        #st.subheader("  ")
        st.write("Neutral")
        try:
            tr=temp1[temp1['Label']=='Neutral']['perc%'].values[0]
        except:
            tr="0 %"
        st.write(tr)
        img = Image.open("neut_2.jpg")
        newsize = (75, 75)
        img = img.resize(newsize)
        #col1,col2,col3=st.columns([1,4,1])
        #with col2:
        #st.title("E-MAIL SENTIMENT ANALYZER")
        st.image(img)
        
        
                 
        
    with col4:
        temp2=output_df.groupby(['Label','Tags'])['From'].count().reset_index()
        temp3=pd.pivot_table(temp2, values='From', index=['Tags'],columns=['Label'], aggfunc=np.sum)
        #st.subheader("Sentiments of Key Topics")
        temp3["sum"] = temp3.sum(axis=1)
        temp3=temp3.sort_values('sum',ascending=True)
        #temp3=temp3.sort_values('Positive',ascending=False)
        fig,ax=plt.subplots(figsize=(7,3))
        #fig,ax=plt.subplots(figsize=(10,5))
        #for axis in [ax.yaxis]:
         #   axis.set_major_locator(ticker.MaxNLocator(integer=True))
             # importing package
              # create data
            #e = temp3['Angry']
        temp3.fillna(0,inplace=True)
        x=list(temp3.index)
        try:
            f = temp3['Positive']
        except:
            f=[0]* len(temp3)
        try:
            ph =temp3['Neutral'] 
        except:
            ph=[0]*len(temp3)
            
        try:    
            p = temp3['Negative']
        except:
            p=[0]* len(temp3)
            
           # rem=temp3['Suprise']
             # plot bars in stack manner
            #ax.bar(x, e, color='r')
        ax.barh(x, f, color='g')
        ax.barh(x, ph, left=f, color='y')
        ax.barh(x, p, left=f+ph, color='r')
        #ax.barh(x, rem, left=f+ph+p, color='brown')
        #ax.barh(x, rem1, left=f+ph+p+rem, color='magenta')
        #ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
            #ax.set_xlabel("Emotions")
        #plt.xticks(rotation=30)
        #ax.bar_label(barh,label_type='edge',fontsize=18)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.get_xaxis().set_ticks([])
        #ax.set_ylabel("No. of mails")
        plt.yticks(fontsize=12)
        ax.legend([ "Positive", "Neutral", "Negative"],fontsize=8)
        st.pyplot(fig)
        
    c1,c2=st.columns([3,5])
    with c1:
        st.subheader("Emotions : Overview")
    with c2:
        st.subheader("Emotions of Key Topics")
         
         
    col1,col2,col3,col5,col4=st.columns([1,1,1,0.3,5])
    
    temp1=output_df.groupby(['emotions1'])['From'].count().reset_index()
    temp1=temp1.sort_values('From',ascending=False)
    t=temp1['From']
    classes=temp1['emotions1']
    #temp1['Perc']=(temp1['From']/data.shape[0])*100
    temp1['perc%'] = (temp1['From'] / output_df.shape[0]).map(lambda num: '{0:.1f}%'.format(round(num * 100, 1)))
            
    with col1:
        #temp1.rename(columns={'perc%':""},inplace=True)
        #temp1.set_index('emotions1',inplace=True)
        temp1.drop('From',axis=1,inplace=True)
        #st.table(temp1)
        unq=temp1['emotions1'].unique()
        
        st.write("Trust")
        st.write("Negative")
        st.write("Anticipation")
        st.write("Joy")
        st.write("Positive")
        st.write("Sadness")
        st.write("Anger")
        st.write("Fear")
        st.write("Disgust")
        st.write("Surprise")
        
        
    with col2:
        try:
            st.write(temp1[temp1['emotions1']=='Trust']['perc%'].values[0])
        except:
            st.write("0 %")
        try:
            st.write(temp1[temp1['emotions1']=='Negative']['perc%'].values[0])
        except:
            st.write("0 %")
        try:
            st.write(temp1[temp1['emotions1']=='Anticipation']['perc%'].values[0])
        except:
            st.write("0 %")
        try:
            st.write(temp1[temp1['emotions1']=='Joy']['perc%'].values[0])
        except:
            st.write("0 %")
        try:
            st.write(temp1[temp1['emotions1']=='Positive']['perc%'].values[0])
        except:
            st.write("0 %")
            
        try:
            st.write(temp1[temp1['emotions1']=='Sadness']['perc%'].values[0])
        except:
            st.write("0 %")
        try:
            st.write(temp1[temp1['emotions1']=='Anger']['perc%'].values[0])
        except:
            st.write("0 %")
        try:
            st.write(temp1[temp1['emotions1']=='Fear']['perc%'].values[0])
        except:
            st.write("0 %")
        try:
            st.write(temp1[temp1['emotions1']=='Disgust']['perc%'].values[0])
        except:
            st.write("0 %")
        try:
            st.write(temp1[temp1['emotions1']=='Surprise']['perc%'].values[0])
        except:
            st.write("0 %")
        
        
    siz=(25,25)
    with col3:
        #st.text("")
        img = Image.open("trust.png")
        newsize = (25, 25)
        img = img.resize(siz)
        st.image(img)
        img = Image.open("sad.png")
        newsize = (27, 27)
        img = img.resize(siz)
        st.image(img)
        img = Image.open("aniticipation.png")
        newsize = (27, 27)
        img = img.resize(siz)
        st.image(img)
        img = Image.open("happy.png")
        newsize = (27, 27)
        img = img.resize(siz)
        st.image(img)
        img = Image.open("happy.png")
        newsize = (27, 27)
        img = img.resize(siz)
        st.image(img)
        img = Image.open("sad.png")
        newsize = (27, 27)
        img = img.resize(siz)
        st.image(img)
        img = Image.open("angry.png")
        newsize = (27, 27)
        img = img.resize(siz)
        st.image(img)
        img = Image.open("fear.png")
        newsize = (27, 27)
        img = img.resize(siz)
        st.image(img)
        img = Image.open("disgust.jpg")
        newsize = (27, 27)
        img = img.resize(siz)
        st.image(img)
        img = Image.open("surprised.png")
        newsize = (27, 27)
        img = img.resize(siz)
        st.image(img)
        
     
    with col4:
    
        temp2=output_df.groupby(['emotions1','Tags'])['From'].count().reset_index()
        #temp2=temp2.sort_values('From',ascending=False)
        temp3=pd.pivot_table(temp2, values='From', index=['Tags'],columns=['emotions1'], aggfunc=np.sum)
        #temp3=temp3.sort_values('Happy',ascending=False)
        temp3["sum"] = temp3.sum(axis=1)
        temp3=temp3.sort_values('sum',ascending=True)
        #st.subheader("Emotions of Key Topics")
        fig,ax=plt.subplots(figsize=(7,3))
        #for axis in [ax.yaxis]:
         #   axis.set_major_locator(ticker.MaxNLocator(integer=True))
             # importing package
              # create data
            #e = temp3['Angry']
        temp3.fillna(0,inplace=True)
        x=list(temp3.index)
        try:
            f = temp3['Trust']
        except:
            f=[0]* len(temp3)
        try:
            ph =temp3['Negative']
        except:
            ph=[0]*len(temp3)
            
        try:    
            p = temp3['Anticipation']
        except:
            p=[0]* len(temp3)
            
        try:
            rem = temp3['Joy']
        except:
            rem=[0]*len(temp3)
            
        try:
            rem1 = temp3['Positive']
        except:
            rem1=[0]*len(temp3)
            
            
        try:
            rem2 = temp3['Sadness']
        except:
            rem2=[0]*len(temp3)
            
        try:
            rem3 = temp3['Anger']
        except:
            rem3=[0]*len(temp3)
            
        try:
            rem4 = temp3['Fear']
        except:
            rem4=[0]*len(temp3)
            
        try:
            rem5 = temp3['Disgust']
        except:
            rem5=[0]*len(temp3)
            
        try:
            rem6 = temp3['Surprise']
        except:
            rem6=[0]*len(temp3)
           # rem=temp3['Suprise']
             # plot bars in stack manner
            #ax.bar(x, e, color='r')
        ax.barh(x, f, color='g')
        ax.barh(x, p, left=f, color='r')
        ax.barh(x, ph, left=f+p, color='orange')
        ax.barh(x, rem, left=f+ph+p, color='y')
        ax.barh(x, rem1, left=f+ph+p+rem, color='g')
        ax.barh(x, rem2, left=f+ph+p+rem+rem1, color='grey')
        ax.barh(x, rem3, left=f+ph+p+rem+rem1+rem2, color='r')
        ax.barh(x, rem4, left=f+ph+p+rem+rem1+rem2+rem3, color='purple')
        ax.barh(x, rem5, left=f+ph+p+rem+rem1+rem2+rem4, color='lime')
        ax.barh(x, rem6, left=f+ph+p+rem+rem1+rem2+rem5, color='lightgreen')
        #ax.barh(x, rem1, left=f+ph+p+rem, color='magenta')
        #ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
            #ax.set_xlabel("Emotions")
        #plt.xticks(rotation=30)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.get_xaxis().set_ticks([])
        #ax.set_ylabel("No. of mails")
        ax.legend(['Trust', 'Negative', 'Anger', 'Anticipation', 'Joy', 'Sadness','Fear', 'Disgust', 'Positive', 'Surprise'],fontsize=8)
        #plt.legend(['Legend'], )
        plt.yticks(fontsize=12)
        st.pyplot(fig)
      
    
    
        temp2=output_df.groupby(['date_mod','Label'])['From'].count().reset_index()
        temp3=pd.pivot_table(temp2, values='From', index=['date_mod'],columns=['Label'], aggfunc=np.sum)
        x=temp3.index
        try:
            pos=temp3['Positive']
        except:
            pos=[0]*len(temp3)
        try:
            neg=temp3['Negative']
        except:
            neg=[0]*len(temp3)
        try:
            neu=temp3['Neutral']
        except:
            neu=[0]*len(temp3)
        st.subheader(" Daily Trend of Sentiments")
        fig, ax = plt.subplots(figsize=(7,2))
        ax.plot(x,pos, label="Positive")
        ax.plot(x,neg, label="Negative")
        ax.plot(x,neu, label="Neutral")
        ax.set_ylabel("No of Mails")
        ax.legend()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.legend(['Positive','Negative','Neutral'],loc='upper right',fontsize=8)
        plt.xticks(rotation=30)
        st.pyplot(fig) 
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    app()