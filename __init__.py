from flask import Flask
from flask_restful import Api
from database.db import initialize_db
from resources.routes import initialize_routes
from config import config_map

app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': config_map['mongodb_host']
}

initialize_db(app)
initialize_routes(api)

@app.route('/')
def index():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=config_map['debug_mode'], port=config_map['port'])
