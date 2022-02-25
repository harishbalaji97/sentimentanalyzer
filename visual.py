# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 18:16:28 2022

@author: harish.b.sampath
"""

import streamlit as st
import numpy as np
import pandas as pd

def try1(df,stre):
    try:
        count=df[df['Sender Email Type'].str.strip()==stre]['count'].values[0]
    except :
        count=0
        
    return count
def app():
    
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
    output_df['Sentiment']=output_df['Label']
    output_df['Emotions']=output_df['emotions1']
    
    st.table(output_df[['Text',"Sentiment","Emotions"]])
    
       
if __name__ == "__main__":
    app()