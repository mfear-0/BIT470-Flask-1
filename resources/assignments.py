from datetime import date
import json
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_restful import Resource, reqparse
from flask import Flask, jsonify, make_response, request
from src.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

parser = reqparse.RequestParser()


class Assignments(Resource):

    def get(self):

        try:

            result = get_db().cursor().execute(f'SELECT * FROM assignments')

            rows = result.fetchall()
            get_db().close()
            response = []
            for row in rows:
                response.append(dict(zip([c[0] for c in result.description], row)))
            response = jsonify(response)
            return make_response(response, 200)

        except:

            message = jsonify(error = 'Something went wrong when getting all the assignments. Please try again.')
            return make_response(message, 500)

    @jwt_required()
    def post(self):   

        try:

            #TODO: Check for empty input before checking if the values exist. Finalize the error messages.
                     
            parser.add_argument('staffid')
            parser.add_argument('taskid')
            parser.add_argument('roomnumber')
            parser.add_argument('status')

            data = parser.parse_args()
            staffid = data['staffid'] 
            roomno = data['roomnumber'] 
            taskid = data['taskid']
            st = data['status']
            if not get_db().cursor().execute(f'SELECT * FROM staff WHERE staffid = "{staffid}"').fetchone():
                message = jsonify(error = 'Staff member of that id does not exist.')
                return make_response(message, 404)
            if not get_db().cursor().execute(f'SELECT * FROM rooms WHERE roomnumber = "{roomno}"').fetchone():
                message = jsonify(error = 'Room of that number does not exist.')
                return make_response(message, 404)
            if not get_db().cursor().execute(f'SELECT * FROM tasks WHERE taskid = "{taskid}"').fetchone():
                message = jsonify(error = 'Task of that id does not exist.')
                return make_response(message, 404)
            if not st:
                message = jsonify(error = 'Please state the status of your assignment')
                return make_response(message, 404)
            get_db().cursor().execute(f'INSERT INTO assignments(staffid, taskid, roomnumber, status) VALUES({staffid}, {taskid}, "{roomno}", "{st}")')
            get_db().commit()
            get_db().close()
            message = jsonify(message = 'Assignment successfully added.')
            return make_response(message, 200) 
        except:
            message = jsonify(error = 'Something went wrong when creating the assignment. Please try again.')
            return make_response(message, 500)


class Assignment(Resource):

    def get(self, assignid):

        try:

            if not get_db().cursor().execute(f'SELECT * FROM assignments WHERE id = {assignid}').fetchone():
                get_db().close()
                message = jsonify(error = 'Could not find the specified assignment. Please check if the Assignment ID is typed correctly.')
                return make_response(message, 404)

            result = get_db().cursor().execute(f'SELECT * FROM assignments WHERE id = {assignid}')
            row = result.fetchone()
            get_db().close()
            response = dict(zip([c[0] for c in result.description], row))
            response = jsonify(response)
            return make_response(response, 200)

        except:

            message = jsonify(error = 'Something went wrong when getting the specified assignment. Please try again.')
            return make_response(message, 500)


    @jwt_required()
    def put(self, assignid):

        try:

            #TODO: Check for empty input before checking if the values exist. Finalize the error messages.

            parser.add_argument('staffid')
            parser.add_argument('roomnumber')
            parser.add_argument('taskid')
            parser.add_argument('status')
            data = parser.parse_args()
            stid = data['staffid']
            rmid = data['roomnumber']
            tkid = data['taskid']
            st = data['status']


            if stid:
                # stidd = get_db().cursor().execute(f'SELECT * FROM staff WHERE staffid={stid}').fetchone()
                # if not stidd[0]:
                #     message = jsonify(error = 'staff does not exist. Please provide a valid staff id.')
                #     return make_response(message, 400)
                get_db().cursor().execute(f'UPDATE assignments SET staffid={stid} WHERE id={assignid}')
                get_db().commit()
                get_db().close()

            if rmid:
                
                # rmidd = get_db().cursor().execute(f'SELECT * FROM rooms WHERE roomnumber= "{rmid}"').fetchone()
                # if not rmidd[0]:
                #     message = jsonify(error = 'Room does not exist. Please provide a valid Room id.')
                #     return make_response(message, 400)
                get_db().cursor().execute(f'UPDATE assignments SET roomnumber="{rmid}" WHERE id={assignid}')
                get_db().commit()
                get_db().close()
                #return({"msg": "hey"})
            
            if tkid:
                # tkidd = get_db().cursor().execute(f'SELECT * FROM tasks WHERE taskid={tkid}').fetchone()
                # if not tkidd[0]:
                #     message = jsonify(error = 'Task does not exist. Please provide a valid Task id.')
                #     return make_response(message, 400)
                get_db().cursor().execute(f'UPDATE assignments SET taskid={tkid} WHERE id={assignid}')
                get_db().commit()
                get_db().close()

            if st:
                get_db().cursor().execute(f'UPDATE assignments SET status="{st}" WHERE id={assignid}')
                get_db().commit()
                get_db().close()

            # result = get_db().cursor().execute(f'SELECT * FROM assignments WHERE id={assignid}')
            # row = result.fetchone()
            # return dict(zip([c[0] for c in result.description], row))
            message = jsonify(message = 'Successfully edited the assignment.')
            return make_response(message, 200)

        except:
            message = jsonify(error = 'Something went wrong when editing the assignment. Please try again.')
            return make_response(message, 500)
    

    @jwt_required()
    def delete(self, assignid):

        try:

            if not get_db().cursor().execute(f'SELECT * FROM assignments WHERE id={assignid}').fetchone():
                get_db().close()
                message = jsonify(error = 'Could not find the specified assignment. Please check if the Assignment ID is typed correctly.')
                return make_response(message, 404)

            # Arica: Deletes the assignment that matches the provided Assignment ID and returns the HTTP code 200 OK.
            # Normally, we would want to return the name of the item to the user so they know what item they deleted. But since the assignments
            # do not have a name, we are going to return the Assignment ID instead.

            get_db().cursor().execute(f'DELETE FROM assignments WHERE id = {assignid}')
            get_db().commit()
            get_db().close()

            message = jsonify(message = f'The assignment \'{assignid}\' has been successfully deleted.')
            return make_response(message, 200) 

        except:

            message = jsonify(error = 'Something went wrong when deleting the assignment. Please try again.')
            return make_response(message, 500)
