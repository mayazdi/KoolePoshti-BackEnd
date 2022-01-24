from flask import Flask
from flask_restful import Api
from resources.routes import initialize_routes
from config import config_map
from flask_cors import CORS, cross_origin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from database.db import initialize_db
from database.utils import clean_db, repopulater_tags
import argparse

def run_server():
    app = Flask(__name__)
    CORS(app, support_credentials=True)
    # CORS(app, resources={r"/*": {"origins": "*"}})

    api = Api(app)
    app.config['MONGODB_SETTINGS'] = {
        'host': config_map['mongodb_host']
    }
    app.config["JWT_SECRET_KEY"] = config_map['jwt_secret_key']
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']

    jwt = JWTManager(app)

    initialize_db(app)
    initialize_routes(api, config_map['routing_prefix'])
    app.run(port=config_map['server_port'], debug=config_map['debug_mode'])
    #threaded=True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Koole-Poshti Backend & utilities')
    FUNCTION_MAP = {'tags' : repopulater_tags, 'clean' : clean_db, 'run' : run_server}
    parser.add_argument('--command', choices=FUNCTION_MAP.keys())
    args = parser.parse_args()
    try:
        func = FUNCTION_MAP[args.command]
        func()
    except Exception as e:
        print(e)