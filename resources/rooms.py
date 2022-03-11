from datetime import date
from flask_restful import Resource, reqparse
from flask import jsonify#, request, abort, g, url_for
from src.db import get_db
from werkzeug.security import generate_password_hash,check_password_hash
#from passlib.apps import custom_app_context as pwd_context
#from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

parser = reqparse.RequestParser()

class Room(Resource): 

    def get(self, room_no):

        result = get_db().cursor().execute(f'SELECT * FROM rooms WHERE roomnumber="{room_no}"')
        row = result.fetchone()
        return dict(zip([c[0] for c in result.description], row))

    def post(self):

        parser.add_argument('roomnumber')
        data = parser.parse_args()
        rno = data['roomnumber']        
        if get_db().cursor().execute(f'SELECT id FROM rooms WHERE roomnumber = "{rno}"').fetchone():
            return {'message': f'Room {rno} already exists'}
        get_db().cursor().execute(f'INSERT INTO rooms(id, roomnumber) VALUES({hash(rno)}, "{rno}")')
        get_db().commit()
        get_db().close()
        return jsonify({'message': 'successfully added room'})

class Rooms(Resource):

    def get(self):
        
        result = get_db().cursor().execute('SELECT * FROM rooms')
        rows = result.fetchall()
        get_db().close()
        response = []
        for row in rows:
            response.append(dict(zip([c[0] for c in result.description], row)))
        return response