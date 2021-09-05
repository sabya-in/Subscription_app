from flask import Response, json, request
from werkzeug.datastructures import MIMEAccept
from werkzeug.wrappers import response
from application import app
from application.model import User


@app.route("/api")

@app.route("/api/root")
def root():
    return Response(response=json.dumps({"apis":['register','login','update_profile','delete_profile','find_profile']}),status=200,mimetype="application/json")

@app.route("/api/register", methods = ['POST'])
def register():
    try:
        if request.mimetype == 'application/json':
            user = User(    
                            phone_no = request.json['phone_no'],
                            first_name = request.json['first_name'],
                            last_name = request.json['last_name'],
                            email = request.json['email'],
                            details = request.json['details'],
                            password = request.json['password']
                        )
            return Response(response=json.dumps({"register_status":user.save()}),status=200,mimetype="application/json")
        else:
            return Response(response=json.dumps({"register_status":"None"}),status=200,mimetype="application/json")
    except Exception as e:
        return Response(response=json.dumps({"register_status":str(e)}),status=200,mimetype="application/json")

@app.route("/api/login")
def login():
    return Response(response=json.dumps({"login_status":None}),status=200,mimetype="application/json")

@app.route("/api/update_profile", methods = ['POST'])
def update_user():
    try:
        if request.mimetype == 'application/json':
            field_names = list(request.json['fields_to_update'])
            user = User.objects(email = request.json['email'])
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
            return Response(response=json.dumps({"profile_status":updated}),status=200,mimetype="application/json")
        else:
            return Response(response=json.dumps({"profile_status":None}),status=200,mimetype="application/json")
    except Exception as e:
        return Response(response=json.dumps({"profile_status":str(e)}))

@app.route("/api/search_profile", methods = ['POST'])
def search_user():
    try:
        if request.mimetype == 'application/json':
            field = request.json['field_to_search']
            if field == 'first_name':
                users = User.objects(first_name=request.json[field])
            if field == 'last_name':
                users = User.objects(last_name=request.json[field])
            if field == 'email':
                users = User.objects(email=request.json[field])
            if field == 'phone_no':
                users = User.objects(phone_no=request.json[field])
            list_user = [[str(user.id),user.email,user.first_name,user.last_name,user.phone_no] for user in users]
            return Response(response=json.dumps({"profile_matching":list_user}),status=200,mimetype="application/json")
        else:
            return Response(response=json.dumps({"profile_matching":None}),status=200,mimetype="application/json")
    except Exception as e:
        return Response(response=json.dumps({"search_error":str(e)}))

@app.route("/api/delete_profile", methods = ['POST'])
def delete_user():
    try:
        user = User.objects(email=request.json['email'])
        return Response(response=json.dumps({"delete_records":user.delete()}),status=200,mimetype="application/json")
    except Exception as e:
        return Response(response=json.dumps({"delete_error":str(e)}),status=200,mimetype="application/json")
