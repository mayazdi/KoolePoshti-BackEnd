from flask import Response, request, jsonify
from database.models import Tag, Category
from flask_restful import Resource
from mongoengine.queryset.visitor import Q
from flask_jwt_extended import jwt_required
import json

class TagApi(Resource):
    decorators = [jwt_required()]
    
    def get(self):
        categories = Category.objects()
        category_ids = [str(c.id) for c in categories]
        print(category_ids)
        tags = {}

        i = 0
        for _id in category_ids:
            tags[categories[i].title] = json.loads(Tag.objects.filter(category=_id).to_json())
            i+=1
        return tags, 200
    
    def post(self):
        body = request.get_json()
        """ import hashlib
        result = hashlib.md5(b'GeeksforGeeks')
        print(result.digest())
        """
        tag = Tag(**body).save()
        id = tag.id
        return {'id': str(id)}, 201


class CategoryApi(Resource):
    decorators = [jwt_required()]

    def get(self):
        categories = Category.objects().to_json()
        return Response(categories, mimetype="application/json", status=200)
    
    def post(self):
        body = request.get_json()
        category = Category(**body).save()
        id = category.id
        return {'id': str(id)}, 201
