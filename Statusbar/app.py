from flask import Flask, request, jsonify
from uuid import uuid1,uuid4
import os, json, pytz
from datetime import date,datetime,timedelta
import pandas as pd

db={}
db_filename="db.json"

#create the object of the flask
app=Flask(__name__)

#check wheather db.json exists in the directory or not
if os.path.exists(db_filename):
    with open(db_filename,'r') as f:
        db=json.load(f)
else:
    db={
        "users":[]
    }
    with open(db_filename,'w+') as f:
        json.dump(db,f,indent=4)

#signup function
@app.route("/signup",methods=['POST'])
def signup():
    if request.method=='POST':
        name=request.form['name']
        username=request.form['username']
        password=request.form['password']
        status=''

        user_dict={
            'name':name,
            'password':password,
            'username':username,
            'status':status
        }
        
        if len(db['users'])==0 or username not in [users["username"] for users in db['users']]:
            db['users'].append(user_dict)

            with open(db_filename,'r+') as f:
                f.seek(0)
                json.dump(db,f,indent=4)
            return "User added successfully"
        else:
            return "User already exists"
    else:
        return "Method not allowed"

#login user
@app.route("/login",methods=['POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        for user in db['users']:
            if username==user['username'] and password==user['password']:
                response={
                    "message":"Login Successful",
                    "Logged in as":db['users'][username],
                    "user_number":db['users'].index(user)
                }
                
                return response
            else:
                continue
    return "Invalid username or password"

#post status
@app.route('/add_status',methods=['POST'])
def add_status():
    user_number=int(request.form['user_number'])
    status=request.form['status']

    if db['users'][user_number]['status']=='':
        db['users'][user_number]['status']=add_status
        with open(db_filename,'r+') as f:
            f.seek(0)
            json.dump(db,f,indent=4)

#update status

#delete status

#get status

#run the flask
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)