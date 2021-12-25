from flask import Flask
from flask_restful import Api
from database.db import initialize_db
from resources.routes import initialize_routes
from config import config_map
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': config_map['mongodb_host']
}

initialize_db(app)
initialize_routes(api, config_map['routing_prefix'])


if __name__ == "__main__":
    app.run(threaded=True, port=5000)

