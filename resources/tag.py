from flask import Response, request, jsonify
from database.models import Tag, Category
from flask_restful import Resource
from mongoengine.queryset.visitor import Q
from flask_jwt_extended import jwt_required
import json

class TagApi(Resource):
    decorators = [jwt_required()]
    
    def post(self):
        body = request.get_json()
        """ import hashlib
        result = hashlib.md5(b'GeeksforGeeks')
        print(result.digest())
        """
        tag = Tag(**body).save()
        id = tag.id
        return {'id': str(id)}, 201


def get_tag(tag):
    return {
        "id" : str(tag.id),
        "name" : tag.name,
        "color" : tag.color
    }

def get_tags(tags):
    tgs = []
    for tag in tags:
        tgs.append(get_tag(tag))
    return tgs


class CategoryApi(Resource):
    decorators = [jwt_required()]

    def get(self):
        categories = Category.objects()
        category_list = []
        for cat in categories:
            category_list.append({
                "id" : str(cat.id),
                "tags" : get_tags(Tag.objects.filter(category=str(cat.id))),
                "title" : cat.title,
            })
        
        categories = {"categories" : category_list}
        return category_list, 200
    
    
    def post(self):
        body = request.get_json()
        category = Category(**body).save()
        id = category.id
        return {'id': str(id)}, 201
