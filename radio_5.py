# -*- coding: utf-8 -"""

import streamlit as st

import os

import visual
import outcome
print(os.getcwd())
import outcome2
import email_parser as ep
import SentimentAnalysisPreprocess as sp
import numpy as np
import Sentimentlabel as sl
import emotionopred as ed
from topic_mod import topicmod
import matplotlib as mpl
#import input1
from PIL import Image
import time

from operator import itemgetter

def correct_emotion(row):
    emotion_dict = row["emotion"].copy()
    
    if row["Label"] == "Positive":
        print(max(list(emotion_dict.items()),key=itemgetter(1))[0])
        print(emotion_dict)
        if max(list(emotion_dict.items()),key=itemgetter(1))[0] == "Fear" or emotion_dict["Happy"]<emotion_dict["Fear"]:

            fear_value = emotion_dict["Fear"]
            emotion_dict["Happy"] = round(emotion_dict["Happy"] + fear_value*0.5 + 0.01,2)
            emotion_dict["Fear"]  = round(fear_value*0.5,2)

            print(emotion_dict)
        return emotion_dict
    else:
        return emotion_dict
def try1(df,stre):
    try:
        count=df[df['Sender Email Type'].str.strip()==stre]['count'].values[0]
    except :
        count=0
    return count 

def try1(df,stre):
    try:
        count=df[df['Sender Email Type'].str.strip()==stre]['count'].values[0]
    except :
        count=0
    return count 
mpl.rcParams["legend.loc"]="lower right"
#mpl.rc('xtick', labelsize=20) 
#mpl.rc('ytick', labelsize=8) 

#st.set_page_config(layout="wide")

import random
import time
    
def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%y', prop)

placeholder = st.empty()
st.session_state['but']=st.sidebar.radio("" ,["Home","User Input","Executive Summary","Sentiment Analytics","Mail Content"])
if st.session_state['but']=='Home':
    placeholder.empty()
    status=0
    with placeholder.container():
        img = Image.open("what-is-sentiment-analysis.jpg")

        newsize = (720, 360)
        img = img.resize(newsize)
        #col1,col2,col3=st.columns([1,4,1])
        #with col2:
        #st.title("E-MAIL SENTIMENT ANALYZER")
        st.title("Welcome")
        st.header("Sentiment Analysis")
        
        st.image(img)   
        
if st.session_state['but']=='User Input':
    placeholder.empty()
    status=0
    st.session_state['genre'] = placeholder.selectbox("Choose file Type",["File","Directory"],index=1)
    with st.empty():
        st.session_state['file']=""
        st.session_state['message_text']=""
        #img = Image.open("MicrosoftTeams-image.png")
    
        #newsize = (720, 360)
        #img = img.resize(newsize)
        #col1,col2,col3=st.columns([1,4,1])
        #with col2:
        #st.title("E-MAIL SENTIMENT ANALYZER")
        #st.title("Welcome")
        
        #st.image(img)   
        #st.write("Let's get started")
        if st.session_state['genre']!="":
            message_text=""
            file=""
            if st.session_state['genre'] == 'File':
                st.session_state['file']=st.file_uploader("upload file",accept_multiple_files=False)
            else:
                st.session_state['message_text'] = st.text_input("Enter Directory Location")
                #
            #submit_button = st.sidebar.form_submit_button(label="UPLOAD")
                
            #if st.sidebar.button("Upload"):
             #   st.markdown("You chose the directory" , message_text)
              #  print("process completed",message_text)
             #message_text=r"C:\Users\harish.b.sampath\Documents\Python_Scripts\Preprocessing Code Files_V1\Data"
            #placeholder.text(" " )
            if st.session_state['message_text']!="":
                placeholder.text("")
                with st.spinner("Parsing the files ....."):
                    df=ep.mail_parser(st.session_state['message_text'])
                    time.sleep(2)
                st.info(" Parsing - Done")
                
                with st.spinner("Preprocessing the extracted text...."):
                    output_df = sp.textpreprocess_pipeline(df,True,True)
                    time.sleep(1)
                st.info("Preprocessing - Done")
                
                with st.spinner(" Model Prediction...."):
                    output_df=sl.sentimentpred(output_df)
                    output_df=ed.emotion(output_df)
                 #output_df=ed.emotion(output_df)
                    output_df['emotions1']=np.nan
                    output_df['date_mod']=np.nan
                    for i in np.arange(0,len(output_df)):
                         ages=output_df['emotion'][i]
                         #ages=ast.literal_eval(ages)
                         #print(ages)
                         max_value = max(ages, key=ages.get)
                         output_df['emotions1'][i]=max_value 
                         output_df['date_mod'][i]=random_date("2/7/22", "2/22/22", random.random())
                    output_df['Receiver_Email_Type'].replace({"gmail":"Gmail","yahoo":"Yahoo","outlook":"Outlook"},inplace=True)
                    output_df['Label'].replace({"positive":"Positive","negative":"Negative","neutral":"Neutral"},inplace=True)
                    output_df=topicmod(output_df)
                    #output_df["emotion"] = output_df["emotion"].apply(lambda x:  ast.literal_eval(x))
                    output_df["emotion_updated"] = output_df.apply(lambda row : correct_emotion(row),axis=1)
                    output_df['emotions1']=np.nan
                    for i in np.arange(0,len(output_df)):
                        ages=output_df['emotion_updated'][i]
                        max_value = max(ages, key=ages.get)
                        output_df['emotions1'][i]=max_value
                    #st.write("File saved")
                    output_df.to_csv('fgk.csv')
                st.info(" Prediction - Done")
                with st.spinner(" Rendering Visualization...."):
                    time.sleep(3)
                    st.info("Redering Visulaization")
            status=1
    #if status==1:
    #st.write("removing")
    #placeholder.empty()
             
    if st.session_state['message_text']!="" and st.session_state['file']=="":
        placeholder.empty()
        with placeholder.container():
            outcome.app()
    if st.session_state['file']!="" and st.session_state['message_text']=="":
            #st.write("Proceed to Executive Summary File Processed" ,st.session_state['file'])
        print("ehllo")
if st.session_state['but']=='Executive Summary':
    placeholder.empty()
    with placeholder.container():
        outcome.app()
        
if st.session_state['but']=='Sentiment Analytics':
    placeholder.empty()
    with placeholder.container():
        outcome2.app()
        
if st.session_state['but']=='Mail Content':
    placeholder.empty()
    with placeholder.container():
        visual.app()
#if st.session_state['but']=='Text Analytics':
 #   placeholder.empty()
  #  with placeholder.container():
   #     outcome2.app()
        
