from flask import Response, request, jsonify
# from database.models import Post
from flask_restful import Resource
from opengraph import OpenGraph
import json

class MainApi(Resource):
    def get(self):
        return Response("<h1 style=\"text-align: center;\">Flask webserver working properly</h1>", status=200)
    

class TermsApi(Resource):
    def get(self):
        with open("./terms.txt", "r") as f:
            return Response(f.read(), status=200)


class OGApi(Resource):
    def get(self, user, repository):
        og = OpenGraph(url="https://github.com/{}/{}".format(user, repository))
        return {'openGraph': og._data}, 200
        # return Response(jsonify(json.loads(str(og).replace("'", '"'))), status=200)
