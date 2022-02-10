# Natalman Nahm

from flask import Flask
from flask_restful import Resource, Api
from resources.user import User, Users
import sqlite3
from os.path import exists
from src.migrate_db import init_db
import src.const
from flask import g

app = Flask(__name__)
api = Api(app)

if not exists(src.const.DB_NAME):
    init_db()

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(User, '/users/<string:user_name>', '/users/create')
api.add_resource(Users, '/users')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
