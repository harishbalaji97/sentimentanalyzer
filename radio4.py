# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 14:23:14 2022

@author: harish.b.sampath
"""

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
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.markdown("""
<style>
.stButton>button {
color: #000000;
backgroud-color: #A100FF;
height: 3em;
width: 13em;

}
</style> 
""",unsafe_allow_html=True)

st.markdown("""
<style>
.h3, h3 {
    font-size: 1.3rem;
    text-align: center;
}
.css-10trblm {
    position: relative;
    flex: 1 1 0%;
    margin-left: calc(0rem);
    text-decoration: underline;
    background:rgb(240, 242, 246);
    
}



.css-1q80ws6 {
    width: 274px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 0.5rem;
}


.css-qrbaxs {
    font-size: 14px;
    color: rgb(49, 51, 63);
    margin-bottom: 7px;
    height: auto;
    min-height: 1.5rem;
    vertical-align: middle;
    display: flex;
    flex-direction: row;
    -webkit-box-align: center;
    align-items: center;
    font-weight: 700;
}
.h3, h3 {
    font-size: 1.3rem;
    text-align: center;
    font-weight: 600;
}
code {
    font-size: 87.5%;
    color: white;
    word-break: break-word;
}

p, ol, ul, dl {
    margin: 0px 0px 1rem;
    padding: 0px;
    font-size: 1rem;
    font-weight: 600;
    TEXT-ALIGN: center;
}
<!--position: relative;
    flex: 1 1 0%;
    margin-left: auto;
    border: ridge; -->
    
p {
    margin-top: 0;
    margin-bottom: 0rem;
}

.css-ye58bx {
    width: 154px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 0rem;
}

.h1, .h2, .h3, .h4, .h5, .h6, h1, h2, h3, h4, h5, h6 {
    margin-bottom: .5rem;
    font-family: inherit;
    font-weight: 700;
    line-height: 1.2;
    color: inherit;
    
}
p, ol, ul, dl {
    margin: 0px 0px 1rem;
    padding: 0px;
    font-size: 1.2rem;
    font-weight: 700;
    TEXT-ALIGN: center;
   <!-- text-decoration: underline;-->
}
.h2, h2 {
    font-size: 1.1rem;
    text-align: center;
    text-decoration: underline;
}
.css-1xarl3l {
    font-size: 1.5rem;
    padding-bottom: 0.25rem;
    font-weight: 700;
}

.css-1ht1j8u {
    overflow-wrap: normal;
    text-overflow: ellipsis;
    width: 100%;
    overflow: hidden;
    white-space: nowrap;
    font-family: "Source Sans Pro", sans-serif;
    line-height: normal;
    text-align: center;
    border: none;
    border-color: lightgrey;
    font-weight:600;
}

.css-ocqkz7 {
    display: flex;
    flex-wrap: wrap;
    -webkit-box-flex: 1;
    flex-grow: 1;
    -webkit-box-align: stretch;
    align-items: stretch;
    gap: 0.5rem;

    
} 
.css-10y5sf6 {
    font-family: "Source Code Pro", monospace;
    font-size: 14px;
    padding-bottom: 9.33333px;
    color: #f8f9fa;
    top: -22px;
    position: absolute;
    white-space: nowrap;
    background-color: transparent;
    line-height: 1.6;
    font-weight: normal;
}

.css-l3zrbl {
    width: 119px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 1rem;
}

</style>
""",unsafe_allow_html=True            )
st.markdown("""
<style>
.sidebar .sidebar-content {
    background-color: #A100FF;
    textColor : #000000;
}
</style>
"""
, unsafe_allow_html=True)
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 250px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 250px;
        margin-left: -250px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
"""
<style>
/* The input itself */
div[data-baseweb="select"] > div {
  background-color: #ffffff !important;
  font-weight:500;
  <!--border-color:#000000;-->
  <!-- font-size: 23px !important;-->
}
</style>
"""
, unsafe_allow_html=True)


st.markdown(
"""
<style>
/* The input itself */
div[data-baseweb="input"] > div {
  background-color: #ffffff;
  border-color:#000000;
  <!-- font-size: 23px !important;-->
  font-weight: bold;
}
</style>
"""
, unsafe_allow_html=True)

st.markdown("""
<style>
.big-font {
    font-size:12 !important;
}
</style>
""", unsafe_allow_html=True)  
st.markdown("""
            <html>
<!-- Include Bootstrap CSS -->
<style>
		/* Modify the background color */
		
		.navbar-custom {
			background-color: #a804fc;
           <!--  border:2px solid#ffffff;-->
            text-align : center ;
		}
		/* Modify brand and text color */
		
		.navbar-custom .navbar-brand,
		.navbar-custom .navbar-text {
			color: #ffffff;
            font-size :1.2em;
            font-weight: bold ;
          }
        .navbar {max-height:55px;}
        
        .navbar-nav.navbar-center {
            position:center;
            }
        
        .css-nlntq9 a {
            color: #f8f9fa;
            align-items: center;
            font-weight: 700;
            font-size: large;
            right: 50%;
        }
        
    
	</style>
    
</head>

<body>
	<!-- Navbar text is dark and background is light -->
	<nav class="navbar fixed-top navbar-expand-lg navbar-custom">
		<a class="navbar-brand" href="#">
        <img src="https://logos-world.net/wp-content/uploads/2020/07/Accenture-Symbol.png" alt="" style="width:100px;height:55px;margin-top:-15px;">
         | Solutions.Ai
	</a>
        <div class="mx-auto">
			<a class="navbar-brand " href="#" style="font-size:1.5rem;">Intelligent Email Sentiment Analyzer</a>
			<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
			  <span class="navbar-toggler-icon"></span>
			</button>
		</div>
    </nav>

</body>

</html>

""", unsafe_allow_html=True)
st.markdown("""
<style>
.st-by {
    width:0px;
    height:0px;
    border:none;
    border-color:white;
}

form input[type=="radio"]:checked+lable
{
 background-color:white;
 }

.st-bd {
    -webkit-box-align: center;
    align-items: center;
    font-weight: 800;
    <!-- border: ridge;  -->
}

.st-cc {
    color: rgb(49, 51, 63);
    <!- font-size: larger;-->
    font-weight: 400;
    <!-- padding: initial;  -->
}



} 
            
element.style {
    background-color:#A100FF;
    border:none;
}

.st-bx {
    vertical-align: middle;
     margin-bottom: 20px;
    border : ridge;
    border-color:#F1EDF2;
    background:white;
}

.st-ea
{
 border:ridge;
 }
.st-e9
{
 border:ridge;
 }
.st-c0
{
 border:none;
 border-color: white;
}

.st-cb {
    padding-left: 0;
    -webkit-box-align: center;
    width: 11em;
    flex-group: 1;
    text-align: center;
    font-size: 1.2rem;
    <!--border:none;-->
}

.css-l3zrbl {
    width: 119px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 1rem;
    border: ridge;
}


.css-dbtxvr {
    width: 152px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 1rem;
    border: ridge;
}
@media (min-width: 576px)
<style>
.css-12oz5g7 {
    padding-left: 0rem;
    padding-right: 0rem;
}
.css-ocqkz7 {
    display: flex;
    flex-wrap: wrap;
    -webkit-box-flex: 1;
    flex-grow: 1;
    -webkit-box-align: stretch;
    align-items: stretch;
    gap: 0.5rem;
    <!-- border: solid; -->
}
.stSelectbox
{
    border:ridge;
    padding: 0.7rem;
    background: rgb(240, 242, 246);
    }



div.css-1v0mbdj.etr89bj1
{
 border:ridge;
 }

img {
  vertical-align: middle;
  border-style: none; // Remove the border on images inside links in IE 10-.
}

div['data-testid']{
    border:none !important;
    `}

.css-qrbaxs {
    font-size: 14px;
    color: rgb(49, 51, 63);
    margin-bottom: 7px;
    height: auto;
    min-height: 1.5rem;
    vertical-align: middle;
    display: flex;
    flex-direction: row;
    -webkit-box-align: center;
    align-items: center;
    font-weight: 700;
    background: rgb(240, 242, 246);
}


.stSlider {
    width: 73px;
    border: ridge;
    padding: 0.4rem;
    background: rgb(240, 242, 246);
}

.css-1kyxreq etr89bj0
{
 border :none ;
 }
[data-stale =false]
{
    border:none !important ;
    }
 .css-keje6w {
    width: calc(50% - 1rem);
    flex: 1 1 calc(50% - 1rem);
    border: none;
}

.css-12w0qpk {
    width: calc(25% - 1rem);
    flex: 1 1 calc(25% - 1rem);
    border: none;
    padding: 0.1rem;
}

.css-wlyek {
    width: calc(60.241% - 1rem);
    flex: 1 1 calc(60.241% - 1rem);
    border: none;
}  

.st-e9 {
    border: none;
}

.st-e8 {
    min-width: 0px;
    border: ridge;
}
            </style>
""",unsafe_allow_html=True)
hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
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
        img = Image.open("MicrosoftTeams-image.png")

        newsize = (720, 360)
        img = img.resize(newsize)
        #col1,col2,col3=st.columns([1,4,1])
        #with col2:
        #st.title("E-MAIL SENTIMENT ANALYZER")
        st.title("Welcome")
        
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
                    #output_df['emotions1']=np.nan
                    output_df['date_mod']=np.nan
                    for i in np.arange(0,len(output_df)):
                         #ages=output_df['emotion'][i]
                         #ages=ast.literal_eval(ages)
                         #print(ages)
                         #max_value = max(ages, key=ages.get)
                         #output_df['emotions1'][i]=max_value 
                         output_df['date_mod'][i]=random_date("2/7/22", "2/22/22", random.random())
                    output_df['Receiver_Email_Type'].replace({"gmail":"Gmail","yahoo":"Yahoo","outlook":"Outlook"},inplace=True)
                    output_df['Label'].replace({"positive":"Positive","negative":"Negative","neutral":"Neutral"},inplace=True)
                    output_df=topicmod(output_df)
                    #output_df["emotion"] = output_df["emotion"].apply(lambda x:  ast.literal_eval(x))
                    #output_df["emotion_updated"] = output_df.apply(lambda row : correct_emotion(row),axis=1)
                    #output_df['emotions1']=np.nan
                    #for i in np.arange(0,len(output_df)):
                     #   ages=output_df['emotion_updated'][i]
                      #  max_value = max(ages, key=ages.get)
                       # output_df['emotions1'][i]=max_value
                    #st.write("File saved")
                    output_df['Departments']=output_df['Department_1']
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
        