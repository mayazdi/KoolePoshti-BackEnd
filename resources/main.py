from flask import Response, request, jsonify
# from database.models import Post
from flask_restful import Resource
from opengraph import OpenGraph
import json
from flask_cors import cross_origin
from utils.auth0 import requires_auth
from database.models import User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from mongoengine.queryset.visitor import Q
import hashlib

class MainApi(Resource):
    @cross_origin(headers=["Content-Type", "Authorization"])
    def get(self):
        return Response("<h1 style=\"text-align: center;\">Flask webserver working properly</h1>", status=200)
    

class TermsApi(Resource):
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self):
        with open("./terms.txt", "r") as f:
            return {"content": f.read()}, 200
            # return Response({"content": f.read()}, status=200)


class OGApi(Resource):
    def get(self, user, repository):
        og = OpenGraph(url="https://github.com/{}/{}".format(user, repository))
        return {'openGraph': og._data}, 200


class LoginApi(Resource):
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


class SigninApi(Resource):
    def post(self):
        body = request.get_json()
        try:
            body['password'] = hashlib.md5(body['password'].encode()).hexdigest()
            # body['password'] = body['password']
            # print(body['password'])
            # print(type(body['password']))
        except Exception:
            return "wrong", 400
        user = User(**body).save()
        id = user.id
        return {'id': str(id)}, 201
    
    # @app.route("/protected", methods=["GET"])
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)
        return {'logged_in_as' : current_user}, 200
