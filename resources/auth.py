from flask import Response, request, jsonify
from flask_restful import Resource
from database.models import User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from mongoengine.queryset.visitor import Q
from config import config_map
import hashlib
import re
import datetime

class SigninApi(Resource):
    def post(self):
        body = request.get_json()
        try:
            _beheshti_email = body['beheshtiEmail']
            _password = hashlib.md5("{}{}".format(body['password'], config_map['password_salt']).encode()).hexdigest()
        except Exception:
            return {'error': 'wrong format'}, 400
        print("pedasag")
        # user = User.objects.get(beheshti_email=_beheshti_email)
        user = User.objects(Q(beheshtiEmail=_beheshti_email) & Q(password=_password))
        if user:
                access_token = create_access_token(identity=_beheshti_email)
                return jsonify(access_token=access_token)
            else:
            return {"Error": "User | Password wrong"}, 406


def user_already_exists(body):
    try:
        user = User.objects.get(beheshtiEmail=body['beheshtiEmail'])
        if user:
            return True            
    except:
        pass
    return False

def email_is_from_SBU(email):
    return bool(re.match(r"^\S+@(mail\.)?sbu\.ac\.ir$", email))

def body_conatins_email_field(body):
    return 'beheshtiEmail' in body

def body_conatins_password_field(body):
    return 'password' in body

class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        if body_conatins_email_field(body):
            if user_already_exists(body):
                return {'error': 'user already exists'}, 409
            else:
                if email_is_from_SBU(body['beheshtiEmail']):
                    if body_conatins_password_field(body):
                        body['password'] = hashlib.md5("{}{}".format(body['password'], config_map['password_salt']).encode()).hexdigest()
                        user = User(**body).save()
                        id = user.id
                        return {'id': str(id)}, 201
                    else:
                        return {'error': 'password not provided'}, 400        
                else:
                    return {'error' : 'Email doesn\'t match beheshti'}, 400
        else:
            return {'error' : 'Email not provided'}, 400
    
    # @app.route("/protected", methods=["GET"])
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)
        return {'logged_in_as' : current_user}, 200


class ForgotApi(Resource):
    def post(self):
        return {'status' : 'to be implemented'}, 200

class ActivateApi(Resource):
    def post(self):
        body = request.get_json()
        try:
            _beheshti_email = body['beheshtiEmail']
            otp = body['otp']
        except Exception:
            return {'error': 'wrong format'}, 400
        user = User.objects(Q(beheshtiEmail=_beheshti_email))
        if user:
            if not user[0].active:
                if user[0].otp_valid_date >= datetime.datetime.utcnow():
                    if user[0].otp == otp:
                        # user.active = True
                        user.update(active=True)
                        return {"msg": "User activated successfully!"}, 200
                    else:
                        return {"Error": "Wrong OTP!"}, 400
                else:
                    user.otp = generate_otp()
                    user.otp_valid_date = datetime.datetime.utcnow() + datetime.timedelta(days=1)
                    user.update()
                    print(user.otp)
                    send_otp_email(user.beheshtiEmail, user.firstName + ' ' + user.lastName, user.otp)
                    return {"Error": "OTP has been expired!"}, 400
            else:
                return {"Error": "Already activated"}, 400
        else:
            return {"Error": "User not found"}, 406
