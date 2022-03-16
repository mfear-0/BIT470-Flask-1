from datetime import date
from flask_jwt_extended import create_access_token, JWTManager, jwt_required
from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request #, abort, g, url_for
from src.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
#from passlib.apps import custom_app_context as pwd_context
#from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

parser = reqparse.RequestParser()

class Room(Resource): 

    def get(self, room_no):

        try:

            # Arica: Checks to see if the provided room number matches an existing room in the Rooms table.
            if not get_db().cursor().execute(f'SELECT * FROM rooms WHERE roomnumber = {room_no}').fetchone():
                get_db().close()
                message = jsonify(error = 'Could not find the specified room. Please check if the room number is typed correctly.')
                return make_response(message, 404)

            # Arica: Returns the specified room and the HTTP code 200 OK.
            result = get_db().cursor().execute(f'SELECT * FROM rooms WHERE roomnumber = {room_no}')
            row = result.fetchone()
            get_db().close()
            response = dict(zip([c[0] for c in result.description], row))
            response = jsonify(response)
            return make_response(response, 200)

        except:

            # Arica: Returns an error message for any problems that occurred during the GET one room process.
            message = jsonify(error = 'Something went wrong when getting the specified room. Please try again. Try using quotation marks around the room number in the endpoint if you have not already done so.')
            return make_response(message, 500)
    
    @jwt_required()
    def put(self, room_no):

        try:

            # Arica: The room number is the only field the user would provide.
            parser.add_argument('roomnumber')
            data = parser.parse_args()
            rno = data['roomnumber'] 

            # Arica: Checks to see if a room number was provided.
            if not data['roomnumber']:
                message = jsonify(error = 'The room number is required to update a room. Please provide a room number.')
                return make_response(message, 400)

            # Arica: Checks to see if the provided room number does not match an existing room in the room table.
            if not get_db().cursor().execute(f'SELECT * FROM rooms WHERE roomnumber = {room_no}').fetchone():
                get_db().close()
                message = jsonify(error = 'Could not find the specified room. Please check if the room number is typed correctly.')
                return make_response(message, 404)      

            # Arica: Updates the room number that matches the provided room number and returns the HTTP code 200 OK.
            get_db().cursor().execute(f'UPDATE rooms SET roomnumber = "{rno}" WHERE roomnumber = {room_no}')
            get_db().commit()
            get_db().close()
            message = jsonify(message = f'The room \'{rno}\' has been successfully updated.')
            return make_response(message, 200)

        except:

            # Arica: Returns an error message for any problems that occurred during the PUT one room process.
            message = jsonify(error = 'Something went wrong when editing the room. Please try again. Try using quotation marks around the room number in the endpoint if you have not already done so.')
            return make_response(message, 500)
    

    @jwt_required()
    def delete(self, room_no):

        try:

            # Arica: Checks to see if the provided room number matches an existing room in the Rooms table.
            if not get_db().cursor().execute(f'SELECT * FROM rooms WHERE roomnumber = {room_no}').fetchone():
                get_db().close()
                message = jsonify(error = 'Could not find the specified room. Please check if the room number is typed correctly.')
                return make_response(message, 404)

            # Arica: Deletes the room that matches the provided room number and returns the HTTP code 200 OK.
            # The following two lines of code are to save the room number from the database and then convert that result's tuple into a string,
            # so that when the room is deleted, the return message displays the name of the room for clarity to the user.

            roomnumber = get_db().cursor().execute(f'SELECT roomnumber FROM rooms WHERE roomnumber = {room_no}').fetchone()
            roomnumber = ''.join(roomnumber)
            get_db().cursor().execute(f'DELETE FROM rooms WHERE roomnumber = {room_no}')
            get_db().commit()

            # Arica: This will also delete any assignments that have the same room number from the Assignments table.
            if get_db().cursor().execute(f'SELECT * FROM assignments WHERE roomnumber = {room_no}').fetchone():
                get_db().cursor().execute(f'DELETE FROM assignments WHERE roomnumber = {room_no}')
                get_db().commit()

            get_db().close()
            message = jsonify(message = f'The room \'{roomnumber}\' has been successfully deleted.')
            return make_response(message, 200)       

        except:

            # Arica: Returns an error message for any problems that occurred during the DELETE one room process.
            message = jsonify(error = 'Something went wrong when deleting the room. Please try again. Try using quotation marks around the room number in the endpoint if you have not already done so.')
            return make_response(message, 500)


class Rooms(Resource):

    def get(self):
        
        try:
            
            # Arica: Returns a list of all the rooms and the HTTP code 200 OK.            
            result = get_db().cursor().execute('SELECT * FROM rooms')
            rows = result.fetchall()
            get_db().close()
            response = []
            for row in rows:
                response.append(dict(zip([c[0] for c in result.description], row)))
            response = jsonify(response)
            return make_response(response, 200)
        
        except:

            # Arica: Returns an error message for any problems that occurred during the GET all rooms process.
            message = jsonify(error = 'Something went wrong when getting all the rooms. Please try again.')
            return make_response(message, 500)
    
    @jwt_required()
    def post(self):

        try: 

            parser.add_argument('roomnumber')
            data = parser.parse_args()
            rno = data['roomnumber']

            # Arica: Checks to see if a room number was provided.
            if not data['roomnumber']:
                message = jsonify(error = 'The room number is required to add a new room. Please add a room number.')
                return make_response(message, 400)

            # Arica: Checks to see if the room the client wants to add already exists.
            if get_db().cursor().execute(f'SELECT id FROM rooms WHERE roomnumber = "{rno}"').fetchone():
                get_db().close()
                message = jsonify(error = f'The room \'{rno}\' already exists. Please use a different room number.')
                return make_response(message, 400)

            get_db().cursor().execute(f'INSERT INTO rooms(id, roomnumber) VALUES({hash(rno)}, "{rno}")')
            get_db().commit()
            get_db().close()
            message = jsonify(message = f'The room \'{rno}\' has been successfully added.')
            return make_response(message, 201)
        
        except:

            # Arica: Returns an error message for any problems that occurred during the POST one room process.
            message = jsonify(error = 'Something went wrong when adding the room. Please try again.')
            return make_response(message, 500)

