from flask import Response, request, jsonify
from flask_restful import Resource
from opengraph import OpenGraph
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required


class MainApi(Resource):
    @cross_origin(headers=["Content-Type", "Authorization"])
    def get(self):
        return Response("<h1 style=\"text-align: center;\">Flask webserver working properly</h1>", status=200)
    

class TermsApi(Resource):
    @cross_origin(headers=["Content-Type", "Authorization"])
    def get(self):
        with open("./terms.txt", "r") as f:
            return {"content": f.read()}, 200
            # return Response({"content": f.read()}, status=200)


class OGApi(Resource):
    decorators = [jwt_required()]
    
    def get(self, user, repository):
        og = OpenGraph(url="https://github.com/{}/{}".format(user, repository))
        return {'openGraph': og._data}, 200


