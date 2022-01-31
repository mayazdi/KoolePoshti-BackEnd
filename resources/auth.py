from flask import Response, request, jsonify
from flask_restful import Resource
from database.models import User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from mongoengine.queryset.visitor import Q
from config import config_map
from utils.otp import generate_otp
from utils.mail import send_otp_email
import hashlib
import re
import datetime

class SigninApi(Resource):
    def post(self):
        body = request.get_json()
        try:
            _beheshti_email = body['beheshtiEmail'].lower()
            _password = hashlib.md5("{}{}".format(body['password'], config_map['password_salt']).encode()).hexdigest()
        except Exception:
            return {'error': 'wrong format'}, 400
        # user = User.objects.get(beheshti_email=_beheshti_email)
        user = User.objects(Q(beheshtiEmail=_beheshti_email) & Q(password=_password))
        if user:
            if user[0].active:
                user[0].update(forgotten_password=False)
                access_token = create_access_token(identity=_beheshti_email)
                return jsonify(accessToken=access_token)
            else:
                return {"Error": "User not activated yet"}, 400
        else:
            return {"Error": "User | Password wrong"}, 406


def user_already_exists(body):
    try:
        user = User.objects.get(beheshtiEmail=body['beheshtiEmail'].lower())
        if user:
            return True            
    except:
        pass
    return False

def email_is_from_SBU(email):
    return True
    # return bool(re.match(r"^\S+@(mail\.)?sbu\.ac\.ir$", email))

def body_conatins_email_field(body):
    return 'beheshtiEmail' in body

def body_conatins_password_field(body):
    return 'password' in body

def body_conatins_names_fields(body):
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
                        if body_conatins_names_fields(body):
                            body['password'] = hashlib.md5("{}{}".format(body['password'], config_map['password_salt']).encode()).hexdigest()
                            user = User(**body)
                            user.otp = generate_otp()
                            print(user.otp)
                            send_otp_email(body['beheshtiEmail'], body['firstName'] + ' ' + body['lastName'], user.otp)
                            user.save()
                            id = user.id
                            return {'id': str(id)}, 201
                        else:
                            return {'error': 'lastName or firstName not provided'}, 400
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
        body = request.get_json()
        if 'beheshtiEmail' in body:
            user = User.objects(Q(beheshtiEmail=body['beheshtiEmail'].lower()))
            if user:
                user = user[0]
                user.update(forgotten_password=True, otp=generate_otp())
                send_otp_email(user.beheshtiEmail, user.firstName + ' ' + user.lastName, user.otp)
                return {"msg": "Activation email has been sent"}, 200
            else:
                return {"Error": "User not found"}, 406
        else:
            return {'error' : 'Email not provided'}, 400

class ActivateApi(Resource):
    def post(self):
        body = request.get_json()
        try:
            _beheshti_email = body['beheshtiEmail'].lower()
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
                    send_otp_email(user.beheshtiEmail, user.firstName + ' ' + user.lastName, user.otp)
                    return {"Error": "OTP has been expired!"}, 400
            else:
                return {"Error": "Already activated"}, 400
        else:
            return {"Error": "User not found"}, 406


class ResetPasswordApi(Resource):
    def post(self):
        # TODO: check for JWT. or if user is loggedin
        body = request.get_json()
        if 'beheshtiEmail' in body and 'password' and 'otp' in body:
            user = User.objects(Q(beheshtiEmail=body['beheshtiEmail'].lower()))
            if user:
                # TODO: Check if user has forgotten password
                user = user[0]
                if user.otp == body['otp']:
                    user.update(password=hashlib.md5("{}{}".format(body['password'], config_map['password_salt']).encode()).hexdigest())
                    user.update(forgotten_password=False)
                    access_token = create_access_token(identity=body['beheshtiEmail'].lower())
                    return jsonify(accessToken=access_token)
                else:
                    print(user.otp)
                    return {'error': 'OTP doesnt match'}, 400
            else:
                return {'error': 'User not found'}, 400
        else:
            return {'error': 'email, password or otp not provided'}, 400