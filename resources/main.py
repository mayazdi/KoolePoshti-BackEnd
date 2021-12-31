from flask import Response, request
# from database.models import Post
from flask_restful import Resource

class MainApi(Resource):
    def get(self):
        return Response("<h1 style=\"text-align: center;\">Flask webserver working properly</h1>", status=200)
    

class TermsApi(Resource):
    def get(self):
        with open("./terms.txt", "r") as f:
            return Response(f.read(), status=200)