from flask import Response, request
# from database.models import Post
from flask_restful import Resource
from flask_cors import cross_origin
from utils.auth0 import requires_auth

class MainApi(Resource):
    @cross_origin(headers=["Content-Type", "Authorization"])
    def get(self):
        return Response("<h1 style=\"text-align: center;\">Flask webserver working properly</h1>", status=200)
    

class TermsApi(Resource):
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self):
        with open("./terms.txt", "r") as f:
            return Response(f.read(), status=200)