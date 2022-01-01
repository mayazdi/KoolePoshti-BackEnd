from flask import Flask
from flask_restful import Api
from database.db import initialize_db
from resources.routes import initialize_routes
from config import config_map
from flask_cors import CORS, cross_origin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__)
CORS(app, support_credentials=True)
# CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': config_map['mongodb_host']
}
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']

jwt = JWTManager(app)

initialize_db(app)
initialize_routes(api, config_map['routing_prefix'])


if __name__ == "__main__":
    app.run(port=config_map['server_port'], debug=config_map['debug_mode'])
    #threaded=True

