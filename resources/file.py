from flask import Response, request
from database.models import File
from flask_restful import Resource
import io 
from flask.helpers import send_file

class FileApi(Resource):
    def post(self):
        f = request.files['file']
        _file = File()
        _file.data.put(f, filename=f.filename)
        _file.save()
        """ body = request.get_json()
        _file = File(**body).save() """
        id = _file.id
        return {'id': str(id)}, 201
    
class FilesApi(Resource):
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