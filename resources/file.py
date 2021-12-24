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
        # f = _file.data.read()
        content_type = _file.data.content_type
        filename = _file.data.filename
        # return Response(f, mimetype=content_type, status=200, direct_passthrough=True)
        return send_file(
                        io.BytesIO(f.read()),
                        attachment_filename=filename,
                        mimetype=content_type
                )
        """ with open("T.pdf", 'rb') as bites:
            return send_file(
                         io.BytesIO(bites.read()),
                         attachment_filename="T.pdf",
                         mimetype='application/pdf'
                   ) """
        """ return send_file(
            path_or_file=f,
            mimetype=content_type,
            # as_attachment=True,
            download_name=filename,
            attachment_filename=filename
        ) """
        """ return send_file(
                     io.BytesIO(f),
                     attachment_filename='logo.jpeg',
                     mimetype=content_type,
                     as_attachment=True), 200 """
        """ return send_file(
            BytesIO(f),
            attachment_filename=filename,
            mimetype=content_type), 200 """
        
        
        """ if post:
            status_code = 200
        else:
            status_code = 404
        return Response(post, mimetype='application/json', status=status_code) """