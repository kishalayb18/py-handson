from flask import Flask, request, jsonify
from uuid import uuid1,uuid4
import os, json, pytz
from datetime import date,datetime,timedelta
import pandas as pd

db={}
db_filename="db.json"

#check wheather db.json exists in the directory or not
if os.path.exists(db_filename):
    with open(db_filename,'r') as f:
        db=json.load(f)
else:
    access_key=str(uuid1())
    secret_key=str(uuid4())
    item_types=[
        "Food","Beverages","Clothing","Stationaries","Electronic Devices","Weareables"
    ]
    db={
        "access_key":access_key,
        "secret_key":secret_key,
        "item_types":item_types,
        "users":[]
    }
    with open(db_filename,'w+') as f:
        json.dump(db,f,indent=4)
    
app=Flask(__name__) #object of flask

#signup function
@app.route("/signup",methods=['POST'])
def signup():
    if request.method=='POST':
        # print(request.form)
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        username=request.form['username']

        user_dict={
            'name':name,
            'email':email,
            'password':password,
            'username':username,
            'purchases':{}
        }
        
        if len(db['users'])==0 or email not in [users["email"] for users in db['users']]:
            db['users'].append(user_dict)

            with open(db_filename,'r+') as f:
                f.seek(0)
                json.dump(db,f,indent=4)
            return "User added successfully"
        else:
            return "User already exists"
    return "Method not allowed"

#login user
@app.route("/login",methods=['POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        for user in db['users']:
            if email==user['email'] and password==user['password']:
                response={
                    "message":"Login Successful",
                    "user_index":db['users'].index(user)
                }
                
                return response
            else:
                continue
    return "Invalid email or password"
    
#add purchase
@app.route('/add_purchase',methods=['POST'])
def add_purchase():
    if request.method=='POST':
        user_idx=int(request.form['user_index'])
        item_type=request.form['item_type']
        item_price=request.form['item_price']
        item_name=request.form['item_name']

        curr_date=str(date.today())
        curr_time=str(datetime.now(pytz.timezone("Asia/Kolkata")))
        item_dict={
            "item_name":item_name,
            "item_type":item_type,
            "item_price":item_price,
            "purchase_time":curr_time
        }
        if item_type in db['item_types']:
            if db['users'][user_idx]['purchases'].get(curr_date,0)==0:
                db['users'][user_idx]['purchases'][curr_date]=[]
            db['users'][user_idx]['purchases'][curr_date].append(item_dict)
            with open(db_filename,'r+') as f:
                f.seek(0)
                json.dump(db,f,indent=4)

            return "Item added successfully"
        else:
            return "Invalid Item"

#Get todat's purchases
@app.route("/get_today_purchase",methods=['GET'])
def get_today_purchase():
    user_idx=int(request.args['user_index'])
    curr_date=str(date.today())

    if curr_date not in db['users'][user_idx]['purchases']:
        return "No purchase today"
    else:
        # return { "response":db['users'][user_idx]['purchases'][curr_date]}
        return jsonify(response=db['users'][user_idx]['purchases'][curr_date])

@app.route("/hello",methods=['GET'])
def hello():
    token= int(request.args["user_index"])
    greetings=request.args["greet"]
    return greetings+" "+db["users"][token]["name"]

#get purchases between a range of dates    
@app.route("/get_purchases_from_to",methods=['GET'])
def get_purchases_from_to():
    data=request.json
    
    user_idx=data['user_index']
    start_dt=data['start_date']
    end_dt=data['end_date']

    date_list=pd.date_range(start_dt,end_dt) #fetch range of dates
    purchase_dict={}
    
    for date in db['users'][user_idx]['purchases'].keys():
        if date in date_list:
            purchase_dict[date]=db['users'][int(data['user_index'])]['purchases'][date]
    
    if len(purchase_dict)==0:
        return "No purchases in this duration"

    return purchase_dict

@app.route("/get_average_amount_of_purchase",methods=['GET'])
def average_amount_of_purchase():
    pass

# hosting of the server
# default port 8080
# debug true will help to refresh the server without restarting it
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)