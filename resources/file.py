from flask import Response, request
from database.models import File
from flask_restful import Resource
from flask.helpers import send_file
from flask_jwt_extended import jwt_required
import io, os
import datetime

def get_file_size(f):
    f.seek(0, os.SEEK_END)
    return f.tell()


class FileApi(Resource):
    decorators = [jwt_required()]
    
    def post(self):
        f = request.files['file']
        _file = File()
        name = str(datetime.datetime.utcnow())+"_"+f.filename
        _file.name = name
        _file.size = get_file_size(f)
        print(_file.size)
        _file.data.put(f, filename=name)
        _file.save()
        id = _file.id
        return {'id': str(id)}, 201
    

class FileDownloadApi(Resource):
    decorators = [jwt_required()]

    def get(self, id):
        _file = File.objects.get(id=id)
        f = _file.data
        content_type = _file.data.content_type
        filename = _file.data.filename
        return send_file(
                io.BytesIO(f.read()),
                attachment_filename=filename,
                mimetype=content_type
            )