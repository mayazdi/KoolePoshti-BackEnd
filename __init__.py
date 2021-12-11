from flask import Flask
from flask_restful import Api
from database.db import initialize_db
from resources.routes import initialize_routes

app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/koole-poshti'
}

initialize_db(app)
initialize_routes(api)

@app.route('/')
def index():
    return "salam donya"


if __name__ == "__main__":
    app.run(debug=True)
