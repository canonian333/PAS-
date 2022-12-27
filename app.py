from flask import Flask 
from flask import render_template
from flask import request
from flask import send_file
from flask import Flask, render_template, request, redirect, url_for,session
import time 
import pandas as pd

import sys

import os, urllib


import pymongo
from pymongo import MongoClient


personGroupId = 'test1'    
UPLOAD_FOLDER="mlFiles"

app = Flask(__name__)
app.secret_key = "basith"
currentDate1 = time.strftime("%d-%m-%y")


cluster = MongoClient("mongodb+srv://DataUser1:DataUser1@cluster0.0r6hn.mongodb.net/database2?retryWrites=true&w=majority")
db = cluster["pas2021"]
Admincollection = db["admin"]
Studentcollection = db["student"] 
Placementcollection = db["placement_cell"]
Companycollection = db["company"]




 
'''@app.route('/download')
def download():
    return send_file('mlFiles/reports_1.csv',
                     mimetype='text/csv',
                     attachment_filename='reports_1.csv',
                     as_attachment=True)
@app.route('/download2')
def download2():
    return send_file('mlFiles/attendance.xlsx',
                     mimetype='text/csv',
                     attachment_filename='attendance.xlsx',
                     as_attachment=True)

@app.route("/predict",methods=["GET","POST"])
def predict():
    print(session["user"])
    if(session["user"]):
        if request.method == "POST":
            image_file = request.files["fileup"]
            
            if image_file:
                image_location=os.path.join(UPLOAD_FOLDER,image_file.filename)
                image_file.save(image_location)
                detect(image_location)
                identify()
                return redirect(url_for('adHome'))
    else:
        return redirect(url_for('SignIn'))
            
    return render_template("upload.html")
'''


@app.route('/index')
def index2():
    return render_template('index2.html')

@app.route('/Logout')
def logout():
    clear()
    return redirect(url_for("signIn"))




@app.route('/phase2')
def phase2():
    return render_template('phase2.html')
     
@app.route('/')
def main():
    clear()
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contactUs')
def contactUs():
    return render_template('contactUs.html')

@app.route('/about')
def about():
    return render_template('about.html')




@app.route('/SignInPl', methods=['GET', 'POST'])
def signInPl():
    
    if request.method == 'POST':
        # Get Form Fields
        _username = request.form['username1'] 
        _password = request.form['password1']      
        # Get user by usernane
        users = Admincollection.find_one({"username":_username}) 
        print(users) # result 1
        
        if(users):
            session["user"]=users["username"]
            password_user=(users["password"])
            if(password_user==_password):
                return redirect(url_for('phase2'))    
           
            else:
                clear()
                return render_template('signin.cell.html',messagebox="../static/js/alertPassword.js")
            
        else:
            return render_template('signin.cell.html',messagebox="../static/js/alertUser.js")
                
    else:
        return render_template('signin.cell.html')
            

@app.route('/SignInCpy', methods=['GET', 'POST'])
def signInCpy():
    
    if request.method == 'POST':
        # Get Form Fields
        _username = request.form['username1'] 
        _password = request.form['password1']      
        # Get user by usernane
        users = Companycollection.find_one({"username":_username}) 
        print(users) # result 1
        
        if(users):
            session["user"]=users["username"]
            password_user=(users["password"])
            if(password_user==_password):
                return redirect(url_for('phase2')) 
            else:
                clear()
                return render_template('signin.company.html',messagebox="../static/js/alertPassword.js")
            
        else:
            return render_template('signin.company.html',messagebox="../static/js/alertUser.js")
                
    else:
        return render_template('signin.company.html')
            


@app.route('/SignIIn', methods=['GET', 'POST'])
def signIIn():
    if request.method == 'POST':
        # Get Form Fields
        _username = request.form['username1'] 
        _password = request.form['password1']      
        # Get user by usernane
        users = Admincollection.find_one({"username":_username}) 
        print(users) # result 1
        
        if(users):
            session["user"]=users["username"]
            password_user=(users["password"])
            if(password_user==_password):
                return redirect(url_for('phase2')) 
            else:
                clear()
                return render_template('signin.admin.html',messagebox="../static/js/alertPassword.js")
            
        else:
            return render_template('signin.admin.html',messagebox="../static/js/alertUser.js")
                
    else:
        return render_template('signin.admin.html')
            
            


@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    
    if request.method == 'POST':
        _email = request.form['email1']
        if (_email):

        # Get Form Fields
            
            _username = request.form['username1'] 
            _password = request.form['password1']      
        # Get user by usernane
            users = Studentcollection.find_one({"username":_username}) 
        
        
        
            print(users) # result 1
        
            if(users):
                return render_template('signin.html',messagebox="../static/js/alertExist.js")
            else:
                usersave = {"username":_username, "password":_password, "email":_email}
                Studentcollection.insert_one(usersave)
                return render_template("register.html",messagebox="../static/js/alertAdded.js")
            
        else:
            
            _username = request.form['username1'] 
            _password = request.form['password1']      
            # Get user by usernane
            users = Studentcollection.find_one({"username":_username}) 
            print(users) # result 1
        
            if(users):
                session["user"]=users["username"]
                password_user=(users["password"])
                if(password_user==_password):
                    return redirect(url_for('phase2'))
                else: 
                    return render_template('signin.html',messagebox="../static/js/alertPassword.js")
            
            else:
                return render_template('signin.html',messagebox="../static/js/alertUser.js")
                
    else:
        return render_template('signin.html')
            


@app.route('/studHome',methods=['POST','GET'])
def studHome():
    if request.method == 'POST'or'GET':
        if "user" in session:
            print(session["user"])
            user=session["user"]
            thour=session["totalhour"]
            tattendance=session["totalattendance"]
            
            if (tattendance or thour !=0):
                percent=int(tattendance/thour*100)
            else:
                percent="None"
            return render_template('student.html',Date=currentDate1, User=user,Thour=thour ,Tattend=tattendance,Percent=percent)
        
        return redirect(url_for('home')) 
    else:
        return redirect(url_for('signIn'))
    



@app.route('/adHome',methods=['POST','GET'])
def adHome():
    if request.method == 'POST'or'GET':
        if "user" in session:
            user=session["user"]
            studno=session["studno"]
            workingdays=session["workingday"]
            if "todayAttendance" in session:
                attendances=session["todayAttendance"]
            else:
                attendances="Not Taken"
        
            return render_template('adminhome.html',Date=currentDate1, User=user,StudNo=studno,Wday=workingdays, Tattend=attendances)
        
        return redirect(url_for('home')) 
    else:
        return render_template('signin.html')
    

     
@app.route('/register',methods=['POST','GET'])

def signUp():     
    
    if request.method == 'POST':

        _name = request.form['username3']
        _password = request.form['password3']
        # validate the received values
        users = Usercollection.find_one({"username":_name})
        if (users):
            return render_template("register.html",messagebox="../static/js/alertExist.js")
                
        else:
            usersave = {"username":_name, "password":_password, "id":"student"}
            Usercollection.insert_one(usersave)
            return render_template("register.html",messagebox="../static/js/alertAdded.js")
                
    else:
        return render_template("signin.admin.html")





def clear():
    print("sessions cleared")
    if "user" in session:  
        print("user : ",session["user"])
        session.pop("user", None)     
        

    if "studno" in session: 
        print("studno : ",session["studno"])
        session.pop("studno", None)

    if "workingday" in session: 
        print("workingday : ",session["workingday"])
        session.pop("workingday", None)

    if "todayAttendance" in session: 
        print("todayAttendance : ",session["todayAttendance"])
        session.pop("todayAttendance" , None)
    if "totalattendance" in session: 
        print("todayAttendance : ",session["totalattendance"])
        session.pop("totalattendance" , None)
    if "totalhour" in session: 
        print("totalhour : ",session["totalhour"])
        session.pop("totalhour" , None)
    if "subno" in session: 
        print("subno : ",session["subno"])
        session.pop("subno" , None)

    
    





if __name__ == '__main__':
    app.run(host="localhost",port=8080, debug=True)