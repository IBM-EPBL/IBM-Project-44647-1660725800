import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
from functools import wraps
from http.client import HTTPException
import numpy as np
from flask import Flask, request, render_template,session, url_for,redirect,flash
import json
import pickle
import inputScript
from passlib.hash import  pbkdf2_sha256
import json
import inputScript 
import ibm_db
app = Flask(__name__,template_folder='../Flask')
model = pickle.load(open('../Flask/Phishing_Website.pkl','rb'))


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
conn = ibm_db.connect(os.environ.get('IBMDB_URL'),'','')
SECRET_KEY = os.environ.get("SECRET_KEY")
app.secret_key= SECRET_KEY
carouselDataFile = open('./static/json/carouselData.json')
carouselData = json.load(carouselDataFile)
aboutDataFile = open('./static/json/aboutData.json')
aboutData = json.load(aboutDataFile)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if('logged_in' in session):
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap


def start_session(userInfo):
    del userInfo['password']
    session['logged_in']=True
    session['user']=userInfo
    session['predicted']=False
    return redirect(url_for('index'))


@app.route('/login/',methods=['POST'])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        verify_account = "SELECT * FROM account WHERE email =?"
        stmt = ibm_db.prepare(conn, verify_account)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        fetch_account = ibm_db.fetch_assoc(stmt)
        if(fetch_account):
            if(pbkdf2_sha256.verify(password,fetch_account['PASSWORD'])):
                userInfo={
                    "fullName":fetch_account['FULLNAME'],
                    "email":fetch_account['EMAIL'],
                    "phoneNumber":fetch_account['PHONENUMBER'],
                    "password":fetch_account['PASSWORD'],
                }
                return start_session(userInfo)
            else:
                flash("Password is incorrect","loginError")
                return redirect(url_for('index',loginError=True))
        flash("Sorry, user with this email id does not exist","loginError")
        return redirect(url_for('index',loginError=True))


@app.route('/signup/',methods=['POST'])
def signup():
    if request.method=="POST":
        userInfo={
        "fullName":request.form.get('fullName'),
        "email":request.form.get('email'),
        "phoneNumber":request.form.get('phoneNumber'),
        "password":request.form.get('password'),
        }
        userInfo['password']=pbkdf2_sha256.encrypt(userInfo['password'])
        sql = "SELECT * FROM account WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,userInfo['email'])
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            flash("Sorry,user with this email already exist","signupError")
            return redirect(url_for('index',signupError=True))
        else:
            insert_sql = "INSERT INTO  account(fullName, email, phoneNumber, password) VALUES (?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, userInfo['fullName'])
            ibm_db.bind_param(prep_stmt, 2, userInfo['email'])
            ibm_db.bind_param(prep_stmt, 3, userInfo['phoneNumber'])
            ibm_db.bind_param(prep_stmt, 4, userInfo['password'])
            ibm_db.execute(prep_stmt)
            return start_session(userInfo)     
    flash("Signup failed","signupError")
    return redirect(url_for('index',signupError=True))


@app.route('/logout/',methods=["GET"])
def logout():
    if request.method=="GET":
        session.clear()
    return redirect(url_for('index'))


@app.route('/')
def index():
    if(session and '_flashes' in dict(session)):
        loginError=request.args.get('loginError')
        signupError=request.args.get('signupError')
        if(loginError):
            return render_template('./index.html',loginError=loginError,carousel_content=carouselData['carousel_content'],currentYear=datetime.date.today().year)
        if(signupError):
            return render_template('./index.html',signupError=signupError,carousel_content=carouselData['carousel_content'],currentYear=datetime.date.today().year)
    if(session and '_flashes' not in dict(session)):
        if(session['logged_in']==True):
            return render_template('./index.html',userInfo=session['user'],carousel_content=carouselData['carousel_content'],currentYear=datetime.date.today().year)
        else:
            return render_template('./index.html',carousel_content=carouselData['carousel_content'],currentYear=datetime.date.today().year)
    else:
        return render_template('./index.html',carousel_content=carouselData['carousel_content'],currentYear=datetime.date.today().year)



@app.route('/detect/', methods=['GET','POST'])
@login_required
def predict():
    if request.method == 'POST':
        title=request.form['title']
        url = request.form['url']
        checkprediction = inputScript.main(url)
        prediction = model.predict(checkprediction)
        output=prediction[0]
        session['predicted']=True
        print(output)
        if(output==1):
            pred = "Wohoo! You are good to go."
            session['status']='safe'
            session['pred'] = pred
        else:
            pred = "Oh no! This is a Malicious URL"
            session['status']='unsafe'
            session['pred'] = pred
        session['title']=title
        session['url']=url
        insert_detection_info_stmt="INSERT INTO DETECTIONHISTORY(email,title,url,status) VALUES(?,?,?,?)"
        insert_detection_info = ibm_db.prepare(conn, insert_detection_info_stmt)
        ibm_db.bind_param(insert_detection_info,1,session['user']['email'])
        ibm_db.bind_param(insert_detection_info,2,session['title'])
        ibm_db.bind_param(insert_detection_info,3,session['url'])
        ibm_db.bind_param(insert_detection_info,4,session['status'])
        ibm_db.execute(insert_detection_info)
        if(session and session['logged_in']):
            if(session['logged_in']==True):
                return redirect(url_for('predictionResult'))
    if request.method == 'GET':
        return render_template('./templates/predict-form.html',userInfo=session['user'])


@app.route('/detection-result/')
@login_required
def predictionResult():
    if(session['predicted']==True):
        urlInfo={
        'message' :session['pred'] ,
        'title':session['title'],
        'url':session['url'],
        'status':session['status']
        }        
        return render_template("./templates/prediction-result.html", urlInfo=urlInfo,userInfo=session['user'])
    else:
        return redirect(url_for('predict'))


@app.route('/detection-history/')
@login_required
def detectionHistory():
    if(session and session['logged_in']):
        if(session['logged_in']==True):
            get_detection_history_stmt = "SELECT title,url,status FROM detectionHistory where email=?"
            get_detection_history = ibm_db.prepare(conn, get_detection_history_stmt)
            ibm_db.bind_param(get_detection_history,1,session['user']['email'])
            ibm_db.execute(get_detection_history)
            fetch_detection_history = ibm_db.fetch_assoc(get_detection_history)
            detection_history = []
            ind = 0
            while fetch_detection_history != False:
                detection_history.append(fetch_detection_history)
                ind += 1
                fetch_detection_history = ibm_db.fetch_assoc(get_detection_history)
            detection_history= detection_history[::-1]
            return render_template('./templates/detection-history.html',userInfo=session['user'],detectionHistory=detection_history)


@app.route('/about/')
def about():
    if(session and session['logged_in']):
        if(session['logged_in']==True):
            return render_template('./templates/about.html',userInfo=session['user'],aboutContents=aboutData['aboutContents'])
        else:
            return render_template('./templates/about.html',aboutContents=aboutData['aboutContents'])
    else:
        return render_template('./templates/about.html',aboutContents=aboutData['aboutContents'])



@app.route('/contact/')
def contact():
        if(session and session['logged_in']):
            if(session['logged_in']==True):
                return render_template('./templates/contact.html',userInfo=session['user'])
            else:
                return render_template('./templates/contact.html')
        else:
            return render_template('./templates/contact.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
    