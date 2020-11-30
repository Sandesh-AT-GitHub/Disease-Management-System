from flask import Flask,render_template,request,redirect,url_for,session
import requests
from flask_sqlalchemy import SQLAlchemy

import os

app=Flask(__name__)
app.secret_key="sandesh"


#authorization

import hmac, hashlib
import base64
import json

token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InNhbmRlc2hnb3dkYTEzNUBnbWFpbC5jb20iLCJyb2xlIjoiVXNlciIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6IjgxNDMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3ZlcnNpb24iOiIyMDAiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xpbWl0IjoiOTk5OTk5OTk5IiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwIjoiUHJlbWl1bSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbGFuZ3VhZ2UiOiJlbi1nYiIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvZXhwaXJhdGlvbiI6IjIwOTktMTItMzEiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL21lbWJlcnNoaXBzdGFydCI6IjIwMjAtMTEtMTYiLCJpc3MiOiJodHRwczovL3NhbmRib3gtYXV0aHNlcnZpY2UucHJpYWlkLmNoIiwiYXVkIjoiaHR0cHM6Ly9oZWFsdGhzZXJ2aWNlLnByaWFpZC5jaCIsImV4cCI6MTYwNjU2ODI4MSwibmJmIjoxNjA2NTYxMDgxfQ.QPZhWfBLk0ut9sVMe9zaOsIcSCdJhp3xGqqRB_sN8T8"

# from authlib.integrations.requests_client import OAuth2dbsession
# client = OAuth2dbsession(client_id, client_secret, scope=scope)

# authorization_endpoint = 'https://authservice.priaid.ch/login'
# uri, state = client.create_authorization_url(authorization_endpoint)
# print(uri)

# authorization_response = 'https://authservice.priaid.ch/login'
# token_endpoint = 'https://authservice.priaid.ch/login'
# token = client.fetch_token(token_endpoint, authorization_response=authorization_response)
# print(token)

#database

import sqlalchemy
from sqlalchemy import create_engine,Column,Integer,String,Date,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship,backref
from sqlalchemy.ext.declarative import declarative_base


print(sqlalchemy.__version__)

# basedir=os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')

engine = create_engine('sqlite:////home/sandesh/Desktop/DMS_V2/data.sqlite',
connect_args={'check_same_thread': False})

Session = sessionmaker(bind=engine)
dbsession = Session()

Base = declarative_base()

class userDetail(Base):
    __tablename__='user'
    uid=Column(Integer,autoincrement=True,primary_key=True)
    name=Column(String(10),nullable=False,unique=True)
    email=Column(String(20),nullable=False)
    phone=Column(Integer,nullable=False)
    address=Column(String(100),nullable=False)
    password=Column(String(20),nullable=False)
    # userrecord=relationship("healthRecord",backref=backref("userrecord",order_by=id),cascade="all,delete,delete-orphan")

    def __init__(self,name,email,phone,address,password):
        self.name=name
        self.email=email
        self.phone=phone
        self.address=address
        self.password=password

class doctorDetail(Base):
    __tablename__='doctor'
    did=Column(Integer,autoincrement=True,primary_key=True)
    name=Column(String(10),nullable=False,unique=True)
    email=Column(String(20),nullable=False)
    phone=Column(Integer,nullable=False)
    address=Column(String(100),nullable=False)
    password=Column(String(20),nullable=False)
    degree=Column(String(20),nullable=False)
    exp=Column(Integer,nullable=False)
    currentstatus=Column(String(20),nullable=False)
    specialisation=Column(String(20),nullable=False)
    # doctorrecord=relationship("healthRecord",backref=backref("doctorrecord",order_by=id))

    def __init__(self,name,email,phone,address,password,degree,exp,currentstatus,specialisation):
        self.name=name
        self.email=email
        self.phone=phone
        self.address=address
        self.password=password
        self.degree=degree
        self.exp=exp
        self.currentstatus=currentstatus
        self.specialisation=specialisation

class healthRecord(Base):
    __tablename__='healthRecord'
    hid=Column(Integer,primary_key=True)
    uid=Column(Integer, nullable=False)
    did=Column(Integer,nullable=True)
    symptoms=Column(String(100),nullable=False)
    diseases=Column(String(100),nullable=True)
    consultationdate=Column(Date,nullable=True)
    consultateddate=Column(Date,nullable=True)
    prescription=Column(String(100),nullable=True)
    consultationstatus=Column(String(10))

    # ForeignKey("user.uid"),

    def __init__(self,uid,did,symptoms,diseases,consultationdate,consultateddate,prescription,consultationstatus):
        self.uid=uid
        self.did=did
        self.symptoms=symptoms
        self.diseases=diseases
        self.consultationdate=consultationdate
        self.consultateddate=consultateddate
        self.prescription=prescription
        self.consultationstatus=consultationstatus

#login page

@app.route("/")
def home():
    return render_template('home.html')    

@app.route("/patientLogin",methods=["post","get"])
def patientLogin():
    
    if request.method == "POST":
        name=request.form['fullname']
        email=request.form["email"]
        phone=request.form["contact"]
        address=request.form["address"]
        password=request.form["password"]

        addPatient=userDetail(name=name,email=email,phone=phone,address=address,password=password)
        dbsession.add(addPatient)
        dbsession.commit()
    
    return render_template('patientLogin.html')

@app.route("/patientSignup")
def patientSignup():
    return render_template('patientSignup.html')

@app.route("/doctorLogin",methods=["post","get"])
def doctorLogin():
    print(request.method)
    if request.method == "POST":
        name=request.form['fullname']
        email=request.form["email"]
        phone=request.form["contact"]
        address=request.form["address"]
        password=request.form["password"]
        degree=request.form["degree"]
        Prof=request.form["status"]
        exp=request.form["exp"]
        specialisation=request.form["specialisation"]

        addDoctor=doctorDetail(name=name,email=email,phone=phone,address=address,password=password,degree=degree,exp=exp,currentstatus=Prof,specialisation=specialisation)
        dbsession.add(addDoctor)
        dbsession.commit()

    
    return render_template('doctorLogin.html')

@app.route("/doctorSignup")
def doctorSignup():
    return render_template('doctorSignup.html')


#users module

@app.route("/users",methods=["post","get"])
def users():
    
    if request.method == "POST":
        username=request.form["username"]
    
        password=request.form["password"]

        q1=dbsession.query(userDetail).filter(userDetail.name==username).first()
        q2=dbsession.query(userDetail).filter(userDetail.password==password).first()
        
        if q1 == None or q2 == None:
             return "invalid credentials"

        if(username == q1.name and password == q2.password):
            
            q3=dbsession.query(userDetail).filter(userDetail.name==username).first()
            
            session['users']=q3.uid
            print(session['users'])

            return render_template('index.html')
        else:
            return render_template('home.html')
    else:
        return render_template('index.html')
    

@app.route("/users/symptomsList")
def symptomsList():

    payload={'token':token,'language':'en-gb'}
    r=requests.get("https://sandbox-healthservice.priaid.ch/symptoms",params=payload)
    symptomsList=r.json()
    
    return render_template("symptomsList.html",symptoms=symptomsList)

@app.route("/users/diseasePrediction")
def diseasePrediction(): 
    return render_template('diseasePrediction.html')

@app.route("/users/diseaseList",methods=["POST","GET"])
def diseaseList():
    if request.method == 'POST':

        url="https://sandbox-healthservice.priaid.ch/diagnosis?symptoms=["

        symptomsstr=request.form['symptoms']
        gender=request.form['gender']
        age=request.form['age']

        symptoms=symptomsstr.split(',')

        for i in range(0,len(symptoms)-1):
            url+=str(symptoms[i])+","
    
        url=url+str(symptoms[len(symptoms)-1])+"]"
        
        payload={'gender':gender,'year_of_birth':age,'token':token,'language':'en-gb'}

        r=requests.get(url,params=payload)
        diseaseList=r.json() 

        issue=[]
        for diseases in diseaseList:
            issue.append(diseases["Issue"])

        specialisation=[]
        for diseases in diseaseList:
            specialisation.append(diseases["Specialisation"])

        listLen = len(issue)    

        return render_template("diseaseList.html",disease=issue,medications=specialisation,listLen=listLen)

@app.route("/users/consultationList")
def consultationList():

    doctorList=dbsession.query(doctorDetail).all()
    
    return render_template("consultationList.html",doctorList=doctorList)

@app.route("/users/consult")
def consult():

    query=dbsession.query(userDetail).filter(userDetail.uid==session['users']).first()
    user=query.name

    doctor=request.args.get('doctor')

    from datetime import date 
    today=date.today()

    return render_template("consult.html",user=user,date=today,doctor=doctor)

@app.route("/users/usersHealthRecord",methods=['post','get'])
def usersHealthRecord():
    
    if request.method == 'POST':

        symptom=request.form['symptom']
        disease=request.form['disease']
        doctorname=request.form['to']
        query2=dbsession.query(doctorDetail).filter(doctorDetail.name==doctorname).first()
        doctorid=query2.did
        
        from datetime import date
        date=date.today()

        addsymptom=healthRecord(uid=session['users'],did=doctorid,symptoms=symptom,diseases=disease,consultationdate=date,consultateddate=sqlalchemy.sql.null(),prescription=sqlalchemy.sql.null(),consultationstatus='applied')
        dbsession.add(addsymptom)
        dbsession.commit()
    
    query=dbsession.query(healthRecord).filter(healthRecord.uid==session['users'])
    return render_template("usersHealthRecord.html",query=query)
    
#doctors module

@app.route("/doctor",methods=["post","get"])
def doctor():
    if request.method == "POST":
        username=request.form["username"]
    
        password=request.form["password"]

        q1=dbsession.query(doctorDetail).filter(doctorDetail.name==username).first()
        q2=dbsession.query(doctorDetail).filter(doctorDetail.password==password).first()
        
        if q1 == None or q2 == None:
             return "invalid credentials"

        if(username == q1.name and password == q2.password):
            q3=dbsession.query(doctorDetail).filter(doctorDetail.name==username).first()
            session['doctor']=q3.did
            return render_template('doctor.html')
        else:
            return render_template('home.html')
    else:
        return render_template('doctor.html')

@app.route("/doctor/consultationRequestList")
def consultationRequestList():
    query = dbsession.query(healthRecord).filter(healthRecord.did==session['doctor'],healthRecord.consultationstatus=="applied")

    return render_template('consultationRequestList.html',query=query)

@app.route("/doctor/consultationReplyList",methods=["POST","GET"])
def consultationReplyList():
    query1 = dbsession.query(healthRecord).filter(healthRecord.did==session['doctor'],healthRecord.consultationstatus=="seen")
    
    if request.method == 'POST':

        hid=request.form["hid"]    
        prescription=request.form["prescription"]
        
        from datetime import date 
        date=date.today()

        query3=dbsession.query(healthRecord).filter(healthRecord.hid == hid).update({healthRecord.consultateddate:date,healthRecord.prescription:prescription,healthRecord.consultationstatus:'seen'}, synchronize_session = False)
        dbsession.commit()

    return render_template("consultationReplyList.html",query=query1)

@app.route("/doctor/writePrescription")
def writePrescription():
    hid=request.args.get('hid')
    
    query1=dbsession.query(healthRecord).filter(healthRecord.hid==hid).first()

    query2=dbsession.query(doctorDetail).filter(doctorDetail.did==query1.did).first()
    doctor=query2.name


    query3=dbsession.query(userDetail).filter(userDetail.uid==query1.uid).first()
    user=query3.name

    return render_template("writePrescription.html",hid=hid,query=query1,doctor=doctor,user=user)

@app.route("/doctor/patientHealthRecord")
def patientHealthRecord():
    uid=request.args.get('uid')
    
    query=dbsession.query(healthRecord).filter(healthRecord.did==session['doctor'],healthRecord.uid==uid,healthRecord.consultationstatus=='seen').all()

    return render_template("patientHealthRecord.html",query=query)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)