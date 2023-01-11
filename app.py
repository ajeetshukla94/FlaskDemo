from flask import Flask, render_template, flash, url_for, request, make_response, jsonify, session,send_from_directory
from werkzeug.utils import secure_filename
import os, time
import io
import base64
import json
import datetime
import os, sys, glob
from flask import send_file
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from fnmatch import fnmatch
import time
import random
import pandas as pd
import flask



app = Flask(__name__)
app.secret_key = 'file_upload_key'
MYDIR = os.path.dirname(__file__)
print("MYDIR",MYDIR)

app.config['UPLOAD_FOLDER']   = "static/inputData/"
document_type_list            = ["CLASSIFIED A","CLASSIFIED B","CLASSIFIED C","CLASSIFIED D"]
visibility_list               = ["INTERNAL","EXTERNAL","PUBLIC"]

sent_mail                     = False
server                        = 'smtp-mail.outlook.com'
port                          =  587
username                      = "pinpointengineers@hotmail.com"
password                      = "#############@12"
send_from                     = "pinpointengineers@hotmail.com"
send_to                       = "ashish@pinpointengineers.co.in"

def send_mail(subject,text,files,file_name,isTls=True):
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = subject
        msg.attach(MIMEText(text))
        if file_name!="":
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(files, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={}.xlsx'.format(file_name))
            msg.attach(part)
            
        smtp = smtplib.SMTP(server, port)
        if isTls:
            smtp.starttls()
        smtp.login(username,password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()
        
#################################### Start Login logout add user ######################################       
@app.route("/")
def render_default():
    if 'user' in session:
        session_var = session['user']
        if session_var["role"] == "DOCUMENTCELL":
            default_page = "DOCUMENTCELL/upload_document.html"
        return make_response(render_template(default_page,msg = False, 
                             err = False, warn = False,
                             document_type_list=document_type_list,visibility_list=visibility_list,
                             role = session_var["role"]),200)     
    return make_response(render_template('LOGIN_PAGE/login.html'),200)
    
@app.route("/render_login", methods=["GET", "POST"])
def render_login():
    if request.method == 'POST':
    
      form_data  = request.form
      login_id   = form_data['login'].lower()
      passworwd  = form_data['password']
      print(login_id,passworwd)
      
      account             = {"role": "", "password": "",'username':""}
      account["role"]     = "DOCUMENTCELL"
      account["password"] = "abc"
      account["username"] = "abc"
      enc_pass="abc"
      if(enc_pass == account["password"]):
          session_var = {"user": login_id, "role": account["role"],"username": account["username"]}
          session['user'] = session_var
          if account["role"] == "DOCUMENTCELL":
              default_page = "DOCUMENTCELL/upload_document.html"
          return make_response(render_template(default_page,msg = False, 
                             err = False, warn = False,
                             document_type_list=document_type_list,visibility_list=visibility_list,
                             role = session_var["role"]),200)  
      else:
          flash('Invalid Credentials')
          return make_response(render_template("LOGIN_PAGE/login.html", msg = False, err = True, warn = False),403)
    else:
        print('get request')
        
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('selected_file', None)
    flash('Logout Successful')
    return make_response(render_template("LOGIN_PAGE/login.html",msg = True, 
            err = False, warn = False,message='Logout Successful'),200)
            
            

@app.route("/uploadDocument",methods=['GET', 'POST'] )    
def uploadDocument():
    if 'user' in session:
        data            = request.form.get('params_data')
        data            = json.loads(data)    
        observation     = data['observation']
        temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
        temp_df         = temp_df[['DOCUMENT_TYPE','VISIBILITY_TYPE','COMMENT']]
        print(temp_df)  
        d = {"error":"none","msg":"Document uploaded successfully"}   
        return flask.jsonify(d)    
    return make_response(render_template('LOGIN_PAGE/login.html',msg = True, 
            err = False, warn = False,message='Logout Successful'),200)    

if __name__ == '__main__':
    app.debug = True
    app.run()

