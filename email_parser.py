import os
import pandas as pd
import email
from email import policy
import datetime as dtm
from datetime import datetime
import extract_msg     #To read the Outlook Mails
from email.parser import BytesParser # to read Emails

def mail_parser(dir1):
    eml         = []  #List of all the .eml files(Email,Yahoo files)
    msgf        = []  #List of all the .msg files(Outllok files)
    msg_receiver= []  #List of receiver info from the email files
    msg_sender  = []  #List of sender info from email files
    subject     = []  #List of subject info from email files
    date        = []  #List of date info from email files
    txt         = []  #List of text/message info from email files
    uid         = []  #Unique ID for EMAIL files
    msg_from    = []  #List of sender info from outllok files
    msg_to      = []  #List of receiver info from Outlook files
    msg_date    = []  #List of date info from outllok files
    msg_subj    = []  #List of Suject info from Outllok files
    msg_body    = []  #List of text/message info from Outllok files
    msg_id      = []  #unique id for Outllok files
    eml_dmy     = []  #Year-Month-Date formate of Date form the EMail files
    msg_dmy     = []  #Year-Month-Date formate of Date form the outlook files
    receiver_eml_type    = []
    receiver_msg_type    = []
    sender_eml_type    = []
    sender_msg_type    = []
    #dir1=r"C:\Users\harish.b.sampath\Documents\Python_Scripts\Preprocessing Code Files_V1\Data"
    for (dir,dirs,files) in os.walk(dir1):
    #for (dir,dirs,files) in os.walk(os.getcwd()):
        
        for f in files:
            if f[-4:]=='.eml':
                eml_fil=dir+'\\'+f
                eml.append(eml_fil)
            elif f[-4:]=='.msg':
                msg_fil=dir+'\\'+f
                msgf.append(msg_fil)

    for out in range(0,len(msgf)):
            msg = extract_msg.Message(msgf[out])
            msg_from.append(msg.sender)
            msg_date.append(msg.date)
            msg_subj.append(msg.subject)
            msg_body.append(msg.body)
            msg_to.append(msg.to)
            msg_id.append(out+1)
      
    for i in range(0,len(eml)):
        with open(eml[i], 'rb') as fp:  # select a specific email file from the list
            name = fp.name # Get file name
            eml_msg = BytesParser(policy=policy.default).parse(fp)
            text=eml_msg.get_body(preferencelist=('plain')).get_content()
            msg_receiver.append(eml_msg['to'])
            msg_sender.append(eml_msg['from'])
            subject.append(eml_msg['Subject'])
            date.append(eml_msg['date'])
            uid.append(len(msgf)+i+1)
            txt.append(text)
    #        print(date)
      
    for i in date:
        eml_dmy.append(dtm.datetime.strptime((i.split(",")[1][1:12]),'%d %b %Y'))
    for i in msg_date:
        msg_dmy.append(dtm.datetime.strptime((i.split(",")[1][1:12]),'%d %b %Y')) 
    for i in (msg_to):
        receiver_msg_type.append((i.split("@")[1]).split(".")[0])
    for i in msg_receiver:
        receiver_eml_type.append((i.split("@")[1]).split(".")[0])
    for i in (msg_from):
        sender_msg_type.append((i.split("@")[1]).split(".")[0])
    for i in msg_sender:
        sender_eml_type.append((i.split("@")[1]).split(".")[0])    
#    print(msg_to)
#    print(msg_receiver)
#    print(eml_type)
#    print(msg_type)    
    print("Data collection done")
    #"Id":msg_id,'Id':uid,
    email_dataframe = pd.DataFrame({"Id":msg_id,"From":msg_from,"To":msg_to,"Date":msg_dmy,
                                    "Subject":msg_subj,"Text":msg_body,"Sender_Email_Type":sender_msg_type,"Receiver_Email_Type":receiver_msg_type})
    eml_data=pd.DataFrame({'Id':uid,'From':msg_sender,'To':msg_receiver,'Date':eml_dmy,
                           'Subject':subject,'Text':txt,"Sender_Email_Type":sender_eml_type,"Receiver_Email_Type":receiver_eml_type})
    data=email_dataframe.append(eml_data,ignore_index=True)
    
    data.to_csv("parser.csv")
    return data 