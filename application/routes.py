from bson import encode
from flask import Response, json, request, redirect, url_for
from werkzeug.datastructures import MIMEAccept
from werkzeug.wrappers import response
from functools import wraps
from application import app
from application.model import User
import datetime
import jwt

def token_validate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return redirect(url_for('login'))
        try:
            user_data = jwt.decode(token, app.config['SECRET_KEY'])
            user = User.objects.filter(**{"email":user_data['email']})
            if not user:
                return redirect(url_for('login'))
            else:
                expire_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
                data = {"email":user[0].email,"exp":expire_time}
                payload = jwt.encode(data, app.config['SECRET_KEY'])
                return  f(user[0], payload, *args, **kwargs)
        except Exception as e:
            # print(str(e)) # error signature expired
            return redirect(url_for('login'))
    return decorated

@app.route("/api",methods=["GET"])
def login():
    data = None
    try:
        if request.mimetype == 'application/json':
            user = User.objects.filter(**{"email":request.json['email'],"password":request.json['password']})
            if user:
                expire_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
                data = {"email":user[0].email,"exp":expire_time}
                payload = jwt.encode(data, app.config['SECRET_KEY'])
                return Response(response=json.dumps({"login_response":"authorized as "+user[0].first_name}),headers=[('x-access-token',payload)])
            return Response(response=json.dumps({"login_response":data}))
    except Exception as e:
        return Response(response=json.dumps({"register_status":str(e)}),status=200,mimetype="application/json")
    return Response(response=json.dumps({"register_status":"unauthorized"}),status=200,mimetype="application/json")

@app.route("/api/root",methods=["POST"])
@token_validate
def root(requestor=None,payload=None):
    return Response(response=json.dumps({"user":requestor['first_name'],"apis":['/api/register','/api/login','/api/update_profile','/api/delete_profile','/api/find_profile']}),status=200,mimetype="application/json",headers=[('x-access-token',payload)])


@app.route("/api/register", methods = ['POST'])
def register(requestor=None,payload=None):
    # if request.mimetype == 'application/json':
    try:
        user = User(    
                        phone_no = request.json['phone_no'],
                        first_name = request.json['first_name'],
                        last_name = request.json['last_name'],
                        email = request.json['email'],
                        details = request.json['details'],
                        password = request.json['password']
                    )
        return Response(response=json.dumps({"register_status":user.save()}),status=200,mimetype="application/json",headers=[('x-access-token',payload)])
    except Exception as e:
        return Response(response=json.dumps({"register_status":str(e)}),status=200,mimetype="application/json")


@app.route("/api/update_profile", methods = ['POST'])
@token_validate
def update_user(requestor=None,payload=None):
    # if request.mimetype == 'application/json':
    try:
        field_names = list(request.json['fields_to_update'])
        user = User.objects(email = requestor['email'])
        updated = []
        for afield in field_names:
            if(afield == 'first_name'):
                updated.append(user.update_one(set__first_name=request.json[afield]))
            if(afield == 'last_name'):
                updated.append(user.update_one(set__last_name=request.json[afield]))
            if(afield == 'phone_no'):
                updated.append(user.update_one(set__phone_no=request.json[afield]))
            if(afield == 'details'):
                updated.append(user.update_one(set__details=request.json[afield]))
            if(afield == 'password'):
                updated.append(user.update_one(set__password=request.json[afield]))
        return Response(response=json.dumps({"profile_status":updated}),status=200,mimetype="application/json",headers=[('x-access-token',payload)])
    except Exception as e:
        return Response(response=json.dumps({"profile_status":str(e)}))


@app.route("/api/search_profile", methods = ['POST'])
@token_validate
def search_user(requestor=None,payload=None):
    # if request.mimetype == 'application/json':
    try:
            field = request.json['field_to_search']
            if field == 'first_name':
                users = User.objects(first_name=request.json[field])
            elif field == 'last_name':
                users = User.objects(last_name=request.json[field])
            elif field == 'email':
                users = User.objects(email=request.json[field])
            elif field == 'phone_no':
                users = User.objects(phone_no=request.json[field])
            else:
                return Response(response=json.dumps({"profile_matching":None}),status=200,mimetype="application/json")
            list_user = [[str(user.id),user.email,user.first_name,user.last_name,user.phone_no] for user in users]
            return Response(response=json.dumps({"profile_matching":list_user}),status=200,mimetype="application/json",headers=[('x-access-token',payload)])
    except Exception as e:
        return Response(response=json.dumps({"search_error":str(e)}))


@app.route("/api/delete_profile", methods = ['POST'])
@token_validate
def delete_user(requestor=None,payload=None):
    # if request.mimetype == 'application/json':
    try:
        user = User.objects(email=requestor['email'])
        return Response(response=json.dumps({"delete_records":user.delete()}),status=200,mimetype="application/json",headers=[('x-access-token',payload)])
    except Exception as e:
        return Response(response=json.dumps({"delete_error":str(e)}),status=200,mimetype="application/json")