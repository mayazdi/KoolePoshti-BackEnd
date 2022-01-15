from flask import Response, request, jsonify
from flask_restful import Resource
from database.models import User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from mongoengine.queryset.visitor import Q
import hashlib

class SigninApi(Resource):
    def post(self):
        body = request.get_json()
        try:
            _beheshti_email = body['beheshti_email']
            _password = hashlib.md5(body['password'].encode()).hexdigest()
        except Exception:
            return "wrong format", 400
        print("pedasag")
        # user = User.objects.get(beheshti_email=_beheshti_email)
        user = User.objects(Q(beheshti_email=_beheshti_email) & Q(password=_password))
        if user:
            access_token = create_access_token(identity=_beheshti_email)
            return jsonify(access_token=access_token)
        else:
            return {"Error": "User | Password wrong"}, 406


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        try:
            user = User.objects(Q(beheshti_email=body['beheshti_email']))
            if user:
                return {'error': 'user already exists'}, 409
        except:
            pass

        try:
            body['password'] = hashlib.md5(body['password'].encode()).hexdigest()
            # body['password'] = body['password']
            # print(body['password'])
            # print(type(body['password']))
        except Exception:
            return {'error': 'password not provided'}, 400
        user = User(**body).save()
        id = user.id
        return {'id': str(id)}, 201
    
    # @app.route("/protected", methods=["GET"])
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)
        return {'logged_in_as' : current_user}, 200


class ForgotApi(Resource):
    def post(self):
        return {'status' : 'to be implemented'}, 200