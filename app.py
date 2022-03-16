# Natalman Nahm
# Arica Conrad
# Mackenzie Fear

# Arica: I followed this tutorial for comments and error trapping:
# https://dev.to/imdhruv99/flask-user-authentication-with-jwt-2788

from flask import Flask, jsonify, make_response, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager, jwt_required
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import uuid
import jwt
import datetime
from flask_restful import Resource, Api
from resources.user import User, Users, Staff, AllStaff
import sqlite3
from os.path import exists
from src.migrate_db import init_db
import src.const
from flask import g
from src.db import get_db
# Arica: Could comment out Logout, but I left it for now so that I could check if the tokens are being deleted.
from resources.auth import Login, Logout, Token
from resources.rooms import Room, Rooms
# Arica: Import the Tasks and Task classes from the tasks.py file.
from resources.tasks import Tasks, Task
from resources.assignments import Assignments, Assignment

# Arica: Making the Flask application.
app = Flask(__name__)

# Arica: An object of the Api class.
api = Api(app)
bcrypt = Bcrypt(app)

# Arica: Configuring the application.
#app.config.from_envvar('ENV_FILE_LOCATION')
app.config['JWT_SECRET_KEY'] = 'something'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///example.db'

# Arica: The JWTManager object.
jwt = JWTManager(app)

if not exists(src.const.DB_NAME):
    init_db()

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

# def token_required(f):
#    @wraps(f)
#    def decorator(*args, **kwargs):
#        token = None
#        if 'x-access-tokens' in request.headers:
#            token = request.headers['x-access-tokens']
 
#        if not token:
#            return jsonify({'message': 'a valid token is missing'})
#        try:
#            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#            current_user = Users.query.filter_by(public_id=data['public_id']).first()
#        except:
#            return jsonify({'message': 'token is invalid'})
 
#        return f(current_user, *args, **kwargs)
#    return decorator

# Arica: Added an "s" to the end of every endpoint for consistency.
# Could comment out Logout, but I left it for now so that I could check if the tokens are being deleted.
api.add_resource(HelloWorld, '/')
api.add_resource(User, '/users/<user_name>', '/signup')
api.add_resource(Users, '/users', '/users/<string:user_name>')
api.add_resource(Login, '/login')
api.add_resource(Logout,'/logout')
api.add_resource(Token,'/token')
api.add_resource(Room, '/rooms/<string:room_no>', '/room')
api.add_resource(Rooms, '/rooms')
api.add_resource(AllStaff, '/staff')
api.add_resource(Staff, '/staff/<staffid>')
api.add_resource(Tasks, '/tasks')
api.add_resource(Task, '/tasks/<taskid>')
api.add_resource(Assignments, '/assignments')
api.add_resource(Assignment, '/assignments/<string:assignid>')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
