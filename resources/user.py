from flask import Response, request, jsonify
from database.models import User
from flask_restful import Resource
from mongoengine.queryset.visitor import Q
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.user import get_user_id, is_post_author
import json


class UserApi(Resource):
    decorators = [jwt_required()]
    
    def get(self):
        user = User.objects.get(beheshtiEmail=get_jwt_identity())
        if user:
            return {
                "githubId" : user.githubId,
                "beheshtiEmail" : user.beheshtiEmail,
                "firstName" : user.firstName,
                "lastName" : user.lastName,
            }, 200
        
    
    def put(self):
        body = request.get_json()
        beheshti_email = get_jwt_identity()
        if beheshti_email:
            if 'firstName' in body or 'lastName' in body:
                user = User.objects.get(beheshtiEmail=beheshti_email)
                if 'firstName' in body:
                    first_name = body['firstName']
                else:
                    first_name = user.firstName
                if 'lastName' in body:
                    last_name = body['lastName']
                else:
                    last_name = user.lastName
                user.update(firstName=first_name, lastName=last_name)
                return {"msg": "User information updated"}, 200
            else:
                return {"Error": "Missing Arguments (firstName or lastName)"}, 400
        else:
            return {"Error": "Not authenticated yet"}, 401